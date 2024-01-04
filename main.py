import streamlit as st
import os 
import openai
import pandas as pd
from streamlit_chat import message


st.set_page_config(page_title="ChatGPT", layout="centered", initial_sidebar_state="auto",)

st.title("TANGO2 Deficiency Agent")
st.sidebar.write("Hello, I am a LLM powered medical assistant specialized in TANGO2 deficiency. I can provide information and support for both patients and physicians. TANGO2 deficiency is a rare genetic disorder with symptoms including developmental delay, intellectual disability, gait incoordination, speech difficulties, seizures, and hypothyroidism.")
st.sidebar.write("I can provide information on current research, guidelines, and best practices for managing this condition. Additionally, I can offer support in understanding test results, medication options, lifestyle adjustments, and strategies for coping with the disorder.")
st.sidebar.write("However, remember that my advice is not a substitute for professional medical advice, diagnosis, or treatment. Always consult your physician or other qualified health provider with any questions you may have regarding a medical condition.")
st.sidebar.write("By Health Universe 2023.")

openai.api_key = os.environ.get('OPENAI-KEY')

CONTENT = open('resources/system_prompt.txt', 'r').read()

def get_response():
    message_placeholder = st.empty()
    full_response = ""
    messages = [{"role": "system", "content": CONTENT}] + [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
    st.session_state["app"] = messages[-1]['content']
    
    for response in openai.ChatCompletion.create(
        model=st.session_state["openai_model"],
        messages= messages,
        stream=True,
    ):
        full_response += response.choices[0].delta.get("content", "")
    message_placeholder.markdown(full_response)
    return full_response

def main():
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4-1106-preview"

    # load previous messages, or empty list if there are no previous messages
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content":"Hi! How can I help you today?"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # chatting part
    if prompt := st.chat_input("How can I help you?"):
        # user input
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # response
        with st.chat_message("assistant"):
            full_response = get_response()
        st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()
