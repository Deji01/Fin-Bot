from datetime import date, datetime, timedelta
import os

from llama_index.core import VectorStoreIndex
from llama_index.core.retrievers import QueryFusionRetriever
from llama_index.vector_stores.timescalevector import TimescaleVectorStore
from typing import Dict, Any


class Retriever:
    """Class for retrieving data from a TimescaleDB vector store."""

    def __init__(self, output: Dict[str, Any]):
        """
        Initialize the retriever class.

        Args:
            output (Dict[str, Any]): The output parameters for the retrieval.
        """

        self.output = output
        self.vector_store_finance = TimescaleVectorStore.from_params(
            service_url=os.getenv("TIMESCALE_SERVICE_URL"),
            table_name=os.getenv("TABLE_NAME_ONE"),
            num_dimensions=384,
            time_partition_interval=timedelta(days=1),
        )

        self.vector_store_stock = TimescaleVectorStore.from_params(
            service_url=os.getenv("TIMESCALE_SERVICE_URL"),
            table_name=os.getenv("TABLE_NAME_TWO"),
            num_dimensions=384,
            time_partition_interval=timedelta(days=1),
        )

        self.index_finance = VectorStoreIndex.from_vector_store(
            self.vector_store_finance
        )
        self.index_stock = VectorStoreIndex.from_vector_store(self.vector_store_stock)

        if (output) is None or "" or {}:
            self.finance_retriever = self.index_finance.as_retriever(
                vector_store_kwargs=(
                    {
                        "start_date": datetime.combine(
                            (date.today() - timedelta(days=5)), datetime.min.time()
                        ),
                        "end_date": datetime.combine(date.today(), datetime.min.time()),
                    }
                )
            )

            self.stock_retriever = self.index_stock.as_retriever(
                vector_store_kwargs=(
                    {
                        "start_date": datetime.combine(
                            (date.today() - timedelta(days=5)), datetime.min.time()
                        ),
                        "end_date": datetime.combine(date.today(), datetime.min.time()),
                    }
                )
            )

        else:
            self.finance_retriever = self.index_finance.as_retriever(
                vector_store_kwargs=(
                    {
                        "start_date": output.date_range.start_date,
                        "end_date": output.date_range.end_date,
                    }
                )
            )

            self.stock_retriever = self.index_stock.as_retriever(
                vector_store_kwargs=(
                    {
                        "start_date": output.date_range.start_date,
                        "end_date": output.date_range.end_date,
                    }
                )
            )

    def __call__(self):
        """
        Call method to retrieve finance and stock retriever.
        """

        return self.finance_retriever, self.stock_retriever


def get_nodes(query: str, output: Dict[str, Any]):
    """
    Function to retrieve nodes based on a query using a fusion retriever.

    Args:
        query (str): The query string to retrieve nodes for.
        output (Dict[str, Any]): The output parameters for the retrieval.

    Returns:
        List[Any]: The retrieved nodes based on the query.
    """
    retriever = QueryFusionRetriever(
        [Retriever(output=output)],
        similarity_top_k=5,
        verbose=True,
    )
    nodes = retriever.retrieve(query)

    return nodes
