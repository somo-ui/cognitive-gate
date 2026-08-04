"""跨任务约束继承层。

这是整套系统里最关键、也最容易被大模型原生缺失的能力：
- 用户在任务 A 说的"不要用这个方向"，要在任务 B、C、D……里持续生效；
- 用户连续三次拒绝同一条约束建议 → 该约束被**永久锁定**，系统不再提出、不再违反。

约束以 JSON 持久化，因此跨进程、跨会话继承（这正是"模拟公司运作"需要的规则一致性）。
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from typing import Optional

LOCK_THRESHOLD = 3  # 连续拒绝次数达到此值 → 永久锁定


@dataclass
class Constraint:
    key: str                 # 稳定标识，例如 "no_red_scheme"
    text: str                # 人类可读的约束描述
    rejections: int = 0      # 被用户拒绝的次数（连续计数，接受后清零）
    locked: bool = False     # 是否已被永久锁定
    source: str = "user"     # 来源：user / system / inherited

    def to_dict(self) -> dict:
        return asdict(self)


class ConstraintStore:
    """持久化的跨任务约束库。"""

    def __init__(self, path: str = "constraints.json"):
        self.path = path
        # ":memory:" 为哨兵：仅内存，不落盘（用于测试/隔离演示）
        self._persist = path != ":memory:"
        self._store: dict[str, Constraint] = {}
        self.load()

    # ---- 持久化 ----
    def load(self) -> None:
        if not self._persist:
            return
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    raw = json.load(f)
                self._store = {k: Constraint(**v) for k, v in raw.items()}
            except (json.JSONDecodeError, TypeError):
                self._store = {}
        else:
            self._store = {}

    def save(self) -> None:
        if not self._persist:
            return
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump({k: v.to_dict() for k, v in self._store.items()},
                      f, ensure_ascii=False, indent=2)

    # ---- 查询 ----
    def active_constraints(self) -> list[Constraint]:
        """返回当前生效（未被锁定）的约束——审计层只检查这些。"""
        return [c for c in self._store.values() if not c.locked]

    def locked_constraints(self) -> list[Constraint]:
        """返回已永久锁定的约束——审计层必须强制拦截，即使本次请求未提及。"""
        return [c for c in self._store.values() if c.locked]

    def is_locked(self, key: str) -> bool:
        return key in self._store and self._store[key].locked

    def get(self, key: str) -> Optional[Constraint]:
        return self._store.get(key)

    # ---- 写入 / 拒绝 ----
    def add(self, key: str, text: str, source: str = "user") -> Constraint:
        if key not in self._store:
            self._store[key] = Constraint(key=key, text=text, source=source)
            self.save()
        return self._store[key]

    def accept(self, key: str) -> None:
        """用户接受了某条约束建议 → 计入生效约束，并清零拒绝计数。"""
        c = self._store.get(key)
        if c:
            c.rejections = 0
            self.save()

    def reject(self, key: str, text: str | None = None) -> dict:
        """用户拒绝了某条约束建议。

        返回 dict 告知调用方：是否刚刚触发永久锁定。
        这是"说三次不对，永久锁定"的唯一真相来源。
        """
        c = self._store.get(key)
        if c is None:
            c = Constraint(key=key, text=text or key, rejections=0)
            self._store[key] = c
        if text:
            c.text = text
        if c.locked:
            return {"locked": True, "already_locked": True, "rejections": c.rejections}
        c.rejections += 1
        if c.rejections >= LOCK_THRESHOLD:
            c.locked = True
        self.save()
        return {"locked": c.locked, "already_locked": False, "rejections": c.rejections}

    def snapshot(self) -> list[dict]:
        return [c.to_dict() for c in self._store.values()]
