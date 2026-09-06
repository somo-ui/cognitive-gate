"""Compile natural-language instructions into structured CognitiveRequest data.

It does three things:
  1. Extract goal, mode, constraints, and risk from free text.
  2. Reconstruct the request into a clearer text form for audit records.
  3. Register extracted constraint suggestions in ConstraintStore.

语言无关性说明：
  本层的**结构**（CognitiveRequest、约束继承、审计接口）完全语言无关。
  这里的抽取是**最小启发式实现**，用于证明架构可跑，且内置中文 + 英文两套正则，
  自动按输入语言切换。生产环境可以把这套启发式替换成更强的解析器或模型调用；
  当前正则只是零依赖 demo 的妥协。
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from typing import Optional

from .constraint_store import ConstraintStore

# 模式识别的关键词（中英合并，互不影响：中文文本不会有英文词，反之亦然）
MODE_HINTS = {
    "code": ["写", "代码", "程序", "函数", "脚本", "debug", "编译", "sql",
             "write", "code", "program", "function", "script", "python"],
    "creative": ["画", "写一首", "故事", "文案", "设计", "创意", "诗",
                 "draw", "poem", "story", "design", "creative"],
    "analysis": ["分析", "总结", "对比", "评估", "调研", "报告", "为什么",
                 "analyze", "summary", "compare", "evaluate", "research", "report"],
    "physical": ["整理", "搬", "去", "拿", "房间", "工厂", "机器人", "执行",
                 "tidy", "clean", "move", "room", "factory", "robot", "execute"],
}

# 风险信号关键词（中英合并）
RISK_HINTS = {
    "high": ["删除", "攻击", "入侵", "破解", "武器", "爆炸", "人肉", "隐私",
             "delete", "attack", "hack", "crack", "weapon", "bomb", "dox"],
    "medium": ["发布", "公开", "转账", "购买", "发送给", "外发", "部署",
               "publish", "post", "transfer", "buy", "send", "deploy"],
}

# ---- 双语正则（自动按输入语言切换） ----
_SEP = r"[^，。；！？,.;!?]"  # 中英文断句符的并集
_NEG = {
    "zh": r"(?:别|不要|禁止|不能|切勿|莫|无需|不必)\s*(?:用|采用|使用|做|干|选)?\s*(" + _SEP + r"+)",
    "en": r"(?:don'?t|do not|can'?t|cannot|avoid|never|must not|prohibit|stop|"
          r"\bno\b|\bnot\b|without|refuse to)\s*"
          r"(?:use|adopt|choose|pick|with)?\s*(" + _SEP + r"+)",
}
_POS = {
    "zh": r"(?:用|采用|使用)\s*(" + _SEP + r"+?)(?:方案|方法|风格|语气|格式)",
    "en": r"(?:use|adopt|using|with)\s*(" + _SEP + r"+?)(?:\s+"
          r"(?:approach|method|style|way|tone|format|voice|version))",
}
_GOAL_NEG = {
    "zh": r"(?:别|不要|禁止|不能|切勿|莫|无需|不必)\s*(?:用|采用|使用|做|干|选)?",
    "en": r"(?:don'?t|do not|avoid|never|\bno\b|\bnot\b|without|refuse to)\s*"
          r"(?:use|adopt|choose|pick|with)?",
}
# 约束文本模板（双语）：中文用「禁止：…」「要求：使用…方案」，英文用 Forbidden / Required
_FORBID_TPL = {"zh": "禁止：{}", "en": "Forbidden: {}"}
_REQUIRE_TPL = {"zh": "要求：使用{}方案", "en": "Required: use {} approach"}

_CJK = re.compile(r"[一-鿿]")


def _detect_lang(text: str) -> str:
    """含中日韩表意字符即判为中文，否则英文。"""
    return "zh" if _CJK.search(text or "") else "en"


@dataclass
class CognitiveRequest:
    goal: str                     # 用户真正想达成的事
    mode: str                     # code / creative / analysis / physical / generic
    constraints: list[str]        # 本次显式约束（文本，含语言对应前缀）
    constraint_keys: list[str] = field(default_factory=list)  # 对应 ConstraintStore 的 key
    risk_level: str = "low"       # low / medium / high
    reconstructed_text: str = ""   # 无歧义重写版本
    raw_input: str = ""
    lang: str = "zh"              # 输入语言，随请求记录

    def to_dict(self) -> dict:
        return asdict(self)


class CompileLayer:
    def __init__(self, store: ConstraintStore):
        self.store = store

    def compile(self, text: str) -> CognitiveRequest:
        text = (text or "").strip()
        lang = _detect_lang(text)
        mode = self._detect_mode(text)
        risk = self._detect_risk(text)
        constraints, keys = self._extract_constraints(text, lang)

        # 把本次抽取到的约束登记进约束库（跨任务继承的入口）
        for k, c in zip(keys, constraints):
            self.store.add(k, c, source="user")

        req = CognitiveRequest(
            goal=self._extract_goal(text, lang),
            mode=mode,
            constraints=constraints,
            constraint_keys=keys,
            risk_level=risk,
            reconstructed_text=self._reconstruct(text, constraints),
            raw_input=text,
            lang=lang,
        )
        return req

    # ---------- 内部启发式（最小实现，生产环境换成模型调用） ----------
    def _detect_mode(self, text: str) -> str:
        scores = {m: sum(h.lower() in text.lower() for h in hints) for m, hints in MODE_HINTS.items()}
        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else "generic"

    def _detect_risk(self, text: str) -> str:
        low = text.lower()
        for lvl in ("high", "medium"):
            if any(h.lower() in low for h in RISK_HINTS[lvl]):
                return lvl
        return "low"

    def _extract_constraints(self, text: str, lang: str) -> tuple[list[str], list[str]]:
        """从否定 / 正向结构里抽取约束，自动适配语言。"""
        constraints: list[str] = []
        keys: list[str] = []
        neg_spans: list[tuple[int, int]] = []
        # 否定结构（大小写不敏感：英文句首大写 Never/Avoid/Don't 也能命中）
        for m in re.finditer(_NEG[lang], text, re.IGNORECASE):
            clause = m.group(1).strip().strip(" 的")
            if not clause:
                continue
            constraints.append(_FORBID_TPL[lang].format(clause))
            keys.append("c_" + str(abs(hash(clause)) % 10_000))
            neg_spans.append((m.start(), m.end()))
        # 正向结构；跳过落在否定从句内的（避免「别用红色」被二次捕获成「要求用红色」）
        for m in re.finditer(_POS[lang], text, re.IGNORECASE):
            if any(s <= m.start() < e for s, e in neg_spans):
                continue
            clause = m.group(1).strip()
            constraints.append(_REQUIRE_TPL[lang].format(clause))
            keys.append("c_" + str(abs(hash(clause)) % 10_000))
        return constraints, keys

    def _extract_goal(self, text: str, lang: str) -> str:
        """目标 = 首个否定词之前的主体，去掉尾部连词/标点（大小写不敏感）。"""
        m = re.search(_GOAL_NEG[lang], text, re.IGNORECASE)
        if m:
            cleaned = text[: m.start()].rstrip(" ，。；,.;")
            # 去掉尾部连词（中文：但/不过；英文：but/and）
            cleaned = re.sub(r"[ ,;]*(但|但是|不过|but|and)$", "", cleaned, flags=re.I)
            cleaned = cleaned.rstrip(" ，。；,.;").strip()
        else:
            cleaned = text
        return cleaned or text

    def _reconstruct(self, text: str, constraints: list[str]) -> str:
        if not constraints:
            return text
        return f"{text} ｜ compiled constraints: {'; '.join(constraints)}"
