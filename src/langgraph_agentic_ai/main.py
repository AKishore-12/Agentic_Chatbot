import streamlit as st
from src.langgraph_agentic_ai.LLMs.groq_llm import GroqLLM
from src.langgraph_agentic_ai.ui.streamlit.load_ui import LoadStreamlitUI
from src.langgraph_agentic_ai.graph.graph_builder import GraphBuilder
from src.langgraph_agentic_ai.ui.streamlit.display_result import DisplayResultStreamlit

def load_langgraph_agentic_ai_app():
    '''
    Loads and runs the Agentic AI application with Streamlit UI
    '''

    # Load UI
    UI = LoadStreamlitUI()
    user_input = UI.load_streamlit_ui()

    if not user_input:
        st.error("Error: Failed to load user input from the UI.")
        return
    if st.session_state.IsFetchClicked:
        user_message = st.session_state.timeframe
    else:
        user_message = st.chat_input("Enter your message:")

    if user_message:
        try:
            # Configure LLM
            obj_llm_config = GroqLLM(user_controls_input=user_input)
            model = obj_llm_config.get_llm_model()

            if not model:
                st.error("Error: LLM model could not be initialized.")
                return
            
            # Initialize and setup the graph based on use case
            usecase = user_input.get('selected_usecase')
            if not usecase:
                st.error("Error: No use case selected.")
                return
            
            # Graph builder
            graph_builder = GraphBuilder(model)
            try:
                graph = graph_builder.setup_graph(usecase)
                DisplayResultStreamlit(usecase, graph, user_message).display_result_on_ui()
            except Exception as e:
                st.error(f"Error: Graph set up failed - {e}")
                return

        except Exception as e:
            st.error(f"Error: Graph set up failed - {e}")
            return