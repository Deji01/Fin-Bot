from llama_index.core.query_pipeline import InputComponent, QueryPipeline
from llama_index.core.settings import Settings

from .components import date_component, node_component


class PipelineFactory:
    def __call__(self):
        """
        Call method to retrieve querypipeline object.
        """

        modules = {
            "input": InputComponent(),
            "date_component": date_component,
            "node_component": node_component,
            "reranker": Settings.reranker,
            "summarizer": Settings.summarizer,
            "prompt_template": Settings.prompt_tmpl,
            "llm_component": Settings.llm.as_query_component(streaming=True),
        }

        # Create the DAG query pipeline
        p = QueryPipeline(verbose=True)
        p.add_modules(modules)

        # Draw links between modules
        p.add_link("input", "date_component")

        p.add_link("date_component", "node_component", dest_key="output")
        p.add_link("input", "node_component", dest_key="query")

        p.add_link("node_component", "reranker", dest_key="nodes")
        p.add_link("input", "reranker", dest_key="query_str")

        p.add_link("reranker", "summarizer", dest_key="nodes")
        p.add_link("input", "summarizer", dest_key="query_str")

        p.add_link("summarizer", "prompt_template", dest_key="context")
        p.add_link("input", "prompt_template", dest_key="input")

        p.add_link("prompt_template", "llm_component")

        return p

