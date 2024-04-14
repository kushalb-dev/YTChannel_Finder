from langchain_openai import OpenAI
from dotenv import load_dotenv
from langchain.prompts.chat import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import BaseOutputParser
import streamlit as st
import re
import os
import emoji

# creating the parser class
class OutputParser(BaseOutputParser):    
    def parse(self, text: str) -> str:
        channels = [re.sub("[^0-9a-zA-z.-]"," ", paragraph) for paragraph in text.split('\n')]
        return ('\n').join(channels)

# loading environment variables
def initialize() -> None:
    load_dotenv()

def get_response(input_area_of_interest: str) -> str:
    
    # creating the chat bot
    chat_bot = ChatOpenAI(temperature=0.5, api_key=os.getenv("OPENAI_API_KEY"))
    
    # creating the input message template
    input_message = "Tell me 5 YouTube Channels good for {input}."
    system_primer = "Your role is to help me find youtube channels for my interests. You need to return 5 youtube channels, along with their short description, seperated by newlines"

    # creating the message template
    answer_template = ChatPromptTemplate.from_messages([
        ("system", system_primer),
        ("human", input_message)
    ]
    )

    # creating a chain to get response
    final_output = answer_template | chat_bot | OutputParser()

    return final_output.invoke({"input": input_area_of_interest})

def write_streamlit() -> None:
    
    st.set_page_config(page_title="YT Channel Finder", page_icon=emoji.emojize(":brain:"))
    st.header("YouTube Channel Finder")
    
    # Get the input area of interest
    input_text = st.text_input("Area of Interest", key="interest")
    
    # Get the response from langchain when button is pressed    
    submit_button = st.button("Get Channels")
    
    if submit_button:
        response = get_response(input_text)
        st.text_area(label="The Channels Are:", value=response, height=300)

if __name__ == "__main__":
    initialize()
    write_streamlit()
