
import json
import re
from pathlib import Path

import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Download NLTK stopwords if they are not already installed
def prepare_nltk():
    try:
        stopwords.words("english")
    except LookupError:
        nltk.download("stopwords", quiet=True)


prepare_nltk()
STOP_WORDS = set(stopwords.words("english"))


# Handle greetings and short conversational messages

SIMPLE_REPLIES = {
    "hi": "Hello! 👋 How can I help you today?",
    "hii": "Hello! 👋 How can I help you today?",
    "hiii": "Hello! 👋 How can I help you today?",
    "hello": "Hello! 👋 Welcome to CustomerCare AI. What can I help you with?",
    "hey": "Hey! 😊 What can I help you with today?",
    "heyy": "Hey! 😊 What can I help you with today?",
    "ok": "Alright! 😊 Do you have another customer support question?",
    "okay": "Alright! 😊 Do you have another customer support question?",
    "thanks": "You're welcome! 😊 I'm happy to help.",
    "thank you": "You're welcome! 😊 I'm happy to help.",
    "thankyou": "You're welcome! 😊 I'm happy to help.",
    "bye": "Goodbye! 👋 Thank you for chatting with CustomerCare AI.",
    "good morning": "Good morning! ☀️ How can I help you?",
    "good afternoon": "Good afternoon! 😊 How can I help you?",
    "good evening": "Good evening! 😊 How can I help you?"
}



# Clean and preprocess customer questions
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    words = text.split()

    words = [
        word for word in words
        if word not in STOP_WORDS
    ]

    return " ".join(words)


# Load FAQ questions and answers
def load_faqs():
    file_path = Path(__file__).with_name("faq_data.json")

    if not file_path.exists():
        raise FileNotFoundError(
            "faq_data.json was not found. "
            "Please save it in the same folder as chatbot.py."
        )

    with file_path.open("r", encoding="utf-8") as file:
        faqs = json.load(file)

    if not isinstance(faqs, list) or not faqs:
        raise ValueError(
            "faq_data.json must contain a non-empty list of FAQs."
        )

    for faq in faqs:
        if not isinstance(faq, dict) or not faq.get("question") or not faq.get("answer"):
            raise ValueError(
                "Every FAQ must contain a question and an answer."
            )

    return faqs


# Find the most similar FAQ answer
def find_best_answer(user_question, threshold=0.20):
    question = user_question.strip()

    if not question:
        return {
            "answer": "Please enter a question.",
            "matched_question": None,
            "score": 0.0,
            "found": False,
        }

    # Normalize the question for conversational matching
    normalized_question = question.lower()
    normalized_question = re.sub(
        r"[.!?,]+$", "", normalized_question
    ).strip()
    normalized_question = re.sub(
        r"\s+", " ", normalized_question
    )

    # Reply directly to greetings and short messages
    if normalized_question in SIMPLE_REPLIES:
        return {
            "answer": SIMPLE_REPLIES[normalized_question],
            "matched_question": None,
            "score": 1.0,
            "found": True,
        }

    # Load customer FAQs
    faqs = load_faqs()

    faq_questions = [
        faq["question"] for faq in faqs
    ]

    processed_questions = [
        preprocess_text(faq_question)
        for faq_question in faq_questions
    ]

    processed_user_question = preprocess_text(question)

    if not processed_user_question:
        return {
            "answer": (
                "I'm sorry, I couldn't understand that. "
                "Please ask a customer support question."
            ),
            "matched_question": None,
            "score": 0.0,
            "found": False,
        }

    # Convert FAQ questions into TF-IDF vectors
    vectorizer = TfidfVectorizer()
    all_questions = processed_questions + [
        processed_user_question
    ]

    try:
        vectors = vectorizer.fit_transform(all_questions)
    except ValueError:
        return {
            "answer": (
                "Sorry, I couldn't understand that question. "
                "Please try asking in a different way."
            ),
            "matched_question": None,
            "score": 0.0,
            "found": False,
        }

    faq_vectors = vectors[:-1]
    user_vector = vectors[-1]

    # Calculate similarity using cosine similarity
    scores = cosine_similarity(
        user_vector, faq_vectors
    ).flatten()

    best_index = scores.argmax()
    best_score = float(scores[best_index])

    # Avoid returning an unrelated FAQ answer
    if best_score < threshold:
        return {
            "answer": (
                "Sorry, I couldn't find a suitable answer. "
                "Please try asking in a different way, "
                "or contact customer support for further help."
            ),
            "matched_question": None,
            "score": best_score,
            "found": False,
        }

    # Return the best matching answer
    return {
        "answer": faqs[best_index]["answer"],
        "matched_question": faq_questions[best_index],
        "score": best_score,
        "found": True,
    }
