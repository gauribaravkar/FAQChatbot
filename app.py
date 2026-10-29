import streamlit as st
from chatbot import find_best_answer

st.set_page_config(
    page_title="CustomerCare AI",
    page_icon="💬",
    layout="centered"
)

# Custom styling
st.markdown("""
<style>
    .block-container {
        max-width: 760px;
        padding-top: 2rem;
    }

    .header {
        background: linear-gradient(120deg, #173b72, #3875d7);
        color: white;
        padding: 25px;
        border-radius: 16px;
        margin-bottom: 20px;
    }

    .header h1 {
        color: white;
        margin: 0;
        font-size: 30px;
    }

    .header p {
        color: #e7efff;
        margin: 6px 0 0;
    }

    /* Suggested question buttons */
    div.stButton > button {
        border-radius: 10px;
        min-height: 58px;
        text-align: left;
        border: 1px solid #c7dcff;
        background-color: #eaf2ff !important;
        color: #173b72 !important;
        font-size: 14px;
        font-weight: 500;
        padding: 10px 14px;
    }

    div.stButton > button p {
        color: #173b72 !important;
    }

    div.stButton > button:hover {
        background-color: #d6e6ff !important;
        border-color: #3875d7 !important;
        color: #173b72 !important;
    }

    [data-testid="stChatMessage"] {
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header">
    <h1>💬 CustomerCare AI</h1>
    <p>Your friendly customer support assistant</p>
</div>
""", unsafe_allow_html=True)

# Initialize chat history WITHOUT a repeated welcome message
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show welcome message only once, above the suggestions
st.markdown("### Hello! 👋 How can I help you today?")

# Suggested questions
suggestions = [
    "📦 How can I track my order?",
    "🚚 How long does delivery take?",
    "💳 How do I request a refund?",
    "↩️ How can I cancel my order?"
]

# Display suggestions in two columns
for start in range(0, len(suggestions), 2):
    col1, col2 = st.columns(2)

    for offset, col in enumerate([col1, col2]):
        index = start + offset

        if index < len(suggestions):
            with col:
                if st.button(
                    suggestions[index],
                    key=f"suggestion_{index}",
                    use_container_width=True
                ):
                    st.session_state.pending_question = (
                        suggestions[index].split(" ", 1)[1]
                    )
                    st.rerun()

# Display conversation
for message in st.session_state.messages:
    with st.chat_message(
        message["role"],
        avatar="🤖" if message["role"] == "assistant" else "👤"
    ):
        st.markdown(message["content"])

# Chat input
typed_question = st.chat_input("Type your question here...")

question = typed_question

if not question and "pending_question" in st.session_state:
    question = st.session_state.pop("pending_question")

# Generate response
if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    try:
        result = find_best_answer(question)
        answer = result.get(
            "answer",
            "Sorry, I couldn't find a suitable answer. Please try another question."
        )
    except Exception:
        answer = "Sorry, something went wrong. Please try again."

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    st.rerun()
