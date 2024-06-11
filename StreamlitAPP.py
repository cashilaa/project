import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging
import streamlit as st
from openai_callbacks import get_openai_callback

def generate_evaluate_chain(params):
    # Implementation of generate_evaluate_chain
    pass


# Load environment variables
load_dotenv()

# Load the JSON response file
with open('C:/Users/Admin/mcqgen/response.json', 'r') as file:
    # Do something with the file

    RESPONSE_JSON = json.load(file)

# Create title
st.title("MCQ Generator")

# Create a form using st.form
with st.form("user_inputs"):
    # File upload
    uploaded_file = st.file_uploader("Upload your PDF or TXT file")

    # Input fields
    mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=50)

    # Subject
    subject = st.text_input("Insert Subject", max_chars=28)

    # Quiz tone
    tone = st.text_input("Complexity level of questions", max_chars=20, placeholder='simple')

    # Add button
    button = st.form_submit_button("Create MCQs")

    # Check if the button is clicked and all fields have input
    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Loading..."):
            try:
                text = read_file(uploaded_file)
                # Count tokens and generate MCQs
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain(
                        {
                            "text": text,
                            "number": mcq_count,
                            "subject": subject,
                            "tone": tone,
                            "response_json": json.dumps(RESPONSE_JSON)
                        }
                    )
                    cb.update_tokens(response["total_tokens"])  # Assuming response contains total_tokens

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("An error occurred")

            else:
                print(f"Total Tokens: {cb.total_tokens}")
                print(f"Prompt Tokens: {cb.prompt_tokens}")
                print(f"Completion Tokens: {cb.completion_tokens}")
                print(f"Total Cost: {cb.total_cost}")

                if isinstance(response, dict):
                    quiz = response.get("quiz", None)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.table(df)
                            st.text_area(label='Review', value=response["review"])
                        else:
                            st.error("Failed to generate MCQs")
                    else:
                        st.write(response)