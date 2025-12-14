from langchain_core.messages import SystemMessage
from langchain_deepseek import ChatDeepSeek

from ..state import MessagesState

def planner(state: MessagesState):
    print("--- PLANNER NODE (Architect) ---")
    
    llm = ChatDeepSeek(model='deepseek-chat', temperature=0)
    
    system_prompt = """
    You are a **Senior Technical Architect**.
    Your objective is to analyze the user requirement and formulate a detailed implementation plan for the subsequent **"Coder" (Software Engineer)** Agent.

    Please adhere strictly to the following guidelines:
    1.  **Do not** write concrete code implementations.
    2.  **Do not** call any tools.
    3.  Your output will be sent directly to the Coder Agent.

    Please generate a clear and atomic step-by-step plan, including:
    * The file names to be created or modified (**File Structure**).
    * The core logic to be implemented in each file.
    * As this is an automated system, ensure the plan is broken down into small, atomic, and sequential steps.

    **Output Format Example:**
    Plan:
    1.  Create file `utils.py`: Implement data processing functions.
    2.  Create file `main.py`: Import utilities and set up the main execution entry point (e.g., CLI).
    3.  Review the overall plan to ensure robust error handling and maintainability.
    """
    messages = [SystemMessage(content=system_prompt)] + state['messages']
    response = llm.invoke(messages)
    return {"messages": [response]}
