from langgraph.graph import StateGraph, START, END
from src.langgraph_agentic_ai.state.state import State
from src.langgraph_agentic_ai.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraph_agentic_ai.nodes.chatbot_with_tool_node import ChatbotWithToolNode
from src.langgraph_agentic_ai.tools.search_tool import get_tools, create_tool_node
from langgraph.prebuilt import tools_condition

class GraphBuilder:
    def __init__(self, model):
        self.llm = model
        self.graph_builder = StateGraph(State)
    
    def basic_chatbot_build_graph(self):
        '''
        Build a basic chatbot graph using LangGraph
        '''

        self.basic_chatbot_node = BasicChatbotNode(self.llm)

        self.graph_builder.add_node("chatbot",self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)

        print("The graph is build successfully")
    
    def chatbot_with_tool(self):
        '''
        Build a basic chatbot with tool graph using Langgraph
        '''
        # Define the tool and toolnode
        tools = get_tools()
        tool_node = create_tool_node(tools)

        # Define the chatbot node
        obj_chatbot_with_tool = ChatbotWithToolNode(self.llm)
        chatbot_node = obj_chatbot_with_tool.create_chatbot(tools)
        
        # Add nodes
        self.graph_builder.add_node("chatbot",chatbot_node)
        self.graph_builder.add_node("tools", tool_node)

        # Define edges
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_conditional_edges("chatbot", tools_condition)
        self.graph_builder.add_edge("tools", "chatbot")

    def setup_graph(self, usecase: str):
        '''
        Sets up the graph for the selected use case.
        '''
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        elif usecase == "Chatbot With Web":
            self.chatbot_with_tool()
        
        return self.graph_builder.compile()