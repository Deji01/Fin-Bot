from llama_index.program.openai import OpenAIPydanticProgram
from llama_index.core import ChatPromptTemplate
from llama_index.core.llms import ChatMessage
from llama_index.core.settings import Settings

from .model import FinancialMarketData
from .prompts import SYSTEM_PROMPT, USER_PROMPT


def get_financial_data(input: str):
    """
    A function to get financial data based on a given input string.
    """
    prompt = ChatPromptTemplate(
        message_templates=[
            ChatMessage(
                role="system",
                content=SYSTEM_PROMPT,
            ),
            ChatMessage(
                role="user", 
                content=USER_PROMPT
            ),
        ],
    )

    program = OpenAIPydanticProgram.from_defaults(
        output_cls=FinancialMarketData, prompt=prompt, llm=Settings.llm, verbose=True
    )
    
    return program(question=input)
