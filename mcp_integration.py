import os
import re
import json
import requests
from typing import Dict, List, Any, Literal
from dataclasses import dataclass, asdict
import anthropic
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

DUCKDUCKGO_ENDPOINT = "https://api.duckduckgo.com"
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

LLMProvider = Literal["claude", "gemini"]

@dataclass
class DDGRequest:
    q: str
    format: str = "json"
    no_html: int = 1
    skip_disambig: int = 1

@dataclass
class WebResult:
    title: str
    url: str
    description: str

class MCPClient:
    def __init__(self, endpoint=DUCKDUCKGO_ENDPOINT):
        self.endpoint = endpoint

    def search(self, query: str) -> List[WebResult]:
        params = asdict(DDGRequest(q=query))
        try:
            res = requests.get(self.endpoint, params=params)
            res.raise_for_status()
            data = res.json()

            if not data.get("Abstract"):
                return []

            return [
                WebResult(
                    title=data.get("Heading", ""),
                    url=data.get("AbstractURL", ""),
                    description=data.get("Abstract", "")
                )
            ]
        except Exception as e:
            print("Search error:", e)
            return []

class LLMMCPBridge:
    def __init__(self, llm_provider: LLMProvider = "gemini"):
        self.llm_provider = llm_provider
        self.mcp_client = MCPClient()

        if llm_provider == "claude":
            self.claude_client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
        elif llm_provider == "gemini":
            if not GEMINI_API_KEY:
                raise ValueError("Missing GEMINI_API_KEY")
            genai.configure(api_key=GEMINI_API_KEY)
            self.gemini_model = genai.GenerativeModel("gemini-pro")

    def extract_queries(self, user_input: str) -> List[str]:
        if self.llm_provider == "gemini":
            return self._extract_with_gemini(user_input)
        return []

    def _extract_with_gemini(self, message: str) -> List[str]:
        try:
            prompt = (
                "Extract search queries from this user request. "
                "Respond with a JSON like: {\"queries\": [\"query1\", \"query2\"]}\n\n"
                f"User: {message}"
            )
            res = self.gemini_model.generate_content(prompt)
            raw = res.text.strip()

            json_match = re.search(r'```(?:json)?\s*({.*?})\s*```', raw, re.DOTALL)
            json_str = json_match.group(1) if json_match else raw
            parsed = json.loads(json_str)
            return parsed.get("queries", [])
        except Exception as e:
            print("Gemini parsing error:", e)
            return []

def handle_claude_tool_call(tool_params: Dict[str, Any], llm_provider: LLMProvider = "gemini") -> Dict[str, Any]:
    query = tool_params.get("query", "")
    if not query:
        return {"error": "No query provided"}

    bridge = LLMMCPBridge(llm_provider=llm_provider)
    results = bridge.mcp_client.search(query)

    return {
        "results": [asdict(r) for r in results] if results else [{"error": "No answer found"}]
    }
