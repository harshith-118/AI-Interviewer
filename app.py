import streamlit as st
import pandas as pd
import os
import pdfplumber
import google.generativeai as genai
from dotenv import load_dotenv

# Configure Google Generative AI
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize session state
if "context" not in st.session_state:
    st.session_state.context = ""  # Store the conversation context
if "qa_pairs" not in st.session_state:
    st.session_state.qa_pairs = []  # Store Q&A pairs for export

# Functions to handle file content
def extract_file_content(file_path):
    """
    Extract content from various file types (Excel, PDF).
    """
    _, file_extension = os.path.splitext(file_path)

    if file_extension.lower() == ".xlsx":
        # Extract data from Excel
        data = pd.read_excel(file_path)
        return data
    elif file_extension.lower() == ".pdf":
        # Extract data from PDF
        return extract_text_from_pdf(file_path)
    else:
        raise ValueError("Unsupported file format. Only Excel (.xlsx) and PDF (.pdf) are supported.")

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file using pdfplumber for better parsing.
    """
    text_data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text_data.append(page.extract_text())
    return "\n".join(text_data)

def get_gemini_response(input_text):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(input_text)
    return response.text if response else None

def generate_question(data, context, temperature=0.7, max_tokens=256):
    """
    Generate a question based on the provided data and context.
    """
    prompt = f"""
    You are an intelligent and professional interviewer conducting an insightful interview based on the given data. 
    Your goal is to ask specific, domain-relevant, and engaging questions that build on previous responses.

    Data: {data}

    Previous Context: {context}

    Based on this information, craft the next question:
    """
    try:
        response = get_gemini_response(prompt)
        return response if response else "No response generated."
    except Exception as e:
        return f"Error generating question: {str(e)}"

def start_interview(data, is_tabular):
    """
    Handle the interview process.
    """
    if is_tabular:
        for i, row in data.iterrows():
            question = generate_question(row.to_dict(), st.session_state.context)
            st.write(f"**Q{i + 1}:** {question}")
            user_answer = st.text_input(f"Your answer to Q{i + 1}:", key=f"answer_{i}")
            if user_answer:
                st.session_state.context += f"Q{i + 1}: {question}\nA{i + 1}: {user_answer}\n"
                st.session_state.qa_pairs.append((question, user_answer))
    else:
        text_chunks = data.split("\n\n")  # Break into smaller chunks
        for i, chunk in enumerate(text_chunks):
            question = generate_question(chunk, st.session_state.context)
            st.write(f"**Q{i + 1}:** {question}")
            user_answer = st.text_input(f"Your answer to Q{i + 1}:", key=f"answer_{i}")
            if user_answer:
                st.session_state.context += f"Q{i + 1}: {question}\nA{i + 1}: {user_answer}\n"
                st.session_state.qa_pairs.append((question, user_answer))

def analyze_responses(qa_pairs):
    """
    Generate a summary of user responses.
    """
    responses = "\n".join([f"Q: {q}\nA: {a}" for q, a in qa_pairs])
    prompt = f"""
    You are a professional scrutnizer. Based on the following Q&A conversation, provide a concise review on how questions were answered and suggestions on area of improvement:
    {responses}
    """
    try:
        response = get_gemini_response(prompt)
        return response if response else "No summary generated."
    except Exception as e:
        return f"Error generating summary: {str(e)}"

# Streamlit UI


# Sidebar navigation (Tabs)
option = st.sidebar.radio(
    "Select an option",
    ("Start Interview", "Export Q&A", "Analyze Responses")
)

if option == "Start Interview":
    st.title("AI Interviewer")
    st.write("Upload a file to generate interview questions based on its content.")
    uploaded_file = st.file_uploader("Upload a file (Excel or PDF):", type=["xlsx", "pdf"])

    # Additional customization for AI model
    st.sidebar.title("Model Settings")
    temperature = st.sidebar.slider("Temperature (creativity):", 0.0, 1.0, 0.7, 0.1)
    max_tokens = st.sidebar.number_input("Max Tokens:", 50, 1000, 256, step=50)

    if uploaded_file:
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        is_tabular = file_extension == ".xlsx"

        try:
            # Save and process the file
            with open("uploaded_file" + file_extension, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Extract content
            data = extract_file_content("uploaded_file" + file_extension)

            # Start the interview
            st.write("### Starting the Interview:")
            if is_tabular:
                st.write("Processing tabular data...")
                start_interview(data, is_tabular=True)
            else:
                st.write("Processing textual data...")
                start_interview(data, is_tabular=False)

            # Display Q&A pairs so far
            if st.session_state.qa_pairs:
                st.write("### Previous Q&A Pairs:")
                for idx, (q, a) in enumerate(st.session_state.qa_pairs, 1):
                    st.write(f"**{q}**")
                    st.write(f"**{a}**")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

elif option == "Export Q&A":
    if st.session_state.qa_pairs:
        qa_text = "\n\n".join([f"Q: {q}\nA: {a}" for q, a in st.session_state.qa_pairs])
        st.download_button(
            "Download Q&A",
            qa_text,
            file_name="interview_qa.txt",
            mime="text/plain"
        )
    else:
        st.write("No Q&A to export yet.")

elif option == "Analyze Responses":
    if st.session_state.qa_pairs:
        summary = analyze_responses(st.session_state.qa_pairs)
        st.write(summary)
    else:
        st.warning("No responses to analyze yet.")