from llama_index.core.query_pipeline import FnComponent

from .loader import get_financial_data
from .retriever import get_nodes

date_component = FnComponent(
    fn=get_financial_data, output_key="query_output", input_key="input"
)
node_component = FnComponent(
    fn=get_nodes, output_key="nodes", input_keys=["input", "output"]
)
