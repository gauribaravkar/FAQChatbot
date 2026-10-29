
# CustomerCare AI 🤖

CustomerCare AI is a simple FAQ chatbot that helps users find answers to common customer support questions about orders, delivery, payments, cancellations, and refunds.

## Features

- Interactive chatbot built with Streamlit
- Prepared FAQ dataset in JSON format
- Text preprocessing using NLTK
- TF-IDF vectorization for question matching
- Cosine similarity to find the closest FAQ
- Helpful fallback response when a suitable answer is not found
- Clickable suggested questions

## Technologies Used

- Python
- Streamlit
- NLTK
- Scikit-learn
- JSON

## Project Structure

```text
CodeAlpha_FAQChatbot/
├── app.py
├── chatbot.py
├── faq_data.json
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL](https://github.com/gauribaravkar/FAQChatbot.git
cd CodeAlpha_FAQChatbot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## How It Works

1. The user enters a question or clicks a suggested question.
2. The chatbot preprocesses the text.
3. TF-IDF converts FAQ questions and the user's question into numerical vectors.
4. Cosine similarity compares the questions.
5. The chatbot displays the best matching answer when the similarity score meets the configured threshold.


## Example

**User:** How can I track my order?

**CustomerCare AI:** You can track your order using the tracking link sent to your registered email or phone number.

## Project Purpose

This project demonstrates basic NLP techniques and similarity-based FAQ matching through a simple chatbot interface.

## Conclusion

The FAQ answers are sample responses for demonstration purposes. They should be customized to match the policies of an actual business.
