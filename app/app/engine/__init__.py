from app.engine.pipeline import PipelineFactory


async def build_chat_engine_pipeline() -> PipelineFactory:
    """
    Asynchronously builds the chat engine pipeline.

    Returns:
        PipelineFactory: The chat engine pipeline factory.
    """

    p = PipelineFactory()

    return p()
