import streamlit as st
import json

st.set_page_config(page_title="TVP AI Concierge", layout="centered")

st.title("TVP AI Concierge")
st.caption("Luxury client inquiry assistant with LU sales structure")

# ---------------------------
# SESSION STATE (FIXED CLEAR)
# ---------------------------
if "client_message" not in st.session_state:
    st.session_state.client_message = ""

if "analysis" not in st.session_state:
    st.session_state.analysis = None


# ---------------------------
# INPUT
# ---------------------------
client_input = st.text_area(
    "Paste client inquiry",
    value=st.session_state.client_message,
    height=150
)

col1, col2 = st.columns(2)

# ---------------------------
# GENERATE RESPONSE
# ---------------------------
with col1:
    if st.button("Generate response"):
        if client_input.strip() == "":
            st.warning("Please paste a client message.")
        else:
            st.session_state.client_message = client_input

            msg = client_input.lower()

            # ---------------------------
            # ANALYSIS ENGINE (LU STYLE)
            # ---------------------------
            objections = []
            emotion = "curious but undecided"
            booking_score = 5
            lu_stage = "consideration"

            if "husband" in msg or "spouse" in msg:
                objections.append("spouse")
                lu_stage = "objection"
                booking_score = 4

            if "budget" in msg or "price" in msg or "cost" in msg:
                objections.append("price")
                lu_stage = "objection"
                booking_score = 5

            if "looking at other photographers" in msg:
                lu_stage = "consideration"

            if "how do i book" in msg or "how does this work" in msg:
                lu_stage = "decision"
                booking_score = 7

            # ---------------------------
            # RESPONSE LOGIC (LUXURY TONE)
            # ---------------------------
            if "spouse" in objections:
                response = (
                    "Of course—that makes complete sense. This is something meaningful, and I would want you both to feel completely confident moving forward.\n\n"
                    "I can send over a simple overview so you can share it, and then once you’ve had a chance to talk it through, we can reconnect.\n\n"
                    "From there, I’d be happy to guide you both through what the experience would look like and help you decide if it feels like the right fit for your family."
                )

            elif "price" in objections:
                response = (
                    "I completely understand—and I’m really glad you reached out. Most people feel that way at first because this experience is a little different than a typical photo session.\n\n"
                    "Everything is designed to be guided and intentional, so you’re not trying to figure it all out ahead of time.\n\n"
                    "The best next step is a simple conversation where I can walk you through how everything works and help you see what would feel right for you."
                )

            elif lu_stage == "decision":
                response = (
                    "I’m so glad you reached out—this is exactly where most clients begin.\n\n"
                    "The next step is a quick, relaxed conversation where I can learn what you’re envisioning and walk you through how everything works.\n\n"
                    "From there, we can design something that feels truly meaningful and aligned with what you’re wanting."
                )

            else:
                response = (
                    "I’m so glad you reached out. A lot of my clients begin exactly here—wanting to understand what the experience feels like before making any decisions.\n\n"
                    "I’d love to learn what you’re envisioning and walk you through how everything works so you can see if it feels like the right fit.\n\n"
                    "From there, we can take the next step together in a way that feels natural and aligned with what you’re wanting."
                )

            # ---------------------------
            # STORE ANALYSIS
            # ---------------------------
            st.session_state.analysis = {
                "booking_score": booking_score,
                "emotion": emotion,
                "objections": objections,
                "lu_stage": lu_stage,
                "response": response,
                "emotional_driver": "confidence and guidance",
                "next_step": "guide into conversation"
            }


# ---------------------------
# CLEAR BUTTON (FIXED)
# ---------------------------
with col2:
    if st.button("Clear"):
        st.session_state.client_message = ""
        st.session_state.analysis = None
        st.rerun()


# ---------------------------
# OUTPUT
# ---------------------------
if st.session_state.analysis:

    analysis = st.session_state.analysis

    st.markdown("## Analysis")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Booking Score", f"{analysis['booking_score']}/10")
    c2.metric("Emotion", analysis["emotion"])
    c3.metric("Objections", ", ".join(analysis["objections"]) if analysis["objections"] else "None")
    c4.metric("LU Stage", analysis["lu_stage"])

    st.markdown("**Emotional driver**")
    st.write(analysis["emotional_driver"])

    st.markdown("**Recommended next step**")
    st.write(analysis["next_step"])

    # ---------------------------
    # CLIENT RESPONSE
    # ---------------------------
    st.markdown("## Client response")

    response_text = st.text_area(
        "Response (editable)",
        value=analysis["response"],
        height=220
    )

    # ---------------------------
    # COPY BUTTON (WORKING)
    # ---------------------------
    st.markdown(
        f"""
        <button onclick="navigator.clipboard.writeText(`{response_text}`)" 
        style="
            background-color:black;
            color:white;
            padding:12px 18px;
            border:none;
            border-radius:8px;
            font-size:16px;
            cursor:pointer;
            margin-top:10px;">
        📋 Copy Response
        </button>
        """,
        unsafe_allow_html=True
    )

    # Optional visible plain text block
    st.code(response_text)
