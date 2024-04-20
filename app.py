import streamlit as st
from openai import OpenAI
import logging
import json
import re
import requests



# Initialize logger
logger = logging.getLogger(__name__)


credentials_path = 'credentials.json'

with open(credentials_path, 'r') as file:
    credentials = json.load(file)

openai_api_key = credentials['openai_api_key']
umls_api_key = credentials['umls_api_key']
# Use the API key as needed, for example, to configure OpenAI's API client
OpenAI.api_key = openai_api_key



def ok_for_discharge(patient_data):
    # Initialize the OpenAI client with your API key
    client = OpenAI(api_key=openai_api_key)

    message =  {
                "role": "user",
                "content": f"""w
                              You are a physician deciding whether to discharge a patient. Please decide whether the given patient is safe to discharge.
                              Consider all information provided, particulary the doctors' notes.
                              Write the output in this format: Yes/No
                              Data: {patient_data}
                """,
            }
    # Create the chat completion request with the patient data
    chat_completion = client.chat.completions.create(
        messages=[
          message
        ],
        model="gpt-3.5-turbo",
    )
    result = chat_completion.choices[0].message.content
    logger.info(f'Q: {message}')
    logger.info(f'A: {result}')
    # Return the content of the generated message
    return result


def generate_patient_summary(patient_data, additional_prompts='', instructions='',example=''):
    """
    Generates a patient summary using OpenAI's GPT-3.5.

    Parameters:
    - patient_data (str): The patient data to generate the summary from.
    - additional_prompts (str): Any additional prompts

    Returns:
    - str: The generated patient summary.
    """
    # Initialize the OpenAI client with your API key
    client = OpenAI(api_key=openai_api_key)

    instructions = """
    General Principle:
    - Write the principle if possible or not to discharge
    Discharge Condition:
    - Write the pertinent information you would want to know if you were the outpatient MD seeing the patient again 2 weeks after discharge. For example:
      - In hypertensive urgency, give discharge BP (or 24 hr range)
      - In CHF, give discharge weight
    """

    message =  {
                "role": "user",
                "content": f"""
                              You are a physician writing a discharge letter for a patient. Use patient data from context only. Write it in the format way. 
                              {additional_prompts}
                              Write the output in this format: {instructions}
                              Data: {patient_data}
                """,
            }
    # Create the chat completion request with the patient data
    chat_completion = client.chat.completions.create(
        messages=[
          message
        ],
        model="gpt-3.5-turbo",
    )
    result = chat_completion.choices[0].message.content
    logger.info(f'Q: {message}')
    logger.info(f'A: {result}')
    # Return the content of the generated message
    return result

# Trying ToT function to see if we can make this better : 

def generate_patient_summary_ToT(patient_data, additional_prompts='', instructions=''):
    """
    Generates a patient summary using OpenAI's GPT-3.5.

    Parameters:
    - patient_data (str): The patient data to generate the summary from.
    - additional_prompts (str): Any additional prompts

    Returns:
    - str: The generated patient summary.
    """

    # Initialize the OpenAI client with your API key
    client = OpenAI(api_key=openai_api_key)

    message =  {
                "role": "user",
                "content": f"""
                              There are experts in this room reviewing the letter you just generated. Another doctor who is going to look at the patient in the future, 
                              the nurse who was in charge of the medication and the hospital course and
                               lab personel whp documented the reports for this patient. 
                               All experts will write down 1 step of their thinking, then share it with the group.Then all experts will go on to the next step, etc.
                               If any expert realises theyre missing essential component of the discharge letetr guideline then they will consult other to fill the gap. 
                              The task is : 
                              You are writing a discharge summary for a patient. Use patient data from context only. Minimize hallucinations.
                              Focus on precision and minimize any assumptions or hallucinations not directly supported by the data. 
                              
                              {additional_prompts}
                              Guideline to write the letter to the patient: {instructions} Address the patient in third-person beginning and replace name with yyyyy.
                              Data: {patient_data}
                             

                """,
            }
    # Create the chat completion request with the patient data
    chat_completion = client.chat.completions.create(
        messages=[
          message
        ],
        model="gpt-3.5-turbo",
    )
    result = chat_completion.choices[0].message.content
    logging.info(f'Q: {message}')
    logging.info(f'A: {result}')
    # Return the content of the generated message
    return result

# RAG
def generate_rag_query(patient_data):
    # Initialize the OpenAI client with your API key
    client = OpenAI(api_key=openai_api_key)

    message = {
                "role": "user",
                "content": f"""
                              Suppose you are a physician writing a discharge letter for a patient. You will include a short paragraph explaning the disease for the patient.
                              You will use the Unified Medical Language System (UMLS) for retrieval augmented generation.
                              Based on the patient data, generate an one-word query for the UMLS. Only display the word.
                              Write the output in this format: one word for the disease
                              Example: Diabete
                              Data: {patient_data}
                """,
    }

    # Create the chat completion request with the patient data
    chat_completion = client.chat.completions.create(
        messages=[
          message
        ],
        model="gpt-3.5-turbo",
    )
    result = chat_completion.choices[0].message.content
    logger.info(f'Q: {message}')
    logger.info(f'A: {result}')
    # Return the content of the generated message
    return result

def search_umls(term, api_key):
    search_url = f"https://uts-ws.nlm.nih.gov/rest/search/current"
    params = {
        'apiKey': api_key,
        'string':f'{term}'
    }
    response = requests.get(search_url, params=params)
    logger.info(f'Search UMLS: term: {term}')
    return response.json()

def get_concept_definition(cui, api_key):
    """Get the concept definition using the CUI and service ticket."""
    api_url = f"https://uts-ws.nlm.nih.gov/rest/content/current/CUI/{cui}/definitions"
    params = {
        'apiKey': api_key,
    }
    response = requests.get(api_url, params=params)
    logger.info(f'''
    Get Concept Definition: cui: {cui}
    Response: {response.json()}
                ''')
    return response.json()

def generate_rag_explanation(patient_data,umls):
    # Initialize the OpenAI client with your API key
    client = OpenAI(api_key=openai_api_key)

    message =   {
                "role": "user",
                "content": f"""
                              Suppose you are a physician writing a discharge letter for a patient. You will include a short paragraph explaning the disease for the patient.
                              You will use the Unified Medical Language System (UMLS) for retrieval augmented generation.
                              Based on the patient data and retrieved UMLS results, generate a brief explanation (100-200 words) of the disease for the patient.
                              Do not use unnecessary medical terminology to ensure the patient can understand the disease.
                              Data: {patient_data}
                              UMLS result: {umls}
                              Format:
                                Terminology:
                                Explanation:
                """,
    }
    # Create the chat completion request with the patient data
    chat_completion = client.chat.completions.create(
        messages=[
          message
        ],
        model="gpt-3.5-turbo",
    )
    result = chat_completion.choices[0].message.content
    logger.info(f'Q: {message}')
    logger.info(f'A: {result}')
    # Return the content of the generated message
    return result

# Main function
def main():
    st.title("Healthcare AI Assistant")

    # Initialize variables for user interaction
    uploaded_file = st.file_uploader("Upload JSON file:", type=["json"])
    #patient_data_input = st.text_area("Enter Patient data:", "")
    #patient_inst = st.text_area("Enter Additional instructions data:", "")
    additional_prompts = 'Make sure that the important components of the guideline for the letter are captured and it seems professional and well structured.Consider expert inputs and also generate the final letter'
    result_discharge = None
    result_summary = None

    #Instructions for a good discharge summary :

    # Define the path to your file
    file_path = 'How to write a discharge summary.txt'

# Open the file using 'open()' in read mode ('r')
    with open(file_path, 'r') as file:
    # Read the contents of the file
        instructions = file.read()



    # If JSON file is uploaded, process it
    if uploaded_file is not None:
        # Parse JSON data
        try:
            #patient_data = json.load(uploaded_file)
            mod_patient_data = json.load(uploaded_file)
            pat_name = mod_patient_data['patient_demographics']['name']
            pat_id = mod_patient_data['patient_id']
            del mod_patient_data['patient_demographics']['name']
            del mod_patient_data ['patient_id']

            # Perform Patient Discharge Decision
            result_discharge = ok_for_discharge(mod_patient_data)
            
            # Check if the patient is discharged
            if result_discharge == "Yes":
                # Perform Generate Patient Summary
                result_summary = generate_patient_summary_ToT(mod_patient_data,additional_prompts,instructions)

    
        except json.JSONDecodeError:
            st.error("Invalid JSON format. Please upload a valid JSON file.")



    # Display results
    if result_discharge is not None:
        st.write(f"Patient Discharge Decision: {result_discharge}")

    if result_summary is not None:
        st.write("Generated Patient Summary:")
        replaced_text = result_summary.replace('YYYYY', pat_name)
        st.write(replaced_text)
        with st.container():
            
            query = generate_rag_query(mod_patient_data)
            print(query)
            results = search_umls(query, umls_api_key)
            print(results)
            cui = None
            if results['result']['results']:
                cui = results['result']['results'][0]['ui']
            print(cui)
            if cui:
                results = get_concept_definition(cui, umls_api_key)
                definition = results['result']
                rag_text = generate_rag_explanation(mod_patient_data,definition)
                st.header('Disease Explanation')
                st.write(rag_text)
     
        

if __name__ == "__main__":
    main()
#Example: {example}





#streamlit run app.py --server.enableXsrfProtection false

#python -m streamlit run app.py