import streamlit as st
from dotenv import load_dotenv 
from openai import OpenAI 
import os
import chromadb

load_dotenv()

os.environ["TOKENIZERS_PARALLELISM"] = "false"

storage_path = os.getenv('STORAGE_PATH')

client = chromadb.PersistentClient(path=storage_path)

collection = client.get_or_create_collection(name="database_systems")

openai_api_key = os.getenv("API_KEY")


def get_res(prompt):
    query = collection.query(query_texts=prompt, n_results=5)
    updated_prompt = f"""
    You are an experienced researcher on Database Systems and can answer any question regarding about it
    
    This is the question {prompt}
    and here is the context you can use to answer this quesiton: {query},
    in your response, give the id of the document where you got the answer
    """
    
    return updated_prompt


st.title("💬 Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    _prompt = get_res(prompt)
    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": _prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-4o-mini", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)