import streamlit as st
from textSummarizer.pipeline.prediction import PredictionPipeline

# Title of the app
st.title('Text Summarization')

# Dark mode toggle
dark_mode = st.checkbox("🌙 Toggle Dark Mode")

# Styling based on dark mode
if dark_mode:
    st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: white;
        }
        .stTextInput, .stTextArea {
            background-color: #333;
            color: white;
        }
        .stButton button {
            background-color: #007bff;
        }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
        body {
            background-color: #f8f8f8;
            color: #333;
        }
        .stTextInput, .stTextArea {
            background-color: #fff;
            color: #333;
        }
        .stButton button {
            background-color: #007bff;
        }
    </style>
    """, unsafe_allow_html=True)

# Input field for text
text = st.text_area("Enter Text", height=150)

# Character counter
st.write(f"Characters: {len(text)}")

# Button to trigger summarization
if st.button("Summarize"):
    if text.strip():
        st.write("⏳ Summarizing...")
        try:
            obj = PredictionPipeline()
            result = obj.predict(text)
            st.subheader("Summary")
            st.write(result)
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter some text before summarizing!")
