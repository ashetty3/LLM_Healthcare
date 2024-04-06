# Healthcare Systems Project

### Overview
Physicians spend a significant amount of time on administrative
work to supplement patient care, where tasks include but are not
limited to: preparing ward round notes, writing discharge
summaries, and writing referral letters (Henry, 2018; Woolhandler,
Himmelstein, 2014). LLMs’ success in an array of natural language
and reasoning tasks in the past few years led to experimentation
and innovation (AWS, 2023). Dr. Frank Instein, DOWNMC Health
System’s CEO, has tasked you with creating an MVP that creates
patient discharge letters based on data about their inpatient stay.

Our task is to experiment with LLMs to create a prototype which generates a patient discharge
summary letter based on sample inpatient data. To begin, explore who your stakeholders are,
what the output should be, what data is available, and prompt engineering techniques.

### High-Level Overview of Technical Setup

* Integration of GPT-3.5 turbo API for Automated Discharge Letters: Our solution will employ the GPT-3.5 API. All the members will recharge their accounts with 5$ of credit for using the API and get their API key. The code will be on git and the creds file has been added to gitignore already.
* Data Exploration: Reviewing the 3 JSON files attached and understanding the features available in the data and how they could be used to advance comprehension and develop better prompts for GPT. 
* Prompt Engineering: We will feed structured patient information into the model to generate detailed and accurate discharge summaries through meticulous prompt engineering, . We aim to try various approaches like the one-shot, chain of thought reasoning  (COTR), and Tree of Thought approach (TOT)  approaches and compare their performance when generating discharge summaries. 
* Output - Discharge Summary: The output should consist of a few fundamental elements necessary in the discharge letter. These are diagnosis, which should be as accurate as possible to guide the practitioners' care plan; past medical history (or secondary diagnoses) for providing comprehensive care for the patient; medications and allergies, to serve as a guide for admission orders and ensure the patient receives correct medications, especially when immediate follow-up care might be delayed; procedures and significant tests, focusing only on those results important for patient outcomes and medical management decisions; reason for admission and hospital course, to communicate the patient's hospitalization story in a concise and cohesive manner; outstanding issues, detailing what is needed for continued care; and follow-up appointments, specifying where, when, and with whom these appointments are, including contact information for rescheduling if necessary. 
* Feature 1 - Safe for Discharge Flag: Thie discharge summary should explicitly mention or alert the user whether the patient should be discharged or not. This could be a pop up or something explicitly mentioned when the patient is unfit for being discharged. 
* Feature 2 -  Explanation for Patient: This segment aims to demystify medical jargon, providing patients with clear and concise explanations of their diagnoses and the underlying pathophysiology, all in accessible language. We plan to incorporate Retrieval-Augmented Generation (RAG) technology. This technology will enable us to source and integrate information from credible medical resources directly into the patient instructions, enhancing the educational value of the discharge summaries
* Feature 3 - Q/A with the summary: We also want the patients to be able to do a Q/A with the discharge summary and get more specific insights about any part of the summary they have doubts about. This feature would be integrated in the way we build our UI.
* Evaluation of the output : We will be rating the effectiveness of the based of three main criterias : Accurate (No hallucinations) , Concise, Clear( Conveys important details in a prose format in a brief but effective manner). Our system will also include a logging function utilizing the logging package for ease of access and evaluation for the historical attempts at prompt engineering. This logging will not only help in monitoring the system's performance but also in ensuring transparency and accountability in the automated generation of discharge letters. 
* User-Friendly Interface: The UI of our system will be developed using Streamlit  This front-end platform will allow healthcare professionals to input patient data in a structured JSON format, which the backend, powered by our .py script, will then process to return the finished discharge summaries. Furthermore, users can do a Q/A style interaction with the summaries for better comprehension. This setup ensures a seamless experience from data input through to the comprehension of the discharge letter.
