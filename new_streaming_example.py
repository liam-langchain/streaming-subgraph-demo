"""
The EXACT fix from GitHub issue #5249 for streaming problem
This shows the precise pattern from the LangGraph maintainer's comment
    FIX:
    1. Upgrade to LangGraph >= 0.6.4
    2. Replace this in your find_node function:
    
    OLD:
       result = find_agent.invoke(state)
    
    NEW:
       final_result = None
       for event in find_agent.stream(state, stream_mode='messages'):
           if event:
               final_result = {'messages': event}
       result = final_result
    
    LangGraph 0.6.4 fix (#5836) enables this streaming pattern!
    
"""
import os
from dotenv import load_dotenv
from typing import Dict, List, TypedDict
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

load_dotenv()
if os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY").strip()

class AgentState(TypedDict):
    messages: List[BaseMessage]

# BROKEN:current code 
def find_node_broken(state: AgentState, config: RunnableConfig) -> Dict[str, List[BaseMessage]]:
    """This broke after LangGraph change #4843"""
    llm = ChatOpenAI(model="gpt-4o-mini", streaming=True, temperature=0)
    tools = []
    
    # subgraph was called as a function inside parent node
    find_agent = create_react_agent(llm, tools)  # This creates a subgraph
    
    # This breaks streaming after #4843
    result = find_agent.invoke(state)
    
    return {
        "messages": [AIMessage(content=result["messages"][-1].content, name="find")]
    }

# FIXED: The pattern from GitHub issue #5249
def find_node_fixed(state: AgentState, config: RunnableConfig) -> Dict[str, List[BaseMessage]]:
    """This is the GitHub issue fix - explicitly request messages streaming"""
    llm = ChatOpenAI(model="gpt-4o-mini", streaming=True, temperature=0)
    tools = []
    
    # subgraph was called as a function.
    subgraph = create_react_agent(llm, tools)  # This creates a subgraph
    
    # messages are explicitly requested to preserve streaming!
    last_event = None
    for event in subgraph.stream(state, stream_mode="messages"):
        # something is done with `event` 
        if event:  # Process the streaming event
            last_event = event
    
    # Return the final result
    if last_event:
        # event is a tuple: (message, metadata)
        message = last_event[0]
        return {
            "messages": [AIMessage(content=message.content, name="find")]
        }
    
    return {"messages": [AIMessage(content="No response", name="find")]}

def test():
    pass


if __name__ == "__main__":
    test()
