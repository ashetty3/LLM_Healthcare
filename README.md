# Healthcare AI Assistant

This Streamlit application utilizes OpenAI's GPT-3.5 model to assist healthcare professionals by automating the creation of discharge summaries and providing disease explanations based on patient data. It integrates with the Unified Medical Language System (UMLS) for retrieval augmented generation (RAG).

## Features

- **Patient Discharge Decision**: Determines whether a patient is safe to be discharged based on the provided data.
- **Generate Patient Summary**: Writes a discharge letter for a patient in a structured format, adhering to clinical guidelines.
- **Generate RAG Query**: Extracts a disease term from the patient data to query the UMLS and provides a brief explanation suitable for patients.

## Setup Instructions

1. Install the required packages:

```bash
pip install openai==1.12.0
pip install streamlit
```

2. Place your OpenAI and UMLS API keys in a credentials.json file in the root directory of the project:

{
  "openai_api_key": "YOUR_OPENAI_API_KEY",
  "umls_api_key": "YOUR_UMLS_API_KEY"
}

3. Run the application using Streamlit:

```bash
streamlit run app.py --server.enableXsrfProtection false
```

## How to use

1. Launch the application and upload the patient's JSON data file using the provided uploader.
2. The application will process the file and display a decision on patient discharge.
3. If the patient is to be discharged, the application will generate a detailed discharge summary following a chain-of-thought process.
4. The application will also provide a simple disease explanation based on UMLS data for patient education.
