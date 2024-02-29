from llama_index.core.llms import MessageRole
from pydantic import BaseModel
from typing import List


class _Message(BaseModel):
    role: MessageRole
    content: str


class _ChatData(BaseModel):
    messages: List[_Message]
