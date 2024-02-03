# Basic Implementation using LLama 2 Model, Prompt template and streamlit for UI
# Install Required libraries

import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers

# Function to get response from LLAma 2 Model


def getLLamaresponse(input_text):

    # Loading the LLama 2 Model
    llm = CTransformers(model='models/llama-2-7b-chat.ggmlv3.q8_0.bin',
                        model_type='llama',
                        config={
                            'max_new_tokens': 256,
                            'temperature': 0.01,
                        })

    # Prompt Template
    template = """
        You are an expert education consultant and are supposed to suggest the best universities 
        to students university search {input_text}.
            """

    prompt = PromptTemplate(input_variables=["input_text"],
                            template=template)

    # Generating the response
    response = llm(prompt.format(
                   input_text=input_text))
    print(response)
    return response


st.set_page_config(page_title="University Explorer Bot",
                   page_icon=':llama:',
                   layout='centered',
                   initial_sidebar_state='collapsed')

st.header("University Explorer ChatBot")

input_text = st.text_input("Search the Information you want")

submit = st.button("Generate")

# Final Response

if submit:
    st.write(getLLamaresponse(input_text))


# To run this code, open terminal and type:
# streamlit run LLama2_bot.py
