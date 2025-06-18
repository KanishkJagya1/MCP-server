import os
import json
import requests
import time
from typing import Dict, List, Any, Optional
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()


GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
MCP_SERVER_URL = os.environ.get("MCP_SERVER_URL", "http://localhost:5001")

class GeminiClient:
    def __init__(self, model: str = "gemini-pro"):
        if not GEMINI_API_KEY:
            raise ValueError("Gemini API key missing from environment")

        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(model)
        self._check_mcp_server()

    def _check_mcp_server(self) -> bool:
        try:
            response = requests.get(f"{MCP_SERVER_URL}/health", timeout=2)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def send_message(self, message: str, history: Optional[List[str]] = None) -> str:
        if history is None:
            history = []

        full_prompt = "\n".join(history + [message])

        print("Sending request to Gemini...")

        try:
            response = self.model.generate_content(full_prompt)
            text = response.text.strip()

            if "fetch_web_content" in text.lower():
                # Basic simulation of a tool call
                tool_call = self._extract_tool_call(text)
                print(f"Tool call detected: {tool_call}")

                tool_response = self._handle_tool_call(tool_call)
                print(f"Tool response: {tool_response}")

                summary_prompt = f"""
Given the user query: "{message}" and the following information from the tool:

{tool_response.get("results", [{}])[0].get("description", "No data returned")}

Please summarize the response and stop calling tools.
"""
                return self.send_message(summary_prompt, history + [message, text])
            
            return text

        except Exception as e:
            return f"Error during Gemini API call: {e}"

    def _extract_tool_call(self, response_text: str) -> Dict[str, Any]:
        # VERY simple simulated parser - ideally use structured output
        query_start = response_text.lower().find("query:")
        if query_start != -1:
            query = response_text[query_start + len("query:"):].strip().splitlines()[0]
            return {"name": "fetch_web_content", "parameters": {"query": query}}
        return {"name": "", "parameters": {}}

    def _handle_tool_call(self, tool_call: Dict[str, Any]) -> Dict[str, Any]:
        tool_name = tool_call.get("name")
        tool_params = tool_call.get("parameters")

        if not self._check_mcp_server():
            return {"error": "MCP server not available"}

        max_retries = 3
        retry_count = 0

        while retry_count < max_retries:
            try:
                response = requests.post(
                    f"{MCP_SERVER_URL}/tool_call",
                    json={"name": tool_name, "parameters": tool_params},
                    timeout=10
                )
                response.raise_for_status()
                return response.json()

            except Exception as e:
                retry_count += 1
                if retry_count < max_retries:
                    time.sleep(2 ** retry_count)
                else:
                    return {"error": "MCP server failed after retries"}

    def get_final_answer(self, message: str) -> str:
        return self.send_message(message)
