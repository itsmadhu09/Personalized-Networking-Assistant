"""
ui.py
-------
Streamlit frontend for the Personalized Networking Assistant.

Run with:
    streamlit run frontend/ui.py

Expects the FastAPI backend to be running at http://localhost:8000
(see backend/main.py).
"""

import streamlit as st
import requests

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="Personalized Networking Assistant", page_icon="🤝", layout="centered")
st.title("🤝 Personalized Networking Assistant")
st.caption("Generate smart, tailored conversation starters for your next networking event.")

tab_generate, tab_factcheck, tab_history = st.tabs(["✨ Generate", "🔍 Fact Check", "🕘 History"])

# ---------------------------------------------------------------------------
# Tab 1: Generate conversation starters
# ---------------------------------------------------------------------------
with tab_generate:
    event_desc = st.text_area(
        "Event description",
        placeholder="e.g. AI for Sustainable Cities",
        height=100,
    )
    interests_raw = st.text_input(
        "Your interests (comma-separated)",
        placeholder="e.g. climate change, urban planning",
    )

    if st.button("Generate Conversation Starters", type="primary"):
        if not event_desc.strip():
            st.warning("Please enter an event description first.")
        else:
            interests = [i.strip() for i in interests_raw.split(",") if i.strip()]
            with st.spinner("Analyzing event and generating starters..."):
                try:
                    resp = requests.post(
                        f"{API_BASE}/generate-conversation",
                        json={"event_description": event_desc, "interests": interests},
                        timeout=60,
                    )
                    resp.raise_for_status()
                    data = resp.json()
                    st.session_state["last_result"] = data
                except requests.exceptions.RequestException as e:
                    st.error(f"Could not reach the backend API. Is it running? ({e})")

    if "last_result" in st.session_state:
        data = st.session_state["last_result"]
        st.subheader("Detected Themes")
        st.write(", ".join(f"`{t}`" for t in data["themes"]))

        st.subheader("Conversation Starters")
        for idx, starter in enumerate(data["starters"]):
            st.markdown(f"**{idx + 1}.** {starter}")
            col1, col2, _ = st.columns([1, 1, 6])
            if col1.button("👍", key=f"up_{data['history_id']}_{idx}"):
                requests.post(f"{API_BASE}/feedback", json={
                    "history_id": data["history_id"], "starter_index": idx, "useful": True,
                })
                st.toast("Marked as useful!")
            if col2.button("👎", key=f"down_{data['history_id']}_{idx}"):
                requests.post(f"{API_BASE}/feedback", json={
                    "history_id": data["history_id"], "starter_index": idx, "useful": False,
                })
                st.toast("Feedback recorded.")

# ---------------------------------------------------------------------------
# Tab 2: Fact check
# ---------------------------------------------------------------------------
with tab_factcheck:
    query = st.text_input("Quick fact check", placeholder="e.g. blockchain in healthcare")
    if st.button("Check Fact"):
        if not query.strip():
            st.warning("Enter something to look up.")
        else:
            with st.spinner("Searching Wikipedia..."):
                try:
                    resp = requests.post(f"{API_BASE}/fact-check", json={"query": query}, timeout=30)
                    resp.raise_for_status()
                    result = resp.json()
                    if result["found"]:
                        st.success(result["summary"])
                        st.markdown(f"[Read more]({result['source_url']})")
                    else:
                        st.info(result["summary"])
                except requests.exceptions.RequestException as e:
                    st.error(f"Could not reach the backend API. Is it running? ({e})")

# ---------------------------------------------------------------------------
# Tab 3: History
# ---------------------------------------------------------------------------
with tab_history:
    if st.button("Refresh History"):
        st.session_state.pop("history_data", None)

    if "history_data" not in st.session_state:
        try:
            resp = requests.get(f"{API_BASE}/history", timeout=30)
            resp.raise_for_status()
            st.session_state["history_data"] = resp.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Could not reach the backend API. Is it running? ({e})")
            st.session_state["history_data"] = []

    history = st.session_state.get("history_data", [])
    if not history:
        st.info("No conversations generated yet. Try the Generate tab first.")
    else:
        for entry in history:
            with st.expander(f"{entry['timestamp']} — {entry['event_description'][:50]}"):
                st.write("**Interests:**", ", ".join(entry["interests"]) or "—")
                st.write("**Themes:**", ", ".join(entry["themes"]))
                st.write("**Starters:**")
                for i, s in enumerate(entry["starters"], 1):
                    st.write(f"{i}. {s}")
