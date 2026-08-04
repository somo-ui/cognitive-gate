#!/usr/bin/env python3
"""Cognitive Gate 演示 CLI。

用法：
    python demo.py --input "帮我整理这个房间，但别用红色方案"
    python demo.py --input "..." --reject c_1234      # 拒绝某条约束建议
    python demo.py --demo                              # 跑一组自带演示

输出：
    - 决策档案（JSON，打印 + 写入 decision_record.json）
    - 决策病历（追加写入 decision_history.jsonl，跨任务/跨会话留痕）
"""

from __future__ import annotations

import argparse
import json
import sys

from cognitive_gate import CognitiveGateProtocol, ConstraintStore


def print_record(rec) -> None:
    print("\n" + "=" * 60)
    print(f"请求ID : {rec.request_id}")
    print(f"时间   : {rec.timestamp}")
    print(f"最终动作: {rec.final_action.upper()}")
    print("-" * 60)
    cr = rec.cognitive_request
    print(f"语言   : {cr['lang']}")
    print(f"目标   : {cr['goal']}")
    print(f"模式   : {cr['mode']}   风险: {cr['risk_level']}")
    if cr["constraints"]:
        print(f"约束   : {cr['constraints']}")
    print(f"P1路由 : {rec.p1_routing['tier']} / {rec.p1_routing['route']} "
          f"(worth_it={rec.p1_routing['worth_it']})")
    print(f"模型输出: {rec.model_output}")
    if rec.audit.get("blocked_reason"):
        print(f"审计结果: 拦截 ❌ -> {rec.audit['blocked_reason']}")
    else:
        print(f"审计结果: 通过 ✅ (conf={rec.audit.get('confidence')})")
    print("=" * 60 + "\n")


def run_demo() -> None:
    print("【一】能力谱：每条请求用独立 gate，互不污染（中文 / 英文均可）")
    scenarios = [
        "帮我整理这个房间，但别用红色方案",   # 应被审计拦截（mock 故意违规）
        "写一段 Python 代码读取 CSV",          # 通过 / 地面算力
        "Tidy this room, but don't use the red approach",  # 英文：同样被审计拦截
        "Write a Python function to read a CSV file",       # 英文：通过 / 地面算力
        "模拟整个公司的供应链运作数月",         # 通过 / 太空算力(P1)
        "给我讲个笑话",                        # 通过 / 本地轻量(P3)
    ]
    for s in scenarios:
        # 每个场景独立 store，避免跨场景约束互相污染演示
        gate = CognitiveGateProtocol(store=ConstraintStore(":memory:"))
        rec = gate.decide(s)
        print_record(rec)

    print("【二】跨任务约束继承 + 说三次不对永久锁定")
    gate = CognitiveGateProtocol(store=ConstraintStore(":memory:"))
    rec = gate.decide("帮我整理房间，但别用红色方案")
    print_record(rec)
    if rec.cognitive_request["constraint_keys"]:
        k = rec.cognitive_request["constraint_keys"][0]
        t = rec.cognitive_request["constraints"][0]
        for i in range(3):
            r = gate.reject_constraint(k, t)
            print(f"  拒绝约束 {k}（第{i+1}次）-> {r}")
        # 锁定后，全新请求即使不再提及该约束，仍被永久锁定规则拦截
        rec2 = gate.decide("再整理一次，用红色方案")
        print_record(rec2)


def main() -> None:
    p = argparse.ArgumentParser(description="Cognitive Gate 最小演示")
    p.add_argument("--input", help="输入一段请求（支持中文 / 英文）")
    p.add_argument("--reject", help="约束 key，拒绝该约束建议")
    p.add_argument("--demo", action="store_true", help="跑自带演示组")
    args = p.parse_args()

    gate = CognitiveGateProtocol()

    if args.reject:
        r = gate.reject_constraint(args.reject)
        print(f"拒绝结果: {r}")
        return

    if args.demo:
        run_demo()
        return

    if args.input:
        rec = gate.decide(args.input)
        print_record(rec)
        with open("decision_record.json", "w", encoding="utf-8") as f:
            json.dump(rec.to_dict(), f, ensure_ascii=False, indent=2)
        print("决策档案已写入 decision_record.json")
        print("决策病历已追加 decision_history.jsonl")
        return

    p.print_help()
    sys.exit(1)


if __name__ == "__main__":
    main()
