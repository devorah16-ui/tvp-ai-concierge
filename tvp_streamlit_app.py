import json
import streamlit as st

st.set_page_config(page_title="TVP AI Concierge", page_icon="✨", layout="centered")


def detect_emotional_state(message: str) -> str:
    msg = message.lower()

    if any(word in msg for word in ["nervous", "scared", "unsure", "afraid", "worried"]):
        if any(word in msg for word in ["excited", "love", "dream", "always wanted"]):
            return "nervous yet excited"
        return "uncertain or hesitant"

    if any(word in msg for word in ["overwhelmed", "busy", "stressed", "a lot right now"]):
        return "overwhelmed"

    if any(word in msg for word in ["love your work", "beautiful", "amazing", "obsessed"]):
        return "high interest"

    if any(word in msg for word in ["just looking", "getting info", "curious", "just wanted to ask"]):
        return "interested but cautious"

    return "curious but undecided"



def detect_objections(message: str) -> list[str]:
    msg = message.lower()
    objections = []

    price_patterns = [
        "cost", "pricing", "price", "afford", "expensive", "how much", "budget", "worth it"
    ]
    spouse_patterns = [
        "husband", "spouse", "partner", "talk to my husband", "talk to my wife", "need to ask"
    ]
    timing_patterns = [
        "busy", "timing", "not right now", "maybe later", "schedule", "crazy right now"
    ]
    overwhelm_patterns = [
        "overwhelmed", "don't know what to expect", "nervous", "stress", "figure it all out"
    ]
    mini_patterns = [
        "mini", "cheaper", "less expensive", "anything smaller"
    ]

    if any(p in msg for p in price_patterns):
        objections.append("price")
    if any(p in msg for p in spouse_patterns):
        objections.append("spouse")
    if any(p in msg for p in timing_patterns):
        objections.append("timing")
    if any(p in msg for p in overwhelm_patterns):
        objections.append("overwhelm")
    if any(p in msg for p in mini_patterns):
        objections.append("mini_session")

    return objections



def estimate_booking_likelihood(message: str, emotional_state: str, objections: list[str]) -> int:
    score = 5
    msg = message.lower()

    positive_signals = [
        "love your work", "always wanted", "i want to book", "interested",
        "i've been following", "beautiful", "obsessed", "would love"
    ]

    for signal in positive_signals:
        if signal in msg:
            score += 1

    if emotional_state == "high interest":
        score += 1
    if emotional_state == "nervous yet excited":
        score += 1

    for objection in objections:
        if objection in {"price", "spouse", "timing", "overwhelm"}:
            score -= 1

    return max(1, min(10, score))



def choose_strategy(emotional_state: str, objections: list[str], booking_likelihood: int) -> str:
    if "spouse" in objections:
        return "validate decision, keep connection warm"
    if "price" in objections:
        return "reassure value, guide conversation"
    if "timing" in objections:
        return "reduce pressure, offer future planning"
    if "overwhelm" in objections:
        return "calm and simplify"
    if emotional_state == "high interest" and booking_likelihood >= 7:
        return "encourage and guide next step"
    return "reassure and guide"



def generate_response(message: str, emotional_state: str, objections: list[str]) -> str:
    msg = message.lower()

    if "spouse" in objections:
        response = (
            "Of course—that makes complete sense. This is something meaningful, and I would want you both "
            "to feel really good about it.\n\n"
            "What I can do is send over a simple overview so you can share it, and then we can reconnect "
            "once you’ve had a chance to talk.\n\n"
            "And if it’s helpful, I’m always happy to answer any questions or even chat with both of you."
        )
    elif "price" in objections:
        response = (
            "I completely understand—and I’m really glad you reached out. Most people feel that way at first because "
            "this is a little different than a typical photo session.\n\n"
            "What I create is a guided portrait experience, and most clients choose the artwork and images that matter most "
            "to them after we’ve planned everything together.\n\n"
            "Rather than trying to fit it into a quick message, I’ve found it’s much more helpful to walk you through it "
            "simply so you can see what feels right for you."
        )
    elif "overwhelm" in objections:
        response = (
            "I completely understand that feeling—and honestly, most of my clients start in that exact place.\n\n"
            "You don’t have to have it all figured out ahead of time. I guide you through everything so it feels easy and natural.\n\n"
            "My goal is for this to feel enjoyable, not stressful."
        )
    elif "what makes" in msg or "difference" in msg:
        response = (
            "That’s a great question—and honestly, it’s an important one.\n\n"
            "What I do is a little different from a typical photo session. I guide you through the entire experience—from styling and wardrobe "
            "to posing and final artwork—so you don’t have to figure anything out on your own.\n\n"
            "The goal isn’t just to take photos, but to create something that feels timeless and meaningful for your family."
        )
    elif emotional_state == "high interest":
        response = (
            "That’s so kind of you to say—thank you.\n\n"
            "You don’t need to know exactly how everything works before reaching out. I guide you through each step so the experience feels easy and relaxed.\n\n"
            "It becomes much more than a photoshoot—it’s something really special."
        )
    else:
        response = (
            "I’m so glad you reached out. A lot of my clients begin exactly here—wanting to understand what the experience feels like "
            "before making any decisions.\n\n"
            "I’d love to learn what you’re envisioning and walk you through how everything works."
        )

    response += (
        "\n\nThe next step would just be a quick, relaxed conversation where I can walk you through everything "
        "and answer any questions—no pressure at all."
    )

    return response



def analyze_client_inquiry(message: str) -> dict:
    emotional_state = detect_emotional_state(message)
    objections = detect_objections(message)
    booking_likelihood = estimate_booking_likelihood(message, emotional_state, objections)
    strategy = choose_strategy(emotional_state, objections, booking_likelihood)
    response_message = generate_response(message, emotional_state, objections)

    return {
        "booking_likelihood": booking_likelihood,
        "emotional_state": emotional_state,
        "objections_detected": objections,
        "strategy": strategy,
        "response_message": response_message,
    }



def clean_input(text: str) -> str:
    text = text.replace("\x00", "")
    return "".join(ch for ch in text if ch.isprintable() or ch in "\n\t")


st.title("TVP AI Concierge")
st.caption("Luxury client inquiry analyzer for Texas Vogue Photography")

with st.sidebar:
    st.subheader("Sample inquiries")
    samples = {
        "Budget concern": "Your work is beautiful but I’m worried it might be out of my budget.",
        "Comparison shopper": "I’m looking at a few photographers right now. What makes your sessions different?",
        "Overwhelmed mom": "This looks beautiful but I’m honestly overwhelmed just thinking about outfits, my kids behaving, and whether I could pull something like this off.",
        "Spouse objection": "I love this but I’d need to talk to my husband first before doing anything.",
    }
    selected = st.selectbox("Load a sample", ["Choose one..."] + list(samples.keys()))
    if selected != "Choose one...":
        st.session_state["client_message"] = samples[selected]

client_message = st.text_area(
    "Paste client inquiry",
    key="client_message",
    height=180,
    placeholder="Paste a DM or inquiry here...",
)

col1, col2 = st.columns([1, 1])
with col1:
    generate = st.button("Generate response", use_container_width=True)
with col2:
    clear = st.button("Clear", use_container_width=True)

if clear:
    st.session_state["client_message"] = ""
    st.rerun()

if generate:
    cleaned_message = clean_input(client_message)

    if not cleaned_message.strip():
        st.warning("Please paste a client inquiry first.")
    else:
        analysis = analyze_client_inquiry(cleaned_message)

        st.subheader("Analysis")
        metric1, metric2, metric3 = st.columns(3)
        metric1.metric("Booking score", f"{analysis['booking_likelihood']}/10")
        metric2.metric("Emotion", analysis["emotional_state"])
        metric3.metric("Objections", ", ".join(analysis["objections_detected"]) if analysis["objections_detected"] else "None")

        with st.expander("View strategy"):
            st.write(analysis["strategy"])
            st.code(json.dumps(analysis, indent=2, ensure_ascii=False), language="json")

        import streamlit.components.v1 as components
        import json
        
        st.subheader("Client response")
        
        response_text = analysis["response_message"]
        st.text_area(
            "Response (editable)",
            value=response_text,
            height=260,
        )
        # Safe copy (handles quotes properly)
        safe_text = json.dumps(response_text)
        
        copy_button_html = f"""
        <button style="
        background-color:#000;
        color:#fff;
        padding:10px 16px;
        border:none;
        border-radius:6px;
        font-size:14px;
        " onclick='navigator.clipboard.writeText({safe_text})'>
        📋 Copy Response
        </button>
        """

components.html(copy_button_html, height=60)

st.code(response_text, language="text")

st.download_button(
    "Download response as .txt",
    data=response_text,
    file_name="tvp_client_response.txt",
    mime="text/plain",
    use_container_width=True,
)

st.markdown("---")
st.markdown("**Next useful upgrades:** Atelier vs Heirloom mode, follow-up message generation, and saved response history.")
