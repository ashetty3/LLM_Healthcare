import streamlit as st
from openai import OpenAI
import logging
import json



# Global variables
logger = None
openai_api_key = None
umls_api_key = None

def del_sensitive_data(data,sensitive_key = ['name','firstname','lastname','patient_id']):
  keys = list(data.keys())
  for key in keys:
    if type(data[key]) is dict:
      del_sensitive_data(data[key])
    else:
      if key.lower() in sensitive_key:
        del data[key]

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

def init_credentials(credentials_path):
    with open(credentials_path, 'r') as file:
        credentials = json.load(file)

    openai_api_key = credentials['openai_api_key']
    umls_api_key = credentials['umls_api_key']

def init_logger():
    #Setup the logger
    logger = logging.getLogger('logger')  # Create a logger object
    logger.setLevel(logging.DEBUG)  # Set the minimum logging level

    #Create a file handler that logs even debug messages
    file_handler = logging.FileHandler('llm.log')
    file_handler.setLevel(logging.DEBUG)

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)


def init():
    # Init the credentials
    credentials_path = 'credentials.json'
    init_credentials(credentials_path)

    # Init the logger
    init_logger()
# Main function
def main():
    st.title("Healthcare AI Assistant")

    # Initialize variables for user interaction
    uploaded_file = st.file_uploader("Upload JSON file:", type=["json"])
    patient_data_input = st.text_area("Enter patient data:", "")
    additional_prompts = ""
    result_discharge = None
    result_summary = None

    # If JSON file is uploaded, process it
    if uploaded_file is not None:
        # Parse JSON data
        try:
            # De-identify patient data
            patient_data = json.load(uploaded_file)
            llm_patient_data = patient_data.copy()
            del_sensitive_data(llm_patient_data)
            
            # Perform Patient Discharge Decision
            result_discharge = ok_for_discharge(llm_patient_data)
            
            # Check if the patient is discharged
            if result_discharge == "Yes":
                # Perform Generate Patient Summary
                result_summary = generate_patient_summary(llm_patient_data)


    

        except json.JSONDecodeError:
            st.error("Invalid JSON format. Please upload a valid JSON file.")

     # If patient data is entered in text area, process it
    elif patient_data_input.strip():
        # Process patient data entered in text area
        try:
            # Parse the text data into a dictionary
            patient_data = patient_data_input

            # Perform Patient Discharge Decision
            result_discharge = ok_for_discharge(patient_data)

            # Check if the patient is discharged
            if result_discharge == "Yes":
                # Perform Generate Patient Summary
                result_summary = generate_patient_summary(patient_data)

        except json.JSONDecodeError:
            st.error("Invalid JSON format. Please enter patient data in valid JSON format.")

    # Display results
    if result_discharge is not None:
        st.write(f"Patient Discharge Decision: {result_discharge}")

    if result_summary is not None:
        st.write("Generated Patient Summary:")
        st.write(result_summary)

if __name__ == "__main__":
    init()
    main()
#Example: {example}







#python -m streamlit run app.py
# if uploading error, try streamlit run app.py --server.enableXsrfProtection false