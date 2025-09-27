import streamlit as st
import os

from src.langgraph_agentic_ai.ui.ui_config_file import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls={}
    
    def load_streamlit_ui(self):
        st.set_page_config(page_title="🤖 " + self.config.get_title(), layout="wide")
        st.header("🤖 " + self.config.get_title())

        with st.sidebar:
            # get options
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()

            # LLM Selecion
            self.user_controls["selected_llm"] = st.selectbox("Select LLM", llm_options)

            if self.user_controls["selected_llm"] == "Groq":
                # Model selection
                groq_llm_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"] = st.selectbox("Select Model", groq_llm_options)
                self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"] = st.text_input("API Key", type='password')

                # Validate API Key
                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("⚠️ Please enter your Groq API Key to proceed.")
                
            # Use case selection
            self.user_controls['selected_usecase'] = st.selectbox("Select Usecases", usecase_options)

            if self.user_controls['selected_usecase'] == 'Chatbot With Web':
                os.environ['TAVILY_API_KEY'] = self.user_controls["TAVILY_API_KEY"] = st.session_state['TAVILY_API_KEY'] = st.text_input("Tavily API Key", type="password")

                # Validate API Key
                if not self.user_controls["TAVILY_API_KEY"]:
                    st.warning("⚠️ Please enter your Tavily API Key to proceed.")
        
        return self.user_controls