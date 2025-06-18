import os
from flask import Flask, request, jsonify
from mcp_integration import LLMMCPBridge, handle_claude_tool_call
from dotenv import load_dotenv
load_dotenv()

PORT = int(os.getenv("PORT", 5001))
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")

app = Flask(__name__)
bridge = LLMMCPBridge(llm_provider=LLM_PROVIDER)

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "name": "MCP Server",
        "llm_provider": LLM_PROVIDER,
        "status": "running"
    })

@app.route("/tool_call", methods=["POST"])
def tool_call():
    if not request.json:
        return jsonify({"error": "Invalid request"}), 400

    tool_name = request.json.get("name")
    parameters = request.json.get("parameters", {})

    if tool_name != "fetch_web_content":
        return jsonify({"error": "Unknown tool name"}), 400

    result = handle_claude_tool_call(parameters, llm_provider=LLM_PROVIDER)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
