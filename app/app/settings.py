import os

from llama_index.core import PromptTemplate
from llama_index.core.response_synthesizers import TreeSummarize
from llama_index.core.settings import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.postprocessor.cohere_rerank import CohereRerank

from .engine.prompts import PROMPT_COMPONENT_STR


def init_settings():
    """
    Initialize the settings for the model and model_name using environment variables.
    """
    model = os.getenv("MODEL", "gpt-3.5-turbo")
    model_name = os.getenv("EMBED_MODEL", "gpt-3.5-turbo")

    Settings.llm = OpenAI(model=model)
    Settings.embed_model = HuggingFaceEmbedding(model_name=model_name)
    Settings.reranker = CohereRerank()
    Settings.summarizer = TreeSummarize()
    Settings.prompt_tmpl = PromptTemplate(PROMPT_COMPONENT_STR)
