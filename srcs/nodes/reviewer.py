import os
from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent

from tools import list_files, read_file, run_shell_command, create_pull_request

from state import MessagesState

def reviewer(state: MessagesState):
    print("--- REVIEWER NODE (Release Manager) ---")
    
    # 确保环境变量 DEEPSEEK_API_KEY 已设置
    llm = ChatDeepSeek(
        model='deepseek-chat', 
        temperature=0
    )
    
    reviewer_tools = [
        list_files,
        run_shell_command,
        create_pull_request,
        read_file
    ]
    
    agent_runnable = create_react_agent(llm, tools=reviewer_tools)
    
    system_prompt = """
    You are the Release Manager for this project.
    The 'Coder' has already modified the files on the local disk.
    
    Your goal is to submit these changes to Github and create a Pull Request.
    
    Please follow these steps strictly:
    1. Check git status using `run_shell_command` to see what changed.
    2. Create a new branch with a descriptive name (e.g., feature/update-logic-<timestamp>).
    3. Add all changes (`git add .`).
    4. Commit changes (`git commit -m "..."`).
    5. Push the branch (`git push origin <branch_name>`).
    6. Create a Pull Request using `create_pull_request`.
       - The title should summarize the changes.
       - The body should describe what was done based on the conversation history.
       
    IMPORTANT: 
    - Do not ask for user permission, just do it.
    - If `git push` fails due to authentication, report the error.
    """
    
    inputs = {
        "messages": [SystemMessage(content=system_prompt)] + state["messages"]
    }
    
    result = agent_runnable.invoke(inputs)
    
    last_message = result["messages"][-1]
    
    return {
        "messages": [last_message]
    }