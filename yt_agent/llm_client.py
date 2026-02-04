from .langchain_utils import LangChainUtils

class LLMClient:
    def __init__(self, api_base: str, model: str, temperature: float = 0.2):
        self.lc_utils = LangChainUtils(api_base=api_base, model=model, temperature=temperature)

    def generate_summary(self, title: str, description: str | None, transcript: str, max_sentences: int, language: str) -> str:
        return self.lc_utils.generate_summary(title, description, transcript, max_sentences, language)
