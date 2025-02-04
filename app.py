import streamlit as st
from main import generate_ans
from langchain_community.llms import Ollama
import logging

# Streamlit UI
st.title("Q/A bot Physics")

# Sidebar for model selection and sessions
with st.sidebar:
    # dropdown menu to select a model
    selected_model = st.selectbox(
        "Select LLM",
        options=["llama3.1", "mistral"],
        index=0  # Default selection
    )

    st.title("Chat Sessions") # Sidebar title

    # Button to clear the session (chat history and memory)
    if st.button("Clear Session"):
        st.session_state.clear()

# Setting up the LLM based on the selected model
if selected_model == "llama3.1":
    llm = Ollama(model="llama3.1")
elif selected_model == "mistral":
    llm = Ollama(model="mistral")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_ques = st.text_input("Throw your problems.")

if st.button("Submit"):
    if user_ques:
        try:
            with st.spinner("Fetching AI response..."):
                final_ans = generate_ans(user_ques, llm)
                # st.write(f"Answer: {final_ans}")
                st.session_state.chat_history.append({"user": user_ques, "answer": final_ans})
                st.session_state.user_input = ""    # Clear input after submission

        except Exception as e:
            st.error(f"An error occured: {str(e)}")
    else:
        st.write("Please enter a question!")

# Display chat history
if st.session_state.chat_history:
    for chat in st.session_state.chat_history:
        st.write(f"**You:** {chat['user']}")
        st.write(f"**Bot:** {chat['answer']}")
        st.markdown("---")

# logging after each response generation
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def log_query(user_question, answer):
    logger.info(f"Question: {user_question}, Answer: {answer}")