from datetime import date

SYSTEM_PROMPT = (
    f"Today is {date.today()}. You are a financial and stock market expert that provides valid / verifyable stock market data and information."
    "You are particularly skilled at extracting information from a user's question using stock and financial market terminology. Provide valid data."
)

USER_PROMPT = (
    "He is the question for you to carry out information extraction: \n"
    "<question>\n"
    "{question}\n"
    "<\question>"
)

PROMPT_COMPONENT_STR = (
    "use the following\n"
    "<context>\n"
    "{context}"
    "</context>\n"
    "to answer the the following question\n"
    "<question>\n"
    "{input}"
    "</question>"
)
