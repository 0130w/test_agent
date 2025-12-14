from langchain.messages import AnyMessage
from typing import TypedDict, Annotated
import operator

class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add] # 历史消息
