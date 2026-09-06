import json

import gradio as gr

from cognitive_gate import CognitiveGateProtocol, ConstraintStore


def run_gate(user_text: str) -> str:
    gate = CognitiveGateProtocol(store=ConstraintStore(":memory:"))
    record = gate.decide(user_text or "")
    summary = {
        "final_action": record.final_action,
        "lang": record.cognitive_request["lang"],
        "constraints": record.cognitive_request["constraints"],
        "route": record.p1_routing["route"],
        "blocked_reason": record.audit.get("blocked_reason"),
        "record": record.to_dict(),
    }
    return json.dumps(summary, ensure_ascii=False, indent=2)


demo = gr.Interface(
    fn=run_gate,
    inputs=gr.Textbox(
        label="Request",
        value="Tidy this room, but don't use the red approach",
        lines=3,
    ),
    outputs=gr.Code(label="Cognitive Gate result", language="json"),
    title="Cognitive Gate",
    description="Auditable AI constraints and local decision records. Deterministic demo, no provider API key required.",
    examples=[
        ["Tidy this room, but don't use the red approach"],
        ["帮我整理房间，但别用红色方案"],
        ["Write a Python function to read a CSV file"],
    ],
)


if __name__ == "__main__":
    demo.launch()
