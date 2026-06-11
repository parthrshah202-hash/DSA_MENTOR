import streamlit as st
from typing import Dict

from gemini import analyze_code


def init_session_state() -> None:
    """Initialize required Streamlit session state keys."""
    if "show_hint2" not in st.session_state:
        st.session_state["show_hint2"] = False
    if "feedback" not in st.session_state:
        st.session_state["feedback"] = {"hint_1": {"up": 0, "down": 0}, "hint_2": {"up": 0, "down": 0}}
    if "result" not in st.session_state:
        st.session_state["result"] = None


def render_result(result: Dict[str, str]) -> None:
    """Render the analysis result dict into the Streamlit UI."""
    if not result:
        return
    errs = [v for v in result.values() if isinstance(v, str) and v.startswith("ERROR:")]
    if errs and len(errs) == len(result):
        st.error("Analysis failed: " + errs[0].replace("ERROR:", "").strip())
        return

    def safe_get(key: str, default: str = "-") -> str:
        val = result.get(key, default)
        if isinstance(val, str) and val.startswith("ERROR:"):
            return "Unavailable — try analyzing again"
        return val

    # Topic badge + bug detection status
    with st.container(border=True):
        topic = safe_get("topic_badge", "-")
        st.markdown(f"<div style='display:inline-block;padding:6px 10px;border-radius:999px;background:#eef6ff;color:#0366d6;font-weight:600'>{topic}</div>", unsafe_allow_html=True)
        bug_detected = safe_get('bug_detected', 'none').lower()
        if "no" in bug_detected or "none" in bug_detected:
            st.success("✅ No bugs detected — nice work!")
        else:
            st.warning(f"🐛 Bug detected: {safe_get('bug_detected','none')}")

    # Hints section - only render when bug is detected
    bug_detected = safe_get('bug_detected', 'none').lower()
    if not ("no" in bug_detected or "none" in bug_detected):
        with st.container(border=True):
            st.subheader("Hints")
            st.write("**Hint 1:**")
            st.write(safe_get("hint_1", ""))
            c1, c2 = st.columns(2)
            if c1.button("👍", key="h1_up"):
                st.session_state["feedback"]["hint_1"]["up"] += 1
            if c2.button("👎", key="h1_down"):
                st.session_state["feedback"]["hint_1"]["down"] += 1

            if not st.session_state["show_hint2"]:
                if st.button("Show Hint 2"):
                    st.session_state["show_hint2"] = True
            else:
                st.write("**Hint 2:**")
                st.write(safe_get("hint_2", ""))
                c3, c4 = st.columns(2)
                if c3.button("👍", key="h2_up"):
                    st.session_state["feedback"]["hint_2"]["up"] += 1
                if c4.button("👎", key="h2_down"):
                    st.session_state["feedback"]["hint_2"]["down"] += 1

    # Complexity metrics
    with st.container(border=True):
        tcol, scol = st.columns(2)
        tcol.metric("Time", safe_get("time_complexity", "-"))
        scol.metric("Space", safe_get("space_complexity", "-"))


def main() -> None:
    """Main Streamlit app entrypoint."""
    st.set_page_config(page_title="AI Coding Mentor", page_icon="🧠", layout="centered")
    st.title("AI Coding Mentor — DSA Hint Engine")
    st.caption("Get Socratic hints for your DSA bugs — without spoiling the solution.")
    st.divider()
    init_session_state()

    with st.sidebar:
        st.header("How it works")
        st.markdown("""
1. Paste your problem statement and code
2. AI analyzes for bugs and tags the topic
3. Get progressive hints — Hint 2 only unlocks after reviewing Hint 1
        """)
        st.divider()
        st.caption("Built for Microsoft AI Skills Fest — Agents League Hackathon")

    left_col, right_col = st.columns(2)
    problem = left_col.text_area("Problem statement", height=160)
    code = right_col.text_area("Your code (will be sent to the analyzer but not shown back)", height=220)
    language = st.selectbox("Language", ["Python", "C++", "Java", "JavaScript"], index=0)

    if st.button("Analyze"):
        if problem.strip() == "" or code.strip() == "":
            st.warning("Please enter both a problem statement and your code before analyzing.")
            st.stop()
        st.session_state["show_hint2"] = False
        try:
            with st.spinner("Analyzing your code..."):
                res = analyze_code(problem, code, language)
        except Exception as e:
            res = {k: f"ERROR: {str(e)}" for k in [
                "topic_badge",
                "bug_detected",
                "hint_1",
                "hint_2",
                "time_complexity",
                "space_complexity",
            ]}
        st.session_state["result"] = res
        # Celebrate when no bug detected
        bug = res.get("bug_detected", "").lower()
        if "no" in bug or "none" in bug:
            st.balloons()

    render_result(st.session_state.get("result"))


if __name__ == "__main__":
    main()
