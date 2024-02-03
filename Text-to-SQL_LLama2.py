# Install Required libraries

import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers
import os
import sqlalchemy
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import psycopg2


def getLLamaresponse(question, prompt):

    # Loading the LLama 2 Model
    llm = CTransformers(model='models/llama-2-7b-chat.ggmlv3.q8_0.bin',
                        model_type='llama',
                        config={
                            'max_new_tokens': 512,
                            'temperature': 0.01,
                            'context_length': 512,
                        })

    # Generating the response
    response = llm(prompt[0], question)
    return response

# function to query from the database


def execute_sql_query(query, db):
    # Database connection URL
    url = 'postgresql+psycopg2://USER:PASSWORD@HOST:PORT/DB_NAME'

    # Creating a SQLAlchemy engine
    engine = create_engine(url)

    # Creating a session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Connecting and creating a cursor
    connection = engine.connect()
    cursor = connection.connection.cursor()

    try:
        # Executing the query using SQLAlchemy text() construct
        result = connection.execute(text(query))
        rows = result.fetchall()

        # Printing the rows
        for row in rows:
            print(row)

    finally:
        # Closing the cursor and connection
        cursor.close()
        connection.close()

    return rows


# PromptTemplate


prompt = [
    """
    You are an Expert in converting English Questions to SQL query!
    The SQL database has the name "ADM2022". You have to generate SQL queries for postgreSQL database to get the required information from the database.
    The queries should be \n\n For Example, \n Example 1 - Institutes which require English Proficiency Test for getting admission in undergrad?
        The SQL command will be something like this Select IC.campusid, IC.pcaddr, IC.pccity from public."ADM2022" as ADM inner join public."IC2022_CAMPUSES" as IC on ADM.unitid = IC.index where ADM.admcon8 = 1;
        \n Example 2 - Institutes which require Formal demonstration of competencies for getting admission in undergrad?
        The SQL command will be something like this Select IC.campusid, IC.pcaddr, IC.pccity from public."ADM2022" as ADM inner join public."IC2022_CAMPUSES" as IC on ADM.unitid = IC.index where ADM.admcon6 = 1 ; 
        also the SQL code should not have ''' in the beginning and end and sql word in the output
    """
]

# Streamlit UI
st.set_page_config(page_title="University Explorer Bot")
st.header("Text-to-SQL Bot")

question = st.text_input("input: ", key="input")
Enter = st.button("Ask the Question")

if Enter:
    response = getLLamaresponse(question, prompt)
    print(response)
    data = execute_sql_query(response, "defaultdb")
    st.subheader("The Response is")
    for row in response:
        print(row)
        st.header(row)

    # ('unitid',)
    #     ('admcon1',)
    #     ('admcon2',)
    #     ('admcon3',)
    #     ('admcon4',)
    #     ('admcon5',)
    #     ('admcon6',)
    #     ('admcon7',)
    #     ('admcon8',)
    #     ('admcon9',)
    #     ('admcon10',)
    #     ('admcon11',)
    #     ('admcon12',)
    #     ('applcn',)
    #     ('applcnm',)
    #     ('applcnw',)
    #     ('applcnan',)
    #     ('applcnun',)
    #     ('admssn',)
    #     ('admssnm',)
    #     ('admssnw',)
    #     ('admssnan',)
    #     ('admssnun',)
    #     ('enrlt',)
    #     ('enrlm',)
    #     ('enrlw',)
    #     ('enrlan',)
    #     ('enrlun',)
    #     ('enrlft',)
    #     ('enrlftm',)
    #     ('enrlftw',)
    #     ('enrlftan',)
    #     ('enrlftun',)
    #     ('enrlpt',)
    #     ('enrlptm',)
    #     ('enrlptw',)
    #     ('enrlptan',)
    #     ('enrlptun',)
    #     ('satnum',)
    #     ('satpct',)
    #     ('actnum',)
    #     ('actpct',)
    #     ('satvr25',)
    #     ('satvr50',)
    #     ('satvr75',)
    #     ('satmt25',)
    #     ('satmt50',)
    #     ('satmt75',)
    #     ('actcm25',)
    #     ('actcm50',)
    #     ('actcm75',)
    #     ('acten25',)
    #     ('acten50',)
    #     ('acten75',)
    #     ('actmt25',)
    #     ('actmt50',)
    #     ('index',)
    #     ('xapplcn',)
    #     ('xenrlptw',)
    #     ('xapplcnm',)
    #     ('xsatmt50',)
    #     ('xapplcnw',)
    #     ('xenrlptan',)
    #     ('xapplcnan',)
    #     ('xactmt25',)
    #     ('xapplcnun',)
    #     ('xenrlptun',)
    #     ('xadmssn',)
    #     ('xsatmt75',)
    #     ('xadmssnm',)
    #     ('xsatnum',)
    #     ('xadmssnw',)
    #     ('xacten50',)
    #     ('xadmssnan',)
    #     ('xsatpct',)
    #     ('xadmssnun',)
    #     ('xactcm25',)
    #     ('xenrlt',)
    #     ('xactnum',)
    #     ('xenrlm',)
    #     ('xactmt75',)
    #     ('xenrlw',)
    #     ('xactpct',)
    #     ('xenrlan',)
    #     ('xactcm50',)
    #     ('xenrlun',)
    #     ('xsatvr25',)
    #     ('xenrlft',)
    #     ('xacten75',)
    #     ('xenrlftm',)
    #     ('xsatvr50',)
    #     ('xenrlftw',)
    #     ('xactcm75',)
    #     ('xenrlftan',)
    #     ('xsatvr75',)
    #     ('xenrlftun',)
    #     ('xactmt50',)
    #     ('xenrlpt',)
    #     ('xsatmt25',)
    #     ('xenrlptm',)
    #     ('xacten25',)
    #     The Data Dictionary in order for the column names is as follows:
    #     Unique identification number of the institution
    #     Secondary school GPA
    #     Secondary school rank
    #     Secondary school record
    #     Completion of college-preparatory program
    #     Recommendations
    #     Formal demonstration of competencies
    #     Admission test scores
    #     English Proficiency Test
    #     Other Test (Wonderlic, WISC-III, etc.)
    #     Work experience
    #     Personal statement or essay
    #     Legacy status
    #     Applicants total
    #     Applicants men
    #     Applicants women
    #     Applicants another gender
    #     Applicants gender unknown
    #     Admissions total
    #     Admissions men
    #     Admissions women
    #     Admissions another gender
    #     Admissions gender unknown
    #     Enrolled total
    #     Enrolled  men
    #     Enrolled  women
    #     Enrolled another gender
    #     Enrolled gender unknown
    #     Enrolled full time total
    #     Enrolled full time men
    #     Enrolled full time women
    #     Enrolled full time another gender
    #     Enrolled full time gender unknown
    #     Enrolled part time total
    #     Enrolled part time men
    #     Enrolled part time women
    #     Enrolled part time another gender
    #     Enrolled part time gender unknown
    #     Number of first-time degree/certificate-seeking students submitting SAT scores
    #     Percent of first-time degree/certificate-seeking students submitting SAT scores
    #     Number of first-time degree/certificate-seeking students submitting ACT scores
    #     Percent of first-time degree/certificate-seeking students submitting ACT scores
    #     SAT Evidence-Based Reading and Writing 25th percentile score
    #     SAT Evidence-Based Reading and Writing 50th percentile score
    #     SAT Evidence-Based Reading and Writing 75th percentile score
    #     SAT Math 25th percentile score
    #     SAT Math 50th percentile score
    #     SAT Math 75th percentile score
    #     ACT Composite 25th percentile score
    #     ACT Composite 50th percentile score
    #     ACT Composite 75th percentile score
    #     ACT English 25th percentile score
    #     ACT English 50th percentile score
    #     ACT English 75th percentile score
    #     ACT Math 25th percentile score
    #     ACT Math 50th percentile score
    #     ACT Math 75th percentile score
