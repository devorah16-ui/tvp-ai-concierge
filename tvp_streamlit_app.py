import json
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="TVP AI Concierge", page_icon="✨", layout="centered")


# -----------------------------
# LOGIC FUNCTIONS
# -----------------------------

def detect_emotional_state(message):
    msg = message.lower()

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

    if any(p in msg for p in ["cost", "price", "budget", "afford", "worth it"]):
        objections.append("price")

    if any(p in msg for p in ["husband", "spouse", "partner"]):
        objections.append("spouse")

    if any(p in msg for p in ["busy", "timing", "later"]):
        objections.append("timing")

    if any(p in msg for p in ["overwhelmed", "nervous", "stress"]):
        objections.append("overwhelm")

    if any(p in msg for p in ["mini", "cheaper"]):
        objections.append("mini_session")

    return objections


def estimate_booking_likelihood(message, emotional_state, objections):
    score = 5
    msg = message.lower()

    if "love your work" in msg:
        score += 2

    if emotional_state in ["high interest", "nervous yet excited"]:
        score += 1

    score -= len(objections)

    return max(1, min(10, score))


def choose_strategy(emotional_state, objections):
    if "price" in objections:
        return "reassure value and guide"
    if "spouse" in objections:
        return "validate and keep warm"
    if "overwhelm" in objections:
        return "simplify and reassure"
    return "guide and connect"


def generate_response(message, emotional_state, objections):
    msg = message.lower()

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

    elif "what makes" in msg:
        response = (
            "That’s a great question—and honestly, it’s an important one.\n\n"
            "What I do is a little different from a typical photo session. I guide you through the entire experience—from styling to posing—so you don’t have to figure anything out on your own.\n\n"
            "The goal isn’t just to take photos, but to create something timeless and meaningful."
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
    strategy = choose_strategy(emotional_state, objections)
    response_message = generate_response(message, emotional_state, objections)

    return {
        "booking_likelihood": booking_likelihood,
        "emotional_state": emotional_state,
        "objections_detected": objections,
        "strategy": strategy,
        "response_message": response_message
    }


# -----------------------------
# SESSION STATE
# -----------------------------

if "client_message" not in st.session_state:
    st.session_state.client_message = ""

if "analysis" not in st.session_state:
    st.session_state.analysis = None


# -----------------------------
# UI
# -----------------------------

st.title("TVP AI Concierge")
st.caption("Luxury client inquiry assistant")

client_message = st.text_area(
    "Paste client inquiry",
    key="client_message",
    height=150
)

col1, col2 = st.columns(2)
generate = col1.button("Generate response", use_container_width=True)
clear = col2.button("Clear", use_container_width=True)


# -----------------------------
# BUTTON ACTIONS
# -----------------------------

if clear:
    st.session_state.client_message = ""
    st.session_state.analysis = None
    st.rerun()

if generate:
    if not st.session_state.client_message.strip():
        st.warning("Please enter a message")
    else:
        st.session_state.analysis = analyze_client_inquiry(st.session_state.client_message)


# -----------------------------
# DISPLAY RESULTS
# -----------------------------

if st.session_state.analysis is not None:
    analysis = st.session_state.analysis

    st.subheader("Analysis")
    st.write(f"Booking Score: {analysis['booking_likelihood']}/10")
    st.write(f"Emotion: {analysis['emotional_state']}")
    st.write(f"Objections: {analysis['objections_detected']}")

    st.subheader("Client response")

    response_text = analysis["response_message"]

    st.text_area(
        "Response (editable)",
        value=response_text,
        height=260,
        key="response_output"
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
        use_container_width=True
    )
