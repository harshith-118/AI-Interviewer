# AI Interviewer Application

## Overview
The AI Interviewer application is a Streamlit-based tool that uses Google's Generative AI capabilities to create an interactive interviewing experience. Users can upload structured data (Excel) or unstructured text (PDF), and the application will generate domain-specific and context-aware interview questions. The app also allows users to export Q&A pairs and analyze responses with suggestions for improvement.

---

## Features
1. **Start Interview**: 
   - Upload a file (Excel or PDF).
   - Generates interview questions based on the uploaded content.
   - Supports both tabular (Excel) and textual (PDF) data.
   - Allows users to provide answers, stores the Q&A context, and displays ongoing pairs.
   
2. **Export Q&A**:
   - Download all Q&A pairs in a `.txt` file.

3. **Analyze Responses**:
   - Provides a detailed review of the answers and offers suggestions for improvement using AI.

4. **Customization**:
   - Configure AI creativity (`Temperature`) and response length (`Max Tokens`) via the sidebar.

---

## Setup and Installation

### Prerequisites
- Python 3.8 or later.
- A Google API key for Generative AI.
- Installed libraries: `streamlit`, `pandas`, `pdfplumber`, `google.generativeai`, and `python-dotenv`.

### Installation Steps
1. **Clone the repository**:
   ```bash
   git clone https://github.com/harshith-118/AI-Interviewer.git
   cd AI-Interviewer
   ```
2.	**Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up environment variables**:
     - Create a .env file in the root directory.
     - Add the following:
   ```bash
   GOOGLE_API_KEY=your_google_api_key
   ```
4. **Run the application**:
   ```bash
   streamlit run app.py
   ```
### Usage Instructions
1.	**Start the App**:
	•	Launch the app using the command: streamlit run app.py.
	•	Access the app in your browser at http://localhost:8501.
2.	**Navigate Between Tabs**:
	•	Use the sidebar to select between:
	•	Start Interview: Upload a file and begin generating questions.
	•	Export Q&A: Download completed Q&A pairs.
	•	Analyze Responses: Get feedback on your answers.
3.	**Uploading Files**:
	•	Supported formats: Excel (.xlsx) and PDF (.pdf).
	•	Upload relevant data files in the Start Interview tab.
4.	**Generate and Answer Questions**:
	•	Answer generated questions in the text fields provided.
	•	Context is updated dynamically based on previous Q&A pairs.
5.	**Export Q&A**:
	•	Download the Q&A pairs as a text file by visiting the “Export Q&A” tab.
6.	**Analyze Responses**:
	•	Review AI-generated feedback on your answers in the “Analyze Responses” tab.

