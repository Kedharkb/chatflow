import streamlit as st
import os
import time
import promptflow as pf
import json 

# Function to delete the history.json file
def delete_history_file():
    history_file_path = "history.json"
    if os.path.exists(history_file_path):
        os.remove(history_file_path)    


def save_history(question,answer):
        chat_history = load_history() 
        chat_history.append({"question":question,"answer":answer})
        with open('history.json','+w') as fd:
            json.dump(chat_history,fd)

def load_history():
    try:
        with open('history.json') as fd:
            chat_history = json.load(fd)
        return chat_history
    except Exception as e:
        return []


def main():
    st.title("Chatbot")
    chat_history = []
    flow = pf._load_flow(source='./flow.dag.yaml')
    chat_history = load_history()

    # Display chat history in the sidebar
    for msg in chat_history:
        with st.chat_message("user"):
            st.markdown(msg["question"])
        with st.chat_message("assistant"):
            st.markdown(msg["answer"])

    if prompt := st.chat_input("What is up?"):
        with st.chat_message("user"):
            st.markdown(prompt)

            

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            response = flow.invoke(inputs={'question':prompt,'chat_history':chat_history})
            # Simulate stream of response with milliseconds delay
            for chunk in response.output["answer"].split():
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            save_history(prompt,response.output["answer"])            

if __name__ == "__main__":
    main()
