"""生成修正版五页 PDF 方案（马斯克展示包）。

落实上一轮的五点修正：
  1) 行动路径重排：仓库+演示先行，X 为主、邮件为辅
  2) 修正 Grok 时间线、补 GPU 来源（诚实标注）
  3) 用马斯克"停止按钮"原话 + xAI 创始人全离职当弹药
  4) 诚实区分"可靠性"与"生存性安全"，不把护栏写成保险
  5) 送达渠道改为 X+仓库为主、code@x.com 为辅

依赖：reportlab（仅用于生成此 PDF，系统本身无需）。
字体：内置 Adobe CJK (STSong-Light)，无需外部字体文件。
"""

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import (
    HRFlowable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
FONT = "STSong-Light"

INK = colors.HexColor("#1a1a1a")
ACCENT = colors.HexColor("#0b5cab")
GREY = colors.HexColor("#555555")
LINE = colors.HexColor("#cccccc")

styles = {
    "title": ParagraphStyle("title", fontName=FONT, fontSize=20, leading=26,
                            textColor=INK, spaceAfter=2),
    "sub": ParagraphStyle("sub", fontName=FONT, fontSize=10.5, leading=15,
                          textColor=GREY, spaceAfter=8),
    "h2": ParagraphStyle("h2", fontName=FONT, fontSize=13.5, leading=18,
                         textColor=ACCENT, spaceBefore=6, spaceAfter=4),
    "body": ParagraphStyle("body", fontName=FONT, fontSize=10.5, leading=16,
                           textColor=INK, alignment=TA_LEFT, spaceAfter=4),
    "bullet": ParagraphStyle("bullet", fontName=FONT, fontSize=10.5, leading=15.5,
                             textColor=INK, leftIndent=12, spaceAfter=2),
    "small": ParagraphStyle("small", fontName=FONT, fontSize=9, leading=13,
                            textColor=GREY),
    "cell": ParagraphStyle("cell", fontName=FONT, fontSize=9.3, leading=13,
                           textColor=INK),
    "cellh": ParagraphStyle("cellh", fontName=FONT, fontSize=9.3, leading=13,
                            textColor=colors.white),
}

EM = '<font color="#0b5cab">{}</font>'


def P(text, style="body"):
    return Paragraph(text, styles[style])


def bullets(items, style="bullet"):
    return [Paragraph("• " + t, styles[style]) for t in items]


def build():
    out = "/Users/suton/WorkBuddy/2026-08-04-23-57-19/cognitive-gate/马斯克展示方案_修正版.pdf"
    doc = SimpleDocTemplate(
        out, pagesize=A4,
        leftMargin=18 * mm, rightMargin=18 * mm,
        topMargin=16 * mm, bottomMargin=14 * mm,
        title="给马斯克：一个他内部团队还没有做出的技术解决方案",
        author="Cognitive Gate",
    )
    s = []

    # ---------- 页 1：问题陈述 ----------
    s.append(P("给马斯克：一个他内部团队还没有做出的技术解决方案", "title"))
    s.append(P("基于你 2026 年公开言论与项目动向的展示包（修正版）", "sub"))
    s.append(HRFlowable(width="100%", thickness=0.8, color=LINE, spaceAfter=8))

    s.append(P("你 2026-07-23 在《经济学人》专访里说了三句话：", "h2"))
    s.extend(bullets([
        "“约五年内，AI 智力将超过人类总和。”",
        "“十年后，人类不太可能还掌控局面。”",
        EM.format("“即使有停止按钮，也不该按。”") + " —— “我找不到任何能阻止它的办法。”",
    ]))
    s.append(Spacer(1, 4))
    s.append(P(
        "与此同时你在加速：用数十万块 GPU 训练 Grok（孟菲斯 Colossus 集群，"
        "具体规模以 xAI 披露为准），并把 Grok 作为 Optimus 与 Macrohard 的“导航器”。", "body"))
    s.append(P(
        "不对称很清楚：你在建造一艘你知道可能失控的船，但还没有安装舵。"
        "你公开提出的解法是“同行评审”——让 AI 公司互相审查。那是<font color='#0b5cab'>治理层</font>；"
        "本方案是让“审查”在模型输出层面可被执行的<font color='#0b5cab'>技术层</font>。", "body"))

    # ---------- 页 2：解决方案 ----------
    s.append(PageBreak())
    s.append(P("二、解决方案：在 Grok 之前编译，在 Grok 之后审计", "h2"))
    s.extend(bullets([
        "<b>编译</b>：把模糊人类指令变成结构化 CognitiveRequest（目标 / 模式 / 约束 / 风险 / 重建文本）"
        "——Optimus 与 Macrohard 拿到的是确定性结构，不是概率性文本。",
        "<b>锁定</b>：用户说三次“不对” → 永久锁定规则，跨任务永不丢失。",
        "<b>审计</b>：Grok 输出后，检查是否符合用户确认的规则；违反则拦截并返回 blocked_reason。",
    ]))
    s.append(Spacer(1, 4))
    s.append(P("诚实的范围声明（重要，避免对你过度承诺）：", "h2"))
    s.extend(bullets([
        "本系统解决的是 <font color='#0b5cab'>可控性 / 可审计性 / 一致性</font>，"
        "不是 <font color='#0b5cab'>生存性安全</font>。它不承诺防止“AI 接管人类”那种灾难性风险。",
        "对 LLM 输出的约束合规审计，目前是 best-effort 护栏，不是数学保证——这是开放研究问题。"
        "我们以可解释规则 + 可插拔模型自检做“最大努力拦截”，并标注置信度。请勿将其宣传为对灭绝风险的保险。",
    ]))

    # ---------- 页 3：与体系对齐 ----------
    s.append(PageBreak())
    s.append(P("三、与你的体系精确对齐", "h2"))
    rows = [
        [P("你的体系", "cellh"), P("本系统提供的层", "cellh")],
        [P("Grok（输出不可控、不可审计）", "cell"), P("输出前意图编译 + 输出后约束审计", "cell")],
        [P("Optimus / Macrohard", "cell"), P("从“模糊指令”到“确定性任务”的翻译层（缺失的决策层）", "cell")],
        [P("Macrohard（跨任务规则一致性）", "cell"), P("跨轮约束继承：说三次不对永久锁定", "cell")],
        [P("太空算力（轨道数据中心极贵）", "cell"), P("P1 分型器：判断任务值不值得、用哪类算力", "cell")],
        [P("跨公司 AI 治理", "cell"), P("统一的 AI 决策审计协议（协议，不是集成）", "cell")],
    ]
    t = Table(rows, colWidths=[58 * mm, 106 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("GRID", (0, 0), (-1, -1), 0.5, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f6fb")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    s.append(t)
    s.append(Spacer(1, 5))
    s.append(P("为什么你的团队还没做出来（真实证据，不是贬低）：", "h2"))
    s.append(P(
        "截至 2026 年 3 月底，xAI 全部 11 位联合创始人已离职；你本人称技术路线"
        "“从地基就盖错了”，正“从地基开始重建”。在重建期的架构上叠加控制层，"
        "比从头设计带控制层的架构更难——这正是外部层能补的位。", "body"))
    s.append(P(
        "你的解法（同行评审）和我们（技术审计层）不冲突：你是治理层，我们是它的可执行技术底座。", "body"))

    # ---------- 页 4：可验证证据 ----------
    s.append(PageBreak())
    s.append(P("四、可验证的证据（诚实标注）", "h2"))
    s.extend(bullets([
        "系统已开源：cognitive-gate，纯标准库，零配置可跑。",
        "已通过 <b>10 项单元测试</b> + 端到端演示（原方案写“137 项”——我们如实改为实际数字）。",
        "3 分钟验证：clone → <font face='Courier'>python -m unittest</font> → "
        "<font face='Courier'>python demo.py --demo</font>。",
        "输入一段请求（中文 / 英文均可），输出结构化决策档案 + 决策病历；你确认过的规则永久锁定，否决过的永不重提。",
        "所有个人数据仅落本地 constraints.json / decision_history.jsonl，可物理删除。",
        "模型可插拔：默认 MockGrok，设 XAI_API_KEY 即接真 Grok——控制层不变，引擎可换。",
    ]))

    # ---------- 页 5：下一步（重排后的行动路径） ----------
    s.append(PageBreak())
    s.append(P("五、下一步（重排后的行动路径）", "h2"))
    s.extend(bullets([
        "<b>1. 仓库已公开（GitHub）</b>：任何人可独立 clone、运行、验证——这是“公开可验证”记录。",
        "<b>2. 在 X 公开发布并 @elonmusk</b>，附可运行 demo 链接"
        "（X 是你团队监控、你本人会回应技术反馈的渠道，比招聘邮箱更可能被看见）。",
        "<b>3. 备选 code@x.com</b>：你用于招募硬核工程师的公开邮箱，作为次要投递"
        "——但它是招聘过滤，非技术提案首选。",
        "<b>4. 一周无回复，不重复发送</b>；将本方案用于下一个目标。",
    ]))
    s.append(Spacer(1, 6))
    s.append(HRFlowable(width="100%", thickness=0.8, color=LINE, spaceAfter=6))
    s.append(P(
        "最终一句话：你不是在“卖一个产品”。你是在他公开承认的痛点上，"
        "提供一个他内部团队（正处于重建期）还没有做出的完整技术实现。"
        "展示包真正的价值，在于把系统压缩成任何人都能三分钟看懂、且能三分钟跑通的东西。", "body"))
    s.append(Spacer(1, 8))
    s.append(P("附：本方案所有事实均来自 2026 年公开报道（《经济学人》7-23 专访、Macrohard 3-12 发布、"
               "SpaceX/xAI 合并与轨道数据中心 FCC 申请、Grok 争议输出报道）。数据如与最新披露不符，以一手来源为准。", "small"))

    doc.build(s)
    print("PDF 已生成：", out)


if __name__ == "__main__":
    build()
