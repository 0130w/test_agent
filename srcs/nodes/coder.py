from langchain_core.messages import SystemMessage
from langchain_deepseek import ChatDeepSeek
from langgraph.prebuilt import create_react_agent

from srcs.tools import list_files, read_file, write_file, run_shell_command
from srcs.state import MessagesState

def coder(state: MessagesState):
    print("--- CODER NODE (Software Engineer) ---")
    
    llm = ChatDeepSeek(model='deepseek-chat', temperature=0.1)
    
    coder_tools = [list_files, read_file, write_file, run_shell_command]
    
    agent_runnable = create_react_agent(llm, tools=coder_tools)

    system_prompt = """
    You are a Senior Software Engineer.
    Your task is to implement the coding plan provided by the "Technical Architect" (the previous speaker).

    GUIDELINES:
    1.  **Execute the Plan**: specificially follow the steps listed in the plan.
    2.  **Write Code**: Use the `write_file` tool to create or update files.
    3.  **Completion (CRITICAL)**: ONLY when you have successfully implemented all files and logic mentioned in the plan, you **MUST** output a **Final Answer** (e.g., 'I have successfully implemented all planned files.') to signal the end of your work.
    4.  **Error Handling**: If a tool call repeatedly fails (e.g., permission error), you MUST report the failure as your Final Answer instead of looping.
    5.  **Avoid Testing**: For this simplified workflow, DO NOT generate any unit tests or test files (e.g., test_*.py). Focus purely on implementing the main application logic.
    """

    inputs = {
        "messages": [SystemMessage(content=system_prompt)] + state["messages"]
    }
    
    result = agent_runnable.invoke(inputs)
    
    return {
        "messages": [result["messages"][-1]]
    }
