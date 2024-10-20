from langchain_groq import ChatGroq
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT, WELCOME_MESSAGE
#from data.employees import generate_employee_data
from gui import AssistantGUI
from assistant import Assistant
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import logging
from langchain_cohere import CohereEmbeddings



if __name__ == "__main__":

    load_dotenv()

    logging.basicConfig(level=logging.INFO)

    st.set_page_config(page_title="Saran GenAI labs", page_icon="🤖", layout="wide")

    #st.title("Saran GenAI Assistant \n \n")

    # @st.cache_data(ttl=3600, show_spinner="Generating User Data...")
    # def get_user_data():
    #     return generate_employee_data(1)[0]

    @st.cache_resource(ttl=3600, show_spinner="Loading Vector Store...")
    def init_vector_store(pdf_path):
        try:
            loader = PyPDFLoader(pdf_path)
            docs = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap=200
            )
            splits = text_splitter.split_documents(docs)

            #embedding_function = OpenAIEmbeddings()
            embedding_function = CohereEmbeddings(model="embed-english-v3.0",)
            #persistent_path = "./data/vectorstore"
            # vectorstore = Chroma.from_documents(
            #     documents=splits,
            #     embedding=embedding_function,
            #     persist_directory=persistent_path
            # )

            vectorstore = FAISS.from_documents(splits, embedding_function)

            return vectorstore
        except Exception as e:
            logging.error(f"Error initializing vector store: {str(e)}")
            st.error(f"Failed to initialize vector store: {str(e)}")
            return None

    #vector_store = init_vector_store("data/umbrella_corp_policies.pdf")
    vector_store = init_vector_store("./data/SaranGenAI.pdf")
    if vector_store is None:
        st.error(
            "Failed to initialize vector store. Please check the logs for more information."
        )
        st.stop()

    llm = ChatGroq()
    system_prompt = SYSTEM_PROMPT
    welcome_message = WELCOME_MESSAGE
    #customer_data = get_user_data()
    vector_store = init_vector_store("./data/SaranGenAI.pdf")

    # if "customer" not in st.session_state:
    #     st.session_state.customer = customer_data
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "ai", "content": welcome_message}]

    assistant = Assistant(
        system_prompt=system_prompt,
        llm=llm,
        #employee_information=st.session_state.customer,
        message_history=st.session_state.messages,
        vector_store=vector_store,
    )

    gui = AssistantGUI(assistant=assistant)
    gui.render()
