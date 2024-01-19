import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers

# Function to get response from LLAma 2 Model


def getLLamaresponse(input_text, no_words, expert_advice):

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
        to students {expert_advice} university search {input_text}
        within {no_words} words.
            """

    prompt = PromptTemplate(input_variables=["expert_advice", "input_text", 'no_words'],
                            template=template)

    # Generating the response
    response = llm(prompt.format(expert_advice=expert_advice,
                   input_text=input_text, no_words=no_words))
    print(response)
    return response


st.set_page_config(page_title="University Explorer Bot",
                   page_icon=':llama:',
                   layout='centered',
                   initial_sidebar_state='collapsed')

st.header("University Explorer ChatBot")

input_text = st.text_input("Search the Information you want")

# Creating columns for Additional fields

col1, col2 = st.columns([5, 5])

with col1:
    no_words = st.text_input('Number of words')
with col2:
    blog_style = st.selectbox('Expert Advice for',
                              ('Student', 'Teacher', 'Parent'), index=0)

submit = st.button("Generate")

# Final Response

if submit:
    st.write(getLLamaresponse(input_text, no_words, blog_style))
