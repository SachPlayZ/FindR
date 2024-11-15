from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import TiDBVectorStore
from langchain_text_splitters import CharacterTextSplitter
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.llms.base import LLM
from pydantic import BaseModel
from typing import Any, List, Optional
import requests
import dotenv
import os

dotenv.load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
JABIR_API_KEY = os.getenv("JABIR_API_KEY")


class CustomConfig(BaseModel):
    api_url: str
    api_key: str


class CustomAPILLM(LLM):
    api_key: str = None
    api_url: str = None


    def __init__(self, config: CustomConfig, callbacks: Optional[List] = None):
        super().__init__()
        self.api_url = config.api_url
        self.api_key = config.api_key
        self.callbacks = callbacks or []

    @property
    def _llm_type(self) -> str:
        return "custom_api"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs: Any,
    ) -> str:
        headers = {
            "Content-Type": "application/json",
            "apiKey": self.api_key,
        }
        data = {"messages": [{"role": "user", "content": prompt}]}
        response = requests.post(self.api_url, json=data, headers=headers)
        response.raise_for_status()
        return response.json().get("result", {}).get("content", "")
