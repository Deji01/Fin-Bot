from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Depends, Request
from app.engine import build_chat_engine_pipeline
from app.engine.pipeline import PipelineFactory

chat_router = r = APIRouter()


@r.post("")
async def chat(
    request: Request,
    input: str,
    chat_engine_pipeline: PipelineFactory = Depends(build_chat_engine_pipeline),
):
    """
    A function that generates events from the request input and yields content tokens.
    Parameters:
        request: Request - the request input
    Returns:
        token: str
    """
    response = await chat_engine_pipeline.arun(input=input)

    async def event_generator(request: Request):
        """
        A function that generates events from the request input and yields content tokens.
        Parameters:
            request: Request - the request input
        Returns:
            token: str
        """
        try:
            # Assuming response is a generator
            async for token in response.message.content.encode():
                # Check if client is disconnected
                if await request.is_disconnected():
                    break
                # Yield content token
                yield token
        except Exception as e:
            # Handle any errors
            print(f"An error occurred: {e}")

    return StreamingResponse(event_generator(request=request), media_type="text/plain")
