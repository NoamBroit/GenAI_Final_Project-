# streamlit_app/streamlit_main.py

import sys
import os
import streamlit as st
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
load_dotenv()

from app.agents.main_agent import MainAgent

st.title("Python Developer Opportunity Recruiter")
st.write(st.session_state)                              #remove after debug

if "agent" not in st.session_state:
    st.session_state.agent = MainAgent()

if "history" not in st.session_state:
    st.session_state.history = []

if "conversation_ended" not in st.session_state:
    st.session_state.conversation_ended = False

if "scheduling_in_progress" not in st.session_state:
    st.session_state.scheduling_in_progress = False

if "interview_confirmed" not in st.session_state:
    st.session_state.interview_confirmed = False

# ── DEBUG: הצג את ה-action האחרון ──────────────────────────────────────────
if "last_action" in st.session_state:
    st.caption(f"🛠 DEBUG — last action: {st.session_state.last_action} | "  #remove after debug
               f"scheduling_in_progress: {st.session_state.scheduling_in_progress} | "  #remove after debug
               f"interview_confirmed: {st.session_state.interview_confirmed}")  #remove after debug

# ── DEBUG: הצג את ה-action האחרון ──────────────────────────────────────────
if "last_action" in st.session_state:
    st.caption(f"🛠 DEBUG — last action: {st.session_state.last_action} | "
               f"scheduling_in_progress: {st.session_state.scheduling_in_progress} | "
               f"interview_confirmed: {st.session_state.interview_confirmed}")    

for user, bot in st.session_state.history:
    with st.chat_message("user"):
        st.write(user)
    with st.chat_message("assistant"):
        st.write(bot)

if st.session_state.conversation_ended:
    st.error("This conversation has ended.")
    st.chat_input("Conversation ended", disabled=True)

else:
    if prompt := st.chat_input("Type your message here..."):

        result = st.session_state.agent.handle_message(
            st.session_state.history,
            prompt,
            scheduling_in_progress=st.session_state.scheduling_in_progress,
            interview_confirmed=st.session_state.interview_confirmed
        )

                # ── DEBUG: שמור את ה-action לפני rerun ──────────────────────────
        st.session_state.last_action = result["action"]
        st.session_state.history.append((prompt, result["response"])) #remove after debug

       
        #st.session_state.history.append((prompt, result["response"]))

        if result["action"] == "end":
            st.session_state.conversation_ended = True
            st.session_state.scheduling_in_progress = False
            st.session_state.interview_confirmed = False

        elif result["action"] == "schedule":
            st.session_state.scheduling_in_progress = True

        elif result["action"] == "confirmed":
            st.session_state.scheduling_in_progress = False
            st.session_state.interview_confirmed = True

        elif result["action"] == "continue":
            if not st.session_state.scheduling_in_progress:
                st.session_state.scheduling_in_progress = False
            #st.session_state.scheduling_in_progress = False

        st.rerun()
