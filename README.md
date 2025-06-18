# 🌐 MCP Server – Multi-LLM Web Search Bridge

A lightweight, extensible backend that leverages **Google Gemini** and **Anthropic Claude** to perform intelligent web-assisted queries through DuckDuckGo. The MCP Server extracts meaningful search topics from natural language input and fetches relevant information from the internet.

## ✨ Features

- **Multi-LLM Support**: Compatible with Google Gemini and Anthropic Claude
- **Intelligent Query Processing**: Extracts search topics from natural language
- **Web Search Integration**: Uses DuckDuckGo for reliable web results
- **Multiple Interfaces**: Flask API, CLI tool, and Streamlit frontend
- **Easy Configuration**: Environment-based setup with provider switching

## 🏗️ Project Structure

```
MCP-server/
├── mcp_server.py          # Flask API server
├── mcp_integration.py     # Core logic (LLM handling + search)
├── ask_llm.py            # Command-line interface
├── streamlit_app.py      # Interactive web frontend
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (not committed)
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google Gemini API key or Anthropic Claude API key
- Internet connection for web searches

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/KanishkJagya1/MCP-server.git
   cd MCP-server
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_google_gemini_api_key_here
   CLAUDE_API_KEY=your_anthropic_api_key_here
   LLM_PROVIDER=gemini  # Options: "gemini" or "claude"
   PORT=5001
   ```

## 🖥️ Usage

### Flask API Server

Start the backend server:
```bash
python mcp_server.py
```

**Available endpoints:**
- `GET /health` - Health check
- `GET /` - Server info
- `POST /tool_call` - Web search endpoint

**Example API call:**
```bash
curl -X POST http://localhost:5001/tool_call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "fetch_web_content",
    "parameters": {
      "query": "latest Mars discoveries"
    }
  }'
```

### Command Line Interface

Ask questions directly from the terminal:
```bash
python ask_llm.py "What are the latest developments in AI?"
```

### Streamlit Frontend

Launch the interactive web interface:
```bash
streamlit run streamlit_app.py
```

Then open http://localhost:8501 in your browser.

**Example queries:**
- "What has NASA discovered on Mars recently?"
- "Tell me about the latest AI breakthroughs"
- "What's happening in renewable energy?"

## 🤖 Supported LLM Providers

| Provider | Model | Notes |
|----------|-------|-------|
| Google Gemini | gemini-pro | Fast and efficient |
| Anthropic Claude | claude-3-sonnet | Strong structured responses |

Switch between providers by updating the `LLM_PROVIDER` in your `.env` file.

## 📋 API Response Format

```json
{
  "results": [
    {
      "title": "Example Search Result",
      "url": "https://example.com",
      "description": "Description of the search result..."
    }
  ]
}
```

## 🚀 Deployment

### Local Development
The server runs on `localhost:5001` by default. Configure the port in your `.env` file.

### Production Deployment
Deploy on platforms like:
- **Streamlit Cloud** (for frontend)
- **Render** / **Railway** / **Replit** (for backend)
- **Docker** (containerized deployment)

For external access, update the Streamlit app to point to your public Flask URL.

## 🎯 Use Cases

- **Research Assistance**: Automated information gathering
- **Academic Fact-Checking**: Verify claims and sources
- **Content Exploration**: Discover related topics and trends
- **News Analysis**: Stay updated with current events
- **Smart Search Bots**: Build intelligent search applications

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | Required |
| `CLAUDE_API_KEY` | Anthropic Claude API key | Required |
| `LLM_PROVIDER` | LLM provider to use | `gemini` |
| `PORT` | Flask server port | `5001` |

### Git Configuration

The project includes a `.gitignore` file to exclude sensitive files:
```gitignore
__pycache__/
*.pyc
.env
.venv/
*.log
.vscode/
.idea/
```

If you accidentally committed files before adding `.gitignore`:
```bash
git rm -r --cached .
git add .
git commit -m "Apply .gitignore changes"
```

## 🛠️ Development

### Testing the API
Test endpoints manually or create automated tests:
```bash
# Health check
curl http://localhost:5001/health

# Search query
curl -X POST http://localhost:5001/tool_call \
  -H "Content-Type: application/json" \
  -d '{"name": "fetch_web_content", "parameters": {"query": "test query"}}'
```

### Adding New Features
The modular structure makes it easy to:
- Add new LLM providers in `mcp_integration.py`
- Extend API endpoints in `mcp_server.py`
- Enhance the frontend in `streamlit_app.py`

## 📝 Roadmap

- [ ] Add result summarization using LLMs
- [ ] Implement logging and error tracking
- [ ] Add caching for repeated queries
- [ ] UI enhancements (dark mode, result cards)
- [ ] Support for additional search engines
- [ ] Batch query processing
- [ ] Result export functionality

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Kanishk Jagya**  
Thapar Institute of Engineering and Technology  
📧 [GitHub Profile](https://github.com/KanishkJagya1)

## 🙏 Acknowledgments

- Google Gemini and Anthropic Claude for LLM capabilities
- DuckDuckGo for search functionality
- Streamlit for the web interface framework
- Flask for the API backend

---

**Need help?** Open an issue or reach out via GitHub!