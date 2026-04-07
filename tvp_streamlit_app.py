import streamlit as st
import random

st.set_page_config(layout="wide")

# =========================
# SESSION STATE INIT
# =========================
if "client_message" not in st.session_state:
    st.session_state.client_message = ""

if "response_text" not in st.session_state:
    st.session_state.response_text = ""

# =========================
# HEADER
# =========================
st.markdown("### TEXAS VOGUE INTERNAL TOOL")
st.title("TVP AI Concierge")
st.caption("Luxury client inquiry + sales conversation system (LU integrated)")

# =========================
# MODE SELECTOR
# =========================
mode = st.selectbox(
    "Conversation Mode",
    [
        "Inquiry Reply",
        "Discovery Call",
        "Consult / Sales Call",
        "Objection Handling",
        "Closing",
        "Follow-Up"
    ]
)

# =========================
# INPUT
# =========================
client_input = st.text_area(
    "CLIENT MESSAGE",
    key="client_message",
    height=120
)

# =========================
# ANALYSIS ENGINE
# =========================
def analyze_message(msg):
    msg_lower = msg.lower()

    objections = []
    stage = "Inquiry"
    emotion = "curious"
    driver = "clarity and connection"
    booking_score = 5

    # Objection detection
    if "husband" in msg_lower or "spouse" in msg_lower:
        objections.append("spouse")
        stage = "Objection"
        driver = "shared confidence"
        booking_score = 4

    if "budget" in msg_lower or "price" in msg_lower:
        objections.append("price")
        stage = "Objection"
        driver = "value reassurance"
        booking_score = 5

    if "how do i book" in msg_lower or "get booked" in msg_lower:
        stage = "Ready"
        driver = "momentum"
        booking_score = 8

    return {
        "booking_score": booking_score,
        "emotion": emotion,
        "objections": objections if objections else ["None"],
        "stage": stage,
        "driver": driver
    }

# =========================
# RESPONSE GENERATOR
# =========================
def generate_outputs(msg, analysis, mode):

    stage = analysis["stage"]
    driver = analysis["driver"]

    # =========================
    # CORE RESPONSE (LUXURY TONE)
    # =========================
    if stage == "Objection" and "spouse" in analysis["objections"]:
        response = (
            "Of course—that makes complete sense. This is something meaningful, and I would want you both to feel completely confident moving forward.\n\n"
            "What I can do is share a simple overview of how everything works so it’s easy to talk through together, and then we can reconnect once you’ve had a chance to explore what feels right for both of you.\n\n"
            "From there, I’d be happy to guide you through what the experience could look like and help you decide if it feels like the right fit."
        )

    elif stage == "Ready":
        response = (
            "I love that—and I’m so glad you reached out.\n\n"
            "The next step is very simple. We begin with a short conversation where I learn what you’re envisioning and guide you through how everything works so it feels clear and easy.\n\n"
            "From there, we’ll design your session together and reserve a date that feels perfect for you."
        )

    else:
        response = (
            "I’m so glad you reached out. Many of my clients begin exactly here—wanting to understand what the experience feels like before making any decisions.\n\n"
            "I’d love to learn more about what you’re envisioning and walk you through how everything works so you have a clear sense of what this could look like for you.\n\n"
            "From there, I can guide you through the next steps in a way that feels thoughtful, easy, and fully tailored to what you’re wanting."
        )

    # =========================
    # MODE-BASED OUTPUTS
    # =========================

    if mode == "Discovery Call":
        next_step = "Guide conversation deeper"
        question = "What about this season feels most important to capture right now?"
        listen_for = "emotional urgency, children growing, desire for meaning"
        value_bridge = "That’s exactly why I create this as a guided experience—so it becomes something lasting, not just a quick photo session."
        avoid = "jumping into pricing too early"

    elif mode == "Consult / Sales Call":
        next_step = "Position experience"
        question = "Where do you imagine displaying your portraits in your home?"
        listen_for = "wall art, legacy, emotional investment"
        value_bridge = "Everything is designed to become artwork you live with every day—not something that sits on a phone."
        avoid = "over-explaining packages"

    elif mode == "Objection Handling":
        next_step = "Stabilize + guide"
        question = "What would help you feel most confident moving forward?"
        listen_for = "fear, hesitation, hidden objections"
        value_bridge = "My role is to guide you so it feels clear and aligned—not overwhelming."
        avoid = "defensiveness or discounting"

    elif mode == "Closing":
        next_step = "Move toward decision"
        question = "Would you like me to reserve one of the upcoming dates for you?"
        listen_for = "readiness signals"
        value_bridge = "We can always refine details, but reserving your date ensures we hold space for you."
        avoid = "pressure language"

    elif mode == "Follow-Up":
        next_step = "Reopen loop"
        question = None
        listen_for = None
        value_bridge = None
        avoid = None

    else:
        next_step = "Invite conversation"
        question = "Can you tell me a little about who this is for and what you’re hoping to create?"
        listen_for = "intent and emotional driver"
        value_bridge = "I guide everything so you don’t have to figure it out alone."
        avoid = "generic responses"

    return {
        "response": response,
        "next_step": next_step,
        "question": question,
        "listen_for": listen_for,
        "value_bridge": value_bridge,
        "avoid": avoid
    }

# =========================
# BUTTONS
# =========================
col1, col2 = st.columns(2)

with col1:
    if st.button("Generate reply"):
        if client_input.strip():
            analysis = analyze_message(client_input)
            outputs = generate_outputs(client_input, analysis, mode)

            st.session_state.response_text = outputs["response"]
            st.session_state.analysis = analysis
            st.session_state.outputs = outputs

with col2:
    if st.button("Clear"):
        st.session_state.client_message = ""
        st.session_state.response_text = ""
        st.session_state.analysis = {}
        st.session_state.outputs = {}
        st.rerun()

# =========================
# DISPLAY
# =========================
if "analysis" in st.session_state and st.session_state.analysis:

    a = st.session_state.analysis
    o = st.session_state.outputs

    st.markdown("---")
    st.header("Client Insight")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Booking Score", f"{a['booking_score']}/10")
    col2.metric("Emotion", a["emotion"])
    col3.metric("Objections", ", ".join(a["objections"]))
    col4.metric("Stage", a["stage"])

    st.markdown("### Emotional Driver")
    st.write(a["driver"])

    st.markdown("### Best Next Move")
    st.write(f"**Direction:** {o['next_step']}")

    if o["question"]:
        st.write(f"**Ask Next:** {o['question']}")

    if o["listen_for"]:
        st.write(f"**Listen For:** {o['listen_for']}")

    if o["value_bridge"]:
        st.write(f"**Value Bridge:** {o['value_bridge']}")

    if o["avoid"]:
        st.write(f"**Avoid:** {o['avoid']}")

    st.markdown("---")
    st.header("Suggested Reply")

    st.text_area(
        "Editable response",
        value=st.session_state.response_text,
        height=220
    )

    st.code(st.session_state.response_text)

    if st.button("Copy Reply"):
        st.toast("Copied!")

    st.download_button(
        "Download reply",
        data=st.session_state.response_text,
        file_name="tvp_response.txt"
    )

# =========================
# TEST PANEL (SIDEBAR)
# =========================
st.sidebar.title("Testing Panel")

scenarios = {
    "Inquiry": [
        "I love your work, can you tell me more?",
        "How does this process work?"
    ],
    "Spouse": [
        "I need to talk to my husband first",
        "I want to do this but my partner needs to be on board"
    ],
    "Price": [
        "I’m worried about budget",
        "How much does this cost?"
    ],
    "Ready": [
        "How do I book?",
        "I’m ready to schedule"
    ]
}

group = st.sidebar.selectbox("Scenario group", list(scenarios.keys()))
sample = st.sidebar.selectbox("Choose sample", scenarios[group])

if st.sidebar.button("Load selected"):
    st.session_state.client_message = sample
    st.rerun()

if st.sidebar.button("Randomize"):
    st.session_state.client_message = random.choice(scenarios[group])
    st.rerun()
