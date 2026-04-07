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
            "The next step is simply a quick conversation so I can learn what you’re envisioning, "
            "walk you through the experience, and help you choose the best session for what you want.\n\n"
            "From there, we’ll get your date reserved and start planning everything out in a really easy, guided way."
        )

    if "spouse" in objections:
        response = (
            "Of course—that makes complete sense. This is something meaningful, and I would want you both to feel really good about it.\n\n"
            "What I can do is send over a simple overview so you can share it, and then we can reconnect once you’ve had a chance to talk.\n\n"
            "And if it’s helpful, I’m always happy to answer any questions or even chat with both of you."
        )

    elif "price" in objections:
        response = (
            "I completely understand—and I’m really glad you reached out. Most people feel that way at first because this is a little different than a typical photo session.\n\n"
            "What I create is a guided portrait experience, and most clients choose the artwork and images that matter most to them after we’ve planned everything together.\n\n"
            "Rather than trying to fit it into a quick message, I’ve found it’s much more helpful to walk you through it simply so you can see what feels right for you."
        )

    elif "overwhelm" in objections:
        response = (
            "I completely understand that feeling—and honestly, most of my clients start in that exact place.\n\n"
            "You don’t have to have it all figured out ahead of time. I guide you through everything so it feels easy and natural.\n\n"
            "My goal is for this to feel enjoyable, not stressful."
        )

    elif "timing" in objections:
        response = (
            "That makes complete sense—life gets busy quickly.\n\n"
            "The nice thing is we can plan this in a really calm, easy way so it fits your schedule and doesn’t feel overwhelming.\n\n"
            "Whenever the timing feels right, I’d be happy to walk you through the next step."
        )

    elif "what makes" in msg or "difference" in msg:
        response = (
            "That’s a great question—and honestly, it’s an important one.\n\n"
            "What I do is a little different from a typical photo session. I guide you through the entire experience—from styling to posing—so you don’t have to figure anything out on your own.\n\n"
            "The goal isn’t just to take photos, but to create something timeless and meaningful."
        )

    elif emotional_state == "high interest":
        response = (
            "That means so much—thank you.\n\n"
            "I’d love to learn more about what you’re envisioning and help you choose the session that fits best.\n\n"
            "Everything is designed to feel easy, guided, and really intentional from start to finish."
        )

    else:
        response = (
            "I’m so glad you reached out. A lot of my clients begin exactly here—wanting to understand what the experience feels like before making any decisions.\n\n"
            "I’d love to learn what you’re envisioning and walk you through how everything works."
        )

    response += "\n\nThe next step would just be a quick, relaxed conversation where I can walk you through everything and answer any questions—no pressure at all."
    return response


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
