from app.engine.pipeline import PipelineFactory


async def get_chat_engine() -> str:
    """
    Asynchronous function to get the chat engine. It does not take any parameters and returns a string.
    """
    p = PipelineFactory()

    # Initialize an empty list to store outputs
    output_list = []

    response = await p.arun(
        input="What are some of the recent major events that have occurred?"
    )

    # Iterate over the async generator and store the outputs
    async for item in response:
        output_list.append(item)

    return output_list[-1].message.content
