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
   git clone <repository-url>
   cd <repository-folder>
