"""Streamlit UI for the Research Agent (team VietnamAirlines).

Run from starter_v0/:
    streamlit run app.py

Reuses the same model -> tool loop as chat.py and writes the same transcript JSON
format to transcripts/ (file name contains `_ui_`), so UI sessions are evidence too.
Tool calls, tool results and tool errors are shown as-is; nothing is hidden.
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st

from chat import ARTIFACTS_DIR, ROOT, now_iso, run_model_tool_loop, safe_slug, trim_history, write_transcript
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version

SYSTEM_PROMPT_PATH = ARTIFACTS_DIR / "system_prompt.md"
TOOLS_PATH = ARTIFACTS_DIR / "tools.yaml"
TRANSCRIPTS_DIR = ROOT / "transcripts"
PROVIDERS = ["openrouter", "openai", "anthropic", "gemini", "ollama"]
SAMPLE_QUESTIONS = [
    "Tweet mới nhất của Sam Altman là gì?",
    "Tin tức AI hôm nay có gì nổi bật?",
    "Trên Hacker News dân dev đang bàn gì về Rust?",
    "Tóm tắt bài viết này hộ mình",
    "Đăng bản tin AI hôm nay lên Telegram giúp mình",
]

st.set_page_config(page_title="Research Agent · VietnamAirlines", page_icon="🔎", layout="wide")


def new_session(provider_name: str, model: str | None, version: str, history_window: int, max_rounds: int) -> None:
    artifact_version = build_artifact_version(version, SYSTEM_PROMPT_PATH, TOOLS_PATH)
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
    transcript_id = "_".join([safe_slug(version), safe_slug(provider_name), "ui", timestamp])
    st.session_state.update({
        "settings": (provider_name, model, version, history_window, max_rounds),
        "history": [],
        "messages": [],
        "transcript_path": TRANSCRIPTS_DIR / f"{transcript_id}.transcript.json",
        "transcript": {
            "transcript_id": transcript_id,
            **artifact_version_dict(artifact_version),
            "provider": provider_name,
            "model": model,
            "system_prompt": str(SYSTEM_PROMPT_PATH),
            "tools": str(TOOLS_PATH),
            "history_window": history_window,
            "max_tool_rounds": max_rounds,
            "interface": "streamlit",
            "created_at": now_iso(),
            "updated_at": now_iso(),
            "turns": [],
        },
    })


def render_tool_events(rounds: list[dict[str, Any]]) -> None:
    for round_record in rounds:
        for event in round_record.get("tool_results", []):
            result = event.get("result", {})
            failed = isinstance(result, dict) and "error" in result
            label = f"{'⚠️' if failed else '🔧'} {event['tool']}({json.dumps(event.get('args', {}), ensure_ascii=False)})"
            with st.expander(label, expanded=failed):
                if failed:
                    st.error(f"{result.get('error')}: {result.get('message', '')}")
                st.json(result, expanded=False)


# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("⚙️ Cấu hình")
    provider_name = st.selectbox("Provider", PROVIDERS, index=0)
    model_input = st.text_input("Model (để trống = mặc định của provider)", value="")
    version = st.text_input("Version label", value="v3-final")
    history_window = st.slider("History window (cặp lượt)", 0, 10, 5)
    max_rounds = st.slider("Max tool rounds", 1, 6, 4)
    model = model_input.strip() or None

    settings = (provider_name, model, version, history_window, max_rounds)
    if "settings" not in st.session_state or st.button("🆕 Cuộc hội thoại mới"):
        new_session(*settings)
    elif st.session_state["settings"] != settings:
        new_session(*settings)

    transcript = st.session_state["transcript"]
    st.caption(f"artifact_version: `{transcript['artifact_version']}`")
    st.caption(f"Transcript: `{st.session_state['transcript_path'].name}`")

    st.subheader("💡 Câu hỏi mẫu")
    for question in SAMPLE_QUESTIONS:
        if st.button(question, use_container_width=True):
            st.session_state["pending_input"] = question

# ---------------- Main ----------------
st.title("🔎 Research Agent")
st.caption(
    "Tìm tin web, tweet theo tài khoản/chủ đề, Hacker News, paper arXiv, chính sách nội bộ; đọc URL; "
    "tổng hợp digest; gửi Telegram chỉ sau khi bạn xác nhận."
)

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("rounds"):
            render_tool_events(message["rounds"])

user_text = st.chat_input("Hỏi agent…") or st.session_state.pop("pending_input", None)

if user_text:
    st.session_state["messages"].append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    system_prompt = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")
    openai_tools = to_openai_tools(load_tool_declarations(TOOLS_PATH))
    messages = [
        {"role": "system", "content": system_prompt},
        *trim_history(st.session_state["history"], history_window),
        {"role": "user", "content": user_text},
    ]
    turn_record: dict[str, Any] = {
        "turn_index": len(transcript["turns"]) + 1,
        "started_at": now_iso(),
        "user": user_text,
        "status": "started",
        "assistant_text": None,
        "rounds": [],
        "tool_events": [],
    }

    with st.chat_message("assistant"):
        try:
            with st.spinner("Agent đang xử lý…"):
                result = run_model_tool_loop(
                    provider=make_provider(provider_name),
                    messages=messages,
                    tools=openai_tools,
                    model=model,
                    max_tool_rounds=max_rounds,
                )
            turn_record.update(result)
            assistant_text = result["assistant_text"] or "(không có nội dung)"
            if result["status"] == "waiting_for_user":
                assistant_text = f"❓ {assistant_text}"
            st.markdown(assistant_text)
            render_tool_events(result["rounds"])
            st.session_state["history"] += [
                {"role": "user", "content": user_text},
                {"role": "assistant", "content": result["assistant_text"] or ""},
            ]
            st.session_state["messages"].append(
                {"role": "assistant", "content": assistant_text, "rounds": result["rounds"]}
            )
        except Exception as exc:  # show provider errors instead of hiding them
            turn_record.update({"status": "provider_error", "error": f"{type(exc).__name__}: {exc}"})
            st.error(turn_record["error"])
            st.session_state["messages"].append({"role": "assistant", "content": f"⚠️ {turn_record['error']}"})

    turn_record["ended_at"] = now_iso()
    transcript["turns"].append(turn_record)
    write_transcript(st.session_state["transcript_path"], transcript)
