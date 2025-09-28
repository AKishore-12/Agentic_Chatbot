from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import tools_condition
from src.langgraph_agentic_ai.state.state import State
from src.langgraph_agentic_ai.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraph_agentic_ai.nodes.chatbot_with_tool_node import ChatbotWithToolNode
from src.langgraph_agentic_ai.nodes.ai_news_node import AINewsNode
from src.langgraph_agentic_ai.tools.search_tool import get_tools, create_tool_node

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
    
    def ai_news_builder_graph(self):
        '''
        Build a basic news summarizer graph using LangGraph
        '''
        ai_news_node = AINewsNode(self.llm)

        # Add nodes
        self.graph_builder.add_node("fetch_news",ai_news_node.fetch_news)
        self.graph_builder.add_node("summarizer",ai_news_node.summarize_news)
        self.graph_builder.add_node("save_result",ai_news_node.save_result)

        # Add edges
        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news", "summarizer")
        self.graph_builder.add_edge("summarizer", "save_result")
        self.graph_builder.set_finish_point("save_result")

    def setup_graph(self, usecase: str):
        '''
        Sets up the graph for the selected use case.
        '''
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        elif usecase == "Chatbot With Web":
            self.chatbot_with_tool()
        elif usecase == "AI News":
            self.ai_news_builder_graph()
        
        return self.graph_builder.compile()