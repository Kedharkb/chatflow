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

def save_uploaded_file(uploaded_file):
    if not os.path.exists('./pdfs'):
        os.makedirs('./pdfs')
    
    file_path = os.path.join('./pdfs', uploaded_file.name)
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    return file_path


def main():
    st.title("Chatbot")
    st.sidebar.header("Configuration Settings")

    # Configuration settings inputs
    prompt_token_limit = st.sidebar.number_input("PROMPT TOKEN LIMIT", min_value=1, value=3000)
    max_completion_tokens = st.sidebar.number_input("MAX COMPLETION TOKENS", min_value=1, value=1024)
    chunk_size = st.sidebar.number_input("CHUNK SIZE", min_value=1, value=1024)
    chunk_overlap = st.sidebar.number_input("CHUNK OVERLAP", min_value=0, value=128)
    use_history = st.sidebar.checkbox("Use history", value=True)
    vector_db = st.sidebar.selectbox("Vector DB", options=["chroma", "faiss"], index=0)
    collection_name = st.sidebar.text_input("Collection Name", value="default_collection")

    # PDF upload button in the sidebar
    uploaded_pdf = st.sidebar.file_uploader("Upload a PDF", type="pdf")

    if uploaded_pdf is not None:
        pdf_name = uploaded_pdf.name
        st.sidebar.write(f"Uploaded PDF: {pdf_name}")
        saved_file_path = save_uploaded_file(uploaded_pdf)
        st.sidebar.success(f"PDF saved to {saved_file_path}")
    
    if st.sidebar.button("Clear Chat History"):
        delete_history_file()
        st.sidebar.success("Chat history cleared!")
    
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
            config = {"EMBEDDING_MODEL_DEPLOYMENT_NAME":"text-embedding-ada-002",
                      "CHAT_MODEL_DEPLOYMENT_NAME":"gpt-3.5-turbo",
                      "PROMPT_TOKEN_LIMIT":prompt_token_limit,
                      "MAX_COMPLETION_TOKENS":max_completion_tokens,
                      "VERBOSE":True,
                      "CHUNK_SIZE":chunk_size,
                      "CHUNK_OVERLAP":chunk_overlap
                      }

            response = flow.invoke(inputs={'question':prompt,
                                           'chat_history':chat_history,
                                           'config':config,
                                           'use_history':use_history,
                                           'vector_db':vector_db,
                                           'collection_name':collection_name,
                                           'pdf_name':pdf_name
                                           })
            
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
