import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

from srcs.graph import build_graph
from srcs.state import MessagesState

load_dotenv()

required_vars = ["DEEPSEEK_API_KEY", "GITHUB_TOKEN", "GITHUB_REPO"]
missing = [var for var in required_vars if not os.getenv(var)]
if missing:
    print(f"missing env variables: {', '.join(missing)}")
    exit()

if __name__ == "__main__":
    app = build_graph()
    user_request = """
    Task: Add a new utility function (tool) to the project.

    Detailed Steps:
    1.  Read the existing `tools.py` file within the current project structure (use the `list_files` tool first to confirm its location in the current or parent directory).
    2.  Append a new function, named `count_file_lines`, to the `tools.py` file.
        * This function must be decorated with `@tool`.
        * **Functionality:** It should accept a single argument, `file_path` (str), and return the total number of lines in that file (str or int).
        * It must include simple exception handling (e.g., for `FileNotFoundError`).
    3.  **Critical Rule:** Ensure that the original code in `tools.py` is preserved. You must write back the **full content** (original code plus the new function) when using the `write_file` tool.
    """

    print(f"start to execute task, user_request: {user_request}\n")

    initial_state: MessagesState = {"messages": [HumanMessage(content=user_request)]}

    for chunk in app.stream(initial_state):
        for node_name, state_update in chunk.items():
            print(f"\n-- node {node_name} execution finished.")

    print("finish task, please check PR in Github")