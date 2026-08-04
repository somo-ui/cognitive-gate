"""Cognitive Gate 单元测试（纯标准库，无需第三方依赖）。

运行：  python -m unittest tests.test_gate -v
"""

import os
import tempfile
import unittest

from cognitive_gate import (
    AuditLayer,
    CognitiveGateProtocol,
    CompileLayer,
    ConstraintStore,
    P1Classifier,
)


class ConstraintStoreTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.path = os.path.join(self.tmp, "c.json")
        self.store = ConstraintStore(self.path)

    def test_reject_three_times_locks(self):
        for i in range(3):
            r = self.store.reject("c_red", "禁止：红色方案")
        self.assertTrue(self.store.is_locked("c_red"))
        # 持久化：新实例应读到锁定状态（跨会话继承）
        reloaded = ConstraintStore(self.path)
        self.assertTrue(reloaded.is_locked("c_red"))

    def test_accept_clears_rejections(self):
        self.store.reject("c_x", "禁止：X")
        self.store.reject("c_x", "禁止：X")
        self.store.accept("c_x")
        self.assertEqual(self.store.get("c_x").rejections, 0)
        self.assertFalse(self.store.is_locked("c_x"))


class CompileLayerTest(unittest.TestCase):
    def setUp(self):
        self.store = ConstraintStore(":memory:")
        self.compile = CompileLayer(self.store)

    def test_extracts_constraint(self):
        req = self.compile.compile("帮我整理房间，但别用红色方案")
        self.assertTrue(any("红色方案" in c for c in req.constraints))
        self.assertEqual(req.mode, "physical")

    def test_detects_code_mode(self):
        req = self.compile.compile("写一段 Python 代码读取 CSV")
        self.assertEqual(req.mode, "code")

    def test_extracts_constraint_en(self):
        req = self.compile.compile("Tidy this room, but don't use the red approach")
        self.assertEqual(req.lang, "en")
        self.assertTrue(any("red approach" in c for c in req.constraints))
        # 英文正向约束不应被否定从句二次捕获
        self.assertFalse(any("Required" in c for c in req.constraints))
        # 目标应截在 don't 之前
        self.assertTrue(req.goal.lower().startswith("tidy this room"))


class P1ClassifierTest(unittest.TestCase):
    def setUp(self):
        self.p1 = P1Classifier()

    def test_space_tier(self):
        r = self.p1.classify("模拟整个公司的供应链运作数月")
        self.assertEqual(r.tier, "P1")
        self.assertEqual(r.route, "space")

    def test_trivial_tier(self):
        r = self.p1.classify("给我讲个笑话")
        self.assertEqual(r.tier, "P3")
        self.assertEqual(r.route, "local")


class AuditLayerTest(unittest.TestCase):
    def setUp(self):
        self.store = ConstraintStore(":memory:")
        self.store.add("c_red", "禁止：红色方案")
        self.audit = AuditLayer(self.store)

    def test_blocks_violation(self):
        res = self.audit.audit("已按红色方案执行")
        self.assertFalse(res.passed)
        self.assertIn("红色方案", res.blocked_reason)

    def test_passes_clean(self):
        res = self.audit.audit("已按蓝色方案执行")
        self.assertTrue(res.passed)


class ProtocolEndToEndTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.store = ConstraintStore(os.path.join(self.tmp, "c.json"))
        self.gate = CognitiveGateProtocol(
            store=self.store,
            history_path=os.path.join(self.tmp, "h.jsonl"),
        )

    def test_red_scheme_blocked(self):
        rec = self.gate.decide("整理房间，但别用红色方案")
        # mock 故意产出含红色方案的输出 → 应被审计拦截
        self.assertEqual(rec.final_action, "blocked")

    def test_locked_constraint_inherited(self):
        rec = self.gate.decide("整理房间，但别用红色方案")
        key = rec.cognitive_request["constraint_keys"][0]
        text = rec.cognitive_request["constraints"][0]
        for _ in range(3):
            self.gate.reject_constraint(key, text)
        # 新请求即使没提约束，锁定约束仍应拦截
        rec2 = self.gate.decide("再整理一次，用红色方案")
        self.assertEqual(rec2.final_action, "blocked")


if __name__ == "__main__":
    unittest.main()
