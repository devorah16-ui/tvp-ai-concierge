import json
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="TVP AI Concierge", page_icon="✨", layout="centered")


# -----------------------------
# PHRASE LIBRARIES
# -----------------------------
BOOKING_INTENT_PHRASES = [
    "love to book",
    "want to book",
    "ready to book",
    "how do i book",
    "how do i go about that",
    "what are the next steps",
    "how can i book",
    "book a session",
    "schedule a session",
    "reserve a session",
    "how do i get started",
]

PRICE_PATTERNS = [
    "cost", "price", "pricing", "budget", "afford", "worth it", "expensive", "how much"
]

SPOUSE_PATTERNS = [
    "husband", "spouse", "partner", "talk to my husband", "talk to my wife", "need to ask"
]

TIMING_PATTERNS = [
    "busy", "timing", "later", "not right now", "crazy right now", "schedule is full"
]

OVERWHELM_PATTERNS = [
    "overwhelmed", "nervous", "stress", "stressed", "don’t know what to expect",
    "don't know what to expect", "not sure what to do"
]

MINI_PATTERNS = [
    "mini", "cheaper", "anything smaller", "something smaller"
]


# -----------------------------
# LOGIC FUNCTIONS
# -----------------------------
def detect_emotional_state(message):
    msg = message.lower()

    if any(phrase in msg for phrase in BOOKING_INTENT_PHRASES):
        return "high interest"

    if any(word in msg for word in ["nervous", "scared", "unsure", "afraid", "worried"]):
        if any(word in msg for word in ["excited", "love", "dream", "always wanted"]):
            return "nervous yet excited"
        return "uncertain or hesitant"

    if any(word in msg for word in ["overwhelmed", "busy", "stressed"]):
        return "overwhelmed"

    if any(word in msg for word in ["love your work", "beautiful", "amazing", "obsessed"]):
        return "high interest"

    if any(word in msg for word in ["just looking", "info", "curious"]):
        return "interested but cautious"

    return "curious but undecided"


def detect_objections(message):
    msg = message.lower()
    objections = []

    if any(p in msg for p in PRICE_PATTERNS):
        objections.append("price")

    if any(p in msg for p in SPOUSE_PATTERNS):
        objections.append("spouse")

    if any(p in msg for p in TIMING_PATTERNS):
        objections.append("timing")

    if any(p in msg for p in OVERWHELM_PATTERNS):
        objections.append("overwhelm")

    if any(p in msg for p in MINI_PATTERNS):
        objections.append("mini_session")

    return objections


def estimate_booking_likelihood(message, emotional_state, objections):
    score = 5
    msg = message.lower()

    if "love your work" in msg:
        score += 2

    if any(phrase in msg for phrase in BOOKING_INTENT_PHRASES):
        score += 3

    if emotional_state in ["high interest", "nervous yet excited"]:
        score += 1

    score -= len(objections)

    return max(1, min(10, score))


def choose_strategy(emotional_state, objections, message):
    msg = message.lower()

    if any(phrase in msg for phrase in BOOKING_INTENT_PHRASES):
        return "guide directly to booking"

    if "price" in objections:
        return "reassure value and guide"
    if "spouse" in objections:
        return "validate and keep warm"
    if "overwhelm" in objections:
        return "simplify and reassure"
    if "timing" in objections:
        return "reduce pressure and plan ahead"

    if emotional_state == "high interest":
        return "encourage and guide next steps"

    return "guide and connect"


def generate_response(message, emotional_state, objections):
    msg = message.lower()

    if any(phrase in msg for phrase in BOOKING_INTENT_PHRASES):
        return (
            "That means so much—thank you. I’d love to create something beautiful for you.\n\n"
            "The next step is simply a conversation so I can learn more about what you’re envisioning, "
            "walk you through the experience, and help you choose the session that feels like the best fit.\n\n"
            "From there, I’ll guide you through reserving your date and planning everything in a way that feels easy, thoughtful, and fully taken care of."
        )

    if "spouse" in objections:
        return (
            "Of course—that makes complete sense. This is something meaningful, and I would want you both to feel really good about it.\n\n"
            "What I can do is send over a simple overview so you can share it, and then we can reconnect once you’ve had a chance to talk it through together.\n\n"
            "If it would be helpful, I’m also happy to answer any questions so everything feels clear and comfortable as you decide what feels right for you both."
        )

    if "price" in objections:
        return (
            "I completely understand—and I’m really glad you reached out. Most people feel that way at first because this is a little different than a typical photo session.\n\n"
            "What I create is a fully guided portrait experience, where everything is thoughtfully planned with you—from styling and wardrobe to how you’ll be photographed—so you don’t have to figure any of it out on your own.\n\n"
            "Most clients don’t choose anything ahead of time. We design everything together in a way that feels natural and aligned with what you’re wanting.\n\n"
            "The next step is simply a conversation so I can learn a little more about you and walk you through what this could look like for you. From there, I’ll guide you every step of the way."
        )

    if "overwhelm" in objections:
        return (
            "I completely understand that feeling—and honestly, many of my clients begin in that exact place.\n\n"
            "That’s why I guide you through each part of the experience, from what to wear to how everything comes together, so it feels calm, easy, and beautifully taken care of.\n\n"
            "You do not need to have everything figured out ahead of time. My role is to help shape it with you in a way that feels natural and enjoyable.\n\n"
            "The next step is simply a conversation so I can learn what you’re hoping for and begin guiding you through it."
        )

    if "timing" in objections:
        return (
            "That makes complete sense—life can feel very full, especially in busy seasons.\n\n"
            "The nice thing is that this can be planned in a really thoughtful way, so it feels intentional rather than rushed. Everything is designed to be guided and taken step by step.\n\n"
            "When the timing feels right, I’d be happy to walk you through what the process would look like and help you choose a date that feels comfortable."
        )

    if "mini_session" in objections:
        return (
            "I do offer a few limited sessions at certain times of year, though most of what I create is a more custom, fully guided portrait experience.\n\n"
            "That is where we’re able to create the more refined, timeless artwork you see throughout my work.\n\n"
            "The next step would be for me to learn a little more about what you’re hoping for so I can guide you toward the option that feels like the best fit."
        )

    if "what makes" in msg or "difference" in msg:
        return (
            "That’s a wonderful question—and honestly, it’s an important one.\n\n"
            "What I do is a little different from a typical photo session. I guide you through the entire experience—from styling and preparation to posing and final artwork—so you don’t have to figure anything out on your own.\n\n"
            "The goal isn’t simply to create beautiful photographs, but to create something lasting, intentional, and meaningful.\n\n"
            "The next step is simply a conversation so I can learn what you’re envisioning and walk you through how the experience would be shaped around you."
        )

    if emotional_state == "high interest":
        return (
            "That means so much—thank you.\n\n"
            "I’d love to learn more about what you’re envisioning and help you choose the session that would feel most aligned with what you want to create.\n\n"
            "Everything is designed to feel easy, thoughtful, and fully guided from beginning to end.\n\n"
            "The next step is simply a conversation so I can walk you through the experience and begin shaping it with you."
        )

    if emotional_state == "nervous yet excited":
        return (
            "I completely understand that feeling—and honestly, that’s such a natural place to begin.\n\n"
            "Most clients come in not knowing exactly how everything will come together yet, and that is completely okay. The experience is designed to be guided, thoughtful, and very personal.\n\n"
            "My role is to help you feel comfortable, cared for, and confident as we plan something beautiful together.\n\n"
            "The next step is simply a conversation so I can learn more about what you’re envisioning and begin guiding you through the process."
        )

    return (
        "I’m so glad you reached out. A lot of my clients begin exactly here—wanting to understand what the experience feels like before making any decisions.\n\n"
        "I’d love to learn more about what you’re envisioning and walk you through how everything works, so you have a clear sense of what this could look like for you.\n\n"
        "From there, I can guide you through the next steps in a way that feels thoughtful, easy, and fully tailored to what you’re wanting."
    )


def analyze_client_inquiry(message):
    emotional_state = detect_emotional_state(message)
    objections = detect_objections(message)
    booking_likelihood = estimate_booking_likelihood(message, emotional_state, objections)
    strategy = choose_strategy(emotional_state, objections, message)
    response_message = generate_response(message, emotional_state, objections)

    return {
        "booking_likelihood": booking_likelihood,
        "emotional_state": emotional_state,
        "objections_detected": objections,
        "strategy": strategy,
        "response_message": response_message,
    }


# -----------------------------
# SESSION STATE
# -----------------------------
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

if "analysis" not in st.session_state:
    st.session_state.analysis = None


# -----------------------------
# CALLBACKS
# -----------------------------
def clear_all():
    st.session_state.input_text = ""
    st.session_state.analysis = None


# -----------------------------
# UI
# -----------------------------
st.title("TVP AI Concierge")
st.caption("Luxury client inquiry assistant")

with st.sidebar:
    st.subheader("Sample inquiries")
    samples = {
        "Ready to book": "One of my friends did images with you and I love how they came out. I would love to book a session. How do I go about that?",
        "Budget concern": "Your work is beautiful but I’m worried it might be out of my budget.",
        "Spouse objection": "I love this but I’d need to talk to my husband first before doing anything.",
        "Overwhelmed mom": "This looks beautiful but I’m honestly overwhelmed just thinking about outfits, my kids behaving, and whether I could pull something like this off.",
        "Comparison shopper": "I’m looking at a few photographers right now. What makes your sessions different?",
    }

    selected = st.selectbox("Load a sample", ["Choose one..."] + list(samples.keys()))
    if selected != "Choose one...":
        st.session_state.input_text = samples[selected]

client_message = st.text_area(
    "Paste client inquiry",
    value=st.session_state.input_text,
    height=150,
)

col1, col2 = st.columns(2)
generate = col1.button("Generate response", use_container_width=True)
col2.button("Clear", use_container_width=True, on_click=clear_all)


# -----------------------------
# BUTTON ACTIONS
# -----------------------------
if generate:
    st.session_state.input_text = client_message

    if not client_message.strip():
        st.warning("Please enter a message.")
        st.session_state.analysis = None
    else:
        st.session_state.analysis = analyze_client_inquiry(client_message)


# -----------------------------
# DISPLAY RESULTS
# -----------------------------
if st.session_state.analysis is not None:
    analysis = st.session_state.analysis

    st.subheader("Analysis")
    metric1, metric2, metric3 = st.columns(3)
    metric1.metric("Booking Score", f"{analysis['booking_likelihood']}/10")
    metric2.metric("Emotion", analysis["emotional_state"])
    metric3.metric(
        "Objections",
        ", ".join(analysis["objections_detected"]) if analysis["objections_detected"] else "None"
    )

    with st.expander("View strategy"):
        st.write(analysis["strategy"])
        st.code(json.dumps(analysis, indent=2, ensure_ascii=False), language="json")

    st.subheader("Client response")

    response_text = analysis["response_message"]

    st.text_area(
        "Response (editable)",
        value=response_text,
        height=260,
        key="response_output",
    )

    safe_text = json.dumps(response_text)

    copy_button_html = f"""
    <button style="
        background-color:#000;
        color:#fff;
        padding:10px 16px;
        border:none;
        border-radius:6px;
        font-size:14px;
        cursor:pointer;
    " onclick='navigator.clipboard.writeText({safe_text})'>
        📋 Copy Response
    </button>
    """

    components.html(copy_button_html, height=60)

    st.code(response_text, language="text")

    st.download_button(
        "Download response",
        data=response_text,
        file_name="response.txt",
        use_container_width=True,
    )
