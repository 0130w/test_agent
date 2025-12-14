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
    2.  **Write Code**: Use the `write_file` tool to create or update files. Do not just output code blocks in the chat; you MUST write them to disk.
    3.  **Verify**: You may use `list_files` or `read_file` to ensure your files were written correctly.
    4.  **Completion**: Once you have implemented all files mentioned in the plan, respond with a final summary confirming the work is done.
    
    IMPORTANT:
    - Write complete, functional code.
    - Do not leave placeholders like "# TODO".
    """

    inputs = {
        "messages": [SystemMessage(content=system_prompt)] + state["messages"]
    }
    
    result = agent_runnable.invoke(inputs)
    
    return {
        "messages": [result["messages"][-1]]
    }
