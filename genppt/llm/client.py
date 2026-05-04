from typing import Optional

from langchain_openai import AzureChatOpenAI, ChatOpenAI

from genppt.config import settings


def get_llm(temperature: float = 0.7):
    """
    Return a LangChain chat model.
    Prefers Azure OpenAI; falls back to any OpenAI-compatible endpoint.
    """
    if settings.azure_openai_api_key and settings.azure_openai_endpoint:
        return AzureChatOpenAI(
            azure_endpoint=settings.azure_openai_endpoint,
            api_key=settings.azure_openai_api_key,
            azure_deployment=settings.azure_openai_deployment_name,
            api_version=settings.azure_openai_api_version,
            temperature=temperature,
        )

    if settings.openai_api_key:
        kwargs = {"api_key": settings.openai_api_key, "temperature": temperature}
        if settings.openai_base_url:
            kwargs["base_url"] = settings.openai_base_url
        return ChatOpenAI(**kwargs)

    raise ValueError(
        "No LLM configured. Set AZURE_OPENAI_API_KEY + AZURE_OPENAI_ENDPOINT "
        "or OPENAI_API_KEY in your .env file."
    )
