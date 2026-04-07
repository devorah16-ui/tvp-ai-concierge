import json
import random
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="TVP AI Concierge", page_icon="✨", layout="centered")


# -----------------------------
# LIGHT STYLING
# -----------------------------
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 980px;
}
.luxury-card {
    padding: 1.25rem 1.4rem;
    border: 1px solid rgba(49, 51, 63, 0.12);
    border-radius: 18px;
    background: rgba(250, 248, 244, 0.70);
    margin-bottom: 1rem;
}
.section-label {
    font-size: 0.9rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    opacity: 0.75;
    margin-bottom: 0.25rem;
}
.big-title {
    font-size: 2.7rem;
    font-weight: 700;
    margin-bottom: 0.2rem;
}
.soft-copy {
    font-size: 1.05rem;
    opacity: 0.82;
}
.subtle-divider {
    margin-top: 0.8rem;
    margin-bottom: 1.2rem;
}
.small-note {
    font-size: 0.95rem;
    opacity: 0.82;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# PHRASE LIBRARIES
# -----------------------------
BOOKING_INTENT_PHRASES = [
    "love to book",
    "want to book",
    "ready to book",
    "how do i book",
    "how do i get booked",
    "how do i go about that",
    "what are the next steps",
    "how can i book",
    "book a session",
    "schedule a session",
    "reserve a session",
    "how do i get started",
    "get booked",
    "get this booked",
    "book with you",
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
# TESTING PANEL DATA
# -----------------------------
TEST_SCENARIOS = {
    "Inquiry": [
        "Hi! I just came across your page and wanted to get some info.",
        "Can you tell me how your sessions work?",
        "Do you have pricing you can send over?",
        "I’m just looking right now but I love your work.",
        "Where are you located and what do you offer?",
        "I’ve never done something like this before—how does it work?",
    ],
    "Discovery": [
        "I’ve always wanted to do something like this but never have.",
        "I love your work—it feels so different than other photographers.",
        "I’ve been thinking about doing portraits with my daughter.",
        "This is beautiful… I just don’t know if I could pull it off.",
        "I want something meaningful but I don’t know what that would look like.",
        "I missed out on photos when my kids were little and I don’t want to regret it again.",
    ],
    "Vision Building": [
        "I’m looking at a few photographers—what makes your sessions different?",
        "Why is your work priced higher than others?",
        "What exactly do you include in your sessions?",
        "Do you help with styling or do I need to figure that out?",
        "What kind of finished products do people usually get?",
        "Are these all done in studio or on location?",
    ],
    "Price Objection": [
        "Your work is beautiful but I’m worried it might be out of my budget.",
        "This feels like it might be expensive…",
        "What do most people spend?",
        "Do you offer anything more affordable?",
        "I love it but I don’t know if I can justify it.",
    ],
    "Spouse Objection": [
        "I need to talk to my husband first.",
        "My spouse would need to be on board.",
        "I’m not sure my partner will understand the value.",
        "Let me run this by my husband.",
        "I love this so much but I would need to talk to my husband first before making a decision.",
    ],
    "Timing Objection": [
        "Things are just really busy right now.",
        "Maybe later this year.",
        "I don’t think now is a good time.",
        "We have a lot going on at the moment.",
        "I’m really interested but things are just really busy for us right now.",
    ],
    "Overwhelm Objection": [
        "This feels like a lot… outfits, kids, everything.",
        "I wouldn’t even know where to start.",
        "My kids don’t sit still—I’m nervous about that.",
        "I’m not comfortable in front of the camera.",
        "This looks beautiful but I’m honestly overwhelmed thinking about outfits, my kids behaving, and whether I could pull something like this off.",
    ],
    "Mini Session": [
        "Do you offer minis?",
        "Is there a smaller version of this?",
        "Do you have anything quick and simple?",
        "Do you offer mini sessions or anything a little more simple?",
    ],
    "Ready to Book": [
        "I would love to book—what are the next steps?",
        "How do I get booked?",
        "Do you have availability in April?",
        "I’m ready to move forward—what do I do next?",
        "Can we get something scheduled?",
        "I want to do this—what does booking look like?",
        "My friend recently did a session with you and I love the print she has in her home. How do I get booked?",
    ],
    "Hybrid / Mixed": [
        "I love your work and would love to do this, I just don’t know if it’s in my budget.",
        "I’m really interested but I need to talk to my husband first.",
        "This is beautiful but I’m honestly overwhelmed thinking about outfits and everything.",
        "I want to do this but I don’t even know where to start.",
        "Hi! I love your work. I’ve been thinking about doing something like this but I’m nervous and also need to talk to my husband lol. Just wanted to get some info.",
    ],
    "Social Proof / Trust": [
        "My friend had photos done with you and I’m obsessed. How do I book?",
        "I saw your work in someone’s home and I need this—how do we start?",
        "You photographed my friend and I’ve been thinking about this ever since.",
        "One of my friends did images with you and I love how they came out. I would love to book a session. How do I go about that?",
    ],
}


# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def has_booking_intent(msg: str) -> bool:
    booking_words = ["book", "booked", "booking", "reserve", "schedule"]
    intent_words = ["how do i", "how can i", "want to", "ready to", "love to", "next steps", "get started"]

    return (
        any(phrase in msg for phrase in BOOKING_INTENT_PHRASES)
        or (any(b in msg for b in booking_words) and any(i in msg for i in intent_words))
    )


# -----------------------------
# DETECTION FUNCTIONS
# -----------------------------
def detect_emotional_state(message: str) -> str:
    msg = message.lower()

    if has_booking_intent(msg):
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


def detect_objections(message: str) -> list[str]:
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


def detect_lu_stage(message: str, objections: list[str]) -> str:
    msg = message.lower()

    if has_booking_intent(msg):
        return "ready_to_book"

    if objections:
        return "objection"

    if "what makes" in msg or "difference" in msg:
        return "vision_building"

    if any(word in msg for word in ["just looking", "info", "how does this work", "can you send"]):
        return "inquiry"

    if any(word in msg for word in [
        "i love your work",
        "i've been following",
        "always wanted",
        "thinking about",
        "interested"
    ]):
        return "discovery"

    return "inquiry"


def detect_emotional_driver(message: str, emotional_state: str, objections: list[str]) -> str:
    msg = message.lower()

    if has_booking_intent(msg):
        return "readiness and trust"

    if "price" in objections:
        return "clarity and reassurance"

    if "spouse" in objections:
        return "shared confidence"

    if "overwhelm" in objections:
        return "guidance and ease"

    if "timing" in objections:
        return "simplicity and flexibility"

    if "mini_session" in objections:
        return "fit and accessibility"

    if "what makes" in msg or "difference" in msg:
        return "confidence in your difference"

    if emotional_state == "nervous yet excited":
        return "confidence and care"

    if emotional_state == "high interest":
        return "beauty, trust, and momentum"

    return "clarity and connection"


def recommend_next_step(lu_stage: str, objections: list[str]) -> str:
    if lu_stage == "ready_to_book":
        return "Invite consultation and reserve date"

    if "price" in objections:
        return "Briefly explain the experience and invite a consult"

    if "spouse" in objections:
        return "Offer an overview they can share and keep the connection warm"

    if "overwhelm" in objections:
        return "Simplify the process and guide with one calm next step"

    if "timing" in objections:
        return "Offer future planning and remove urgency"

    if lu_stage == "vision_building":
        return "Reinforce your difference and invite a conversation"

    if lu_stage == "discovery":
        return "Ask one meaningful discovery question or invite a consult"

    return "Invite a simple conversation"


def estimate_booking_likelihood(
    message: str,
    emotional_state: str,
    objections: list[str],
    lu_stage: str
) -> int:
    score = 5
    msg = message.lower()

    if "love your work" in msg or "love the print" in msg or "love how they came out" in msg:
        score += 2

    if has_booking_intent(msg):
        score += 3

    if "my friend" in msg or "recommended" in msg or "friend recently did a session" in msg:
        score += 1

    if lu_stage == "ready_to_book":
        score += 1

    if emotional_state in ["high interest", "nervous yet excited"]:
        score += 1

    score -= len(objections)

    return max(1, min(10, score))


def choose_strategy(lu_stage: str, emotional_driver: str, recommended_next_step: str) -> str:
    if lu_stage == "ready_to_book":
        return "Move confidently into booking guidance"

    if lu_stage == "objection":
        return f"Address the concern with calm authority, support the client's need for {emotional_driver}, and {recommended_next_step.lower()}"

    if lu_stage == "vision_building":
        return "Differentiate the experience and deepen desire"

    if lu_stage == "discovery":
        return "Build connection and guide toward a meaningful next step"

    return "Create clarity and invite the conversation forward"


def calculate_confidence(message: str, lu_stage: str, objections: list[str], emotional_state: str) -> str:
    msg = message.lower()
    signal_count = 0

    if has_booking_intent(msg):
        signal_count += 2
    if objections:
        signal_count += 1
    if emotional_state in ["high interest", "nervous yet excited", "overwhelmed"]:
        signal_count += 1
    if "my friend" in msg or "recommended" in msg:
        signal_count += 1
    if lu_stage in ["ready_to_book", "objection", "vision_building"]:
        signal_count += 1

    if signal_count >= 4:
        return "High"
    if signal_count >= 2:
        return "Medium"
    return "Low"


def detect_lead_priority(message: str, booking_likelihood: int, lu_stage: str) -> str:
    msg = message.lower()

    if booking_likelihood >= 8 and ("my friend" in msg or "recommended" in msg or lu_stage == "ready_to_book"):
        return "High-touch lead"

    if booking_likelihood >= 7:
        return "Strong lead"

    if lu_stage == "objection":
        return "Nurture lead"

    return "Early-stage lead"


# -----------------------------
# RESPONSE GENERATION
# -----------------------------
def generate_response(
    message: str,
    emotional_state: str,
    objections: list[str],
    lu_stage: str,
    emotional_driver: str
) -> str:
    msg = message.lower()

    if lu_stage == "ready_to_book":
        return (
            "That means so much—thank you. I’d love to create something beautiful for you.\n\n"
            "The next step is simply a conversation so I can learn a little more about what you’re envisioning, "
            "walk you through the experience, and help you choose the session that feels like the best fit.\n\n"
            "From there, I’ll guide you through reserving your date and planning everything in a way that feels easy, thoughtful, and fully taken care of."
        )

    if "spouse" in objections:
        return (
            "Of course—that makes complete sense. This is something meaningful, and I would want you both to feel completely confident moving forward.\n\n"
            "I can send over a simple overview so you can share it, and then once you’ve had a chance to talk it through, we can reconnect.\n\n"
            "From there, I’d be happy to guide you both through what the experience would look like and help you decide if it feels like the right fit for your family."
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

    if lu_stage == "vision_building" or "what makes" in msg or "difference" in msg:
        return (
            "That’s a wonderful question—and honestly, it’s an important one.\n\n"
            "What I do is a little different from a typical photo session. I guide you through the entire experience—from styling and preparation to posing and final artwork—so you don’t have to figure anything out on your own.\n\n"
            "The goal isn’t simply to create beautiful photographs, but to create something lasting, intentional, and meaningful.\n\n"
            "The next step is simply a conversation so I can learn what you’re envisioning and walk you through how the experience would be shaped around you."
        )

    if lu_stage == "discovery":
        return (
            "I’m so glad you reached out. It sounds like this is something that matters to you, and I’d love to learn a little more about what you’re envisioning.\n\n"
            "The experience is designed to be thoughtful and fully guided, so you do not need to have every detail figured out before reaching out.\n\n"
            "The next step is simply a conversation so I can get a sense of what you’re hoping to create and begin guiding you toward what would fit best."
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


def suggest_discovery_question(lu_stage: str, emotional_driver: str, objections: list[str]) -> str:
    if lu_stage == "discovery":
        return "What is it about this season or this moment that makes you want to capture it now?"

    if lu_stage == "vision_building":
        return "What was it about my work that felt most meaningful or most like what you’re wanting?"

    if "price" in objections:
        return "Would it help if I walked you through how the experience works so you could get a clearer sense of what feels right for you?"

    if "overwhelm" in objections:
        return "Would it be helpful if I walked you through the process step by step so it feels simpler?"

    if "spouse" in objections:
        return "Would it help if I sent over a simple overview you could share so you both have a clear sense of how it works?"

    if lu_stage == "ready_to_book":
        return "Would you like me to walk you through the next step and what the booking process looks like?"

    return "Can you tell me a little about who this is for and what you’re hoping to create?"


def generate_follow_up(lu_stage: str, objections: list[str]) -> str:
    if lu_stage == "ready_to_book":
        return (
            "Hi! I just wanted to follow up with you in case you’d like to move forward. "
            "I’d be happy to walk you through the next step and help you find a date that feels right."
        )

    if "spouse" in objections:
        return (
            "Hi! I just wanted to check in and see if you had a chance to talk it through together. "
            "If it would be helpful, I’m happy to walk you through the experience or answer any questions."
        )

    if "price" in objections:
        return (
            "Hi! I just wanted to check in. If it would be helpful, I’d be happy to walk you through how the experience works so you can get a clearer sense of what would feel right for you."
        )

    if "overwhelm" in objections:
        return (
            "Hi! I just wanted to check in. If it would help, I can walk you through everything step by step so it feels simple and easy."
        )

    return (
        "Hi! I just wanted to check back in and see if you had any questions. "
        "I’d be happy to walk you through the experience whenever you’re ready."
    )


def analyze_client_inquiry(message: str) -> dict:
    emotional_state = detect_emotional_state(message)
    objections = detect_objections(message)
    lu_stage = detect_lu_stage(message, objections)
    emotional_driver = detect_emotional_driver(message, emotional_state, objections)
    recommended_next_step = recommend_next_step(lu_stage, objections)
    booking_likelihood = estimate_booking_likelihood(message, emotional_state, objections, lu_stage)
    strategy = choose_strategy(lu_stage, emotional_driver, recommended_next_step)
    response_message = generate_response(message, emotional_state, objections, lu_stage, emotional_driver)
    discovery_question = suggest_discovery_question(lu_stage, emotional_driver, objections)
    follow_up_message = generate_follow_up(lu_stage, objections)
    confidence = calculate_confidence(message, lu_stage, objections, emotional_state)
    lead_priority = detect_lead_priority(message, booking_likelihood, lu_stage)

    return {
        "booking_likelihood": booking_likelihood,
        "emotional_state": emotional_state,
        "objections_detected": objections,
        "lu_stage": lu_stage,
        "emotional_driver": emotional_driver,
        "recommended_next_step": recommended_next_step,
        "strategy": strategy,
        "suggested_discovery_question": discovery_question,
        "follow_up_message": follow_up_message,
        "confidence": confidence,
        "lead_priority": lead_priority,
        "response_message": response_message,
    }


# -----------------------------
# SESSION STATE
# -----------------------------
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "selected_test_category" not in st.session_state:
    st.session_state.selected_test_category = "Inquiry"


# -----------------------------
# CALLBACKS
# -----------------------------
def clear_all():
    st.session_state.input_text = ""
    st.session_state.analysis = None


# -----------------------------
# UI
# -----------------------------
st.markdown('<div class="luxury-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Texas Vogue Internal Tool</div>', unsafe_allow_html=True)
st.markdown('<div class="big-title">TVP AI Concierge</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="soft-copy">Luxury client inquiry assistant with LU sales structure</div>',
    unsafe_allow_html=True
)
st.markdown('</div>', unsafe_allow_html=True)

with st.sidebar:
    st.subheader("Built-In Testing Panel")

    category = st.selectbox(
        "Scenario group",
        list(TEST_SCENARIOS.keys()),
        key="selected_test_category"
    )

    scenario_list = TEST_SCENARIOS[category]
    picked_scenario = st.selectbox("Choose a sample", scenario_list)

    sidebar_col1, sidebar_col2 = st.columns(2)
    if sidebar_col1.button("Load selected", use_container_width=True):
        st.session_state.input_text = picked_scenario
        st.session_state.analysis = None
        st.rerun()

    if sidebar_col2.button("Randomize", use_container_width=True):
        st.session_state.input_text = random.choice(TEST_SCENARIOS[category])
        st.session_state.analysis = None
        st.rerun()

    st.markdown("---")
    st.markdown("**Quick stage samples**")
    quick_samples = {
        "Ready to Book": "My friend recently did a session with you and I love the print she has in her home. How do I get booked?",
        "Price": "Your work is beautiful but I’m worried it might be out of my budget.",
        "Spouse": "I love this so much but I would need to talk to my husband first before making a decision.",
        "Overwhelm": "This looks beautiful but I’m honestly overwhelmed thinking about outfits, my kids behaving, and whether I could pull something like this off.",
    }

    quick_pick = st.radio("Fast load", list(quick_samples.keys()), index=0)
    if st.button("Load quick sample", use_container_width=True):
        st.session_state.input_text = quick_samples[quick_pick]
        st.session_state.analysis = None
        st.rerun()

st.markdown('<div class="section-label">Client Message</div>', unsafe_allow_html=True)
client_message = st.text_area(
    "Paste client inquiry",
    value=st.session_state.input_text,
    height=150,
    label_visibility="collapsed",
    placeholder="Paste a DM or inquiry here..."
)

col1, col2 = st.columns(2)
generate = col1.button("Generate reply", use_container_width=True)
col2.button("Clear", use_container_width=True, on_click=clear_all)

if generate:
    st.session_state.input_text = client_message

    if not client_message.strip():
        st.warning("Please enter a message.")
        st.session_state.analysis = None
    else:
        st.session_state.analysis = analyze_client_inquiry(client_message)

if st.session_state.analysis is not None:
    analysis = st.session_state.analysis

    st.markdown('<div class="subtle-divider"></div>', unsafe_allow_html=True)
    st.markdown("## Client Insight")

    metric1, metric2, metric3, metric4 = st.columns(4)
    metric1.metric("Booking Score", f"{analysis['booking_likelihood']}/10")
    metric2.metric("Emotion", analysis["emotional_state"])
    metric3.metric(
        "Objections",
        ", ".join(analysis["objections_detected"]) if analysis["objections_detected"] else "None"
    )
    metric4.metric("LU Stage", analysis["lu_stage"].replace("_", " ").title())

    metric5, metric6 = st.columns(2)
    metric5.metric("Confidence", analysis["confidence"])
    metric6.metric("Lead Priority", analysis["lead_priority"])

    st.markdown('<div class="luxury-card">', unsafe_allow_html=True)
    st.markdown("**Emotional Driver**")
    st.write(analysis["emotional_driver"])
    st.markdown("**Recommended Next Step**")
    st.write(analysis["recommended_next_step"])
    st.markdown("**Suggested Discovery Question**")
    st.write(analysis["suggested_discovery_question"])
    st.markdown("**Suggested Follow-Up**")
    st.write(analysis["follow_up_message"])
    st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("Concierge Notes"):
        st.write(analysis["strategy"])

    st.markdown("## Suggested Reply")

    response_text = analysis["response_message"]

    st.text_area(
        "Suggested reply text",
        value=response_text,
        height=260,
        key="response_output",
        label_visibility="collapsed",
    )

    safe_text = json.dumps(response_text)

    copy_button_html = f"""
    <button style="
        background-color:#111111;
        color:#ffffff;
        padding:12px 18px;
        border:none;
        border-radius:10px;
        font-size:15px;
        cursor:pointer;
        font-family:inherit;
    " onclick='navigator.clipboard.writeText({safe_text})'>
        Copy Reply
    </button>
    """

    components.html(copy_button_html, height=55)

    st.download_button(
        "Download reply",
        data=response_text,
        file_name="tvp_reply.txt",
        use_container_width=False,
    )
