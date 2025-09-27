from src.langgraph_agentic_ai.state.state import State

class ChatbotWithToolNode:
    '''
    Chatbot logic enhanced with tool integration
    '''
    def __init__(self, model):
        self.llm = model
    
    def create_chatbot(self, tools):
        '''
        Return a chatbot with node function
        '''
        llm_with_tools = self.llm.bind_tools(tools)

        def chatbot_node(state: State):
            '''
            Chatbot logic for preprocessing the input state and returning a response.
            '''
            return {"messages":[llm_with_tools.invoke(state["messages"])]}
        
        return chatbot_node