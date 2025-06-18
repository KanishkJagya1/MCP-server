import streamlit as st
import requests

st.title("🌐 MCP: AI-Powered Web Query Engine")

query = st.text_input("Ask something:")
llm_provider = st.selectbox("LLM Provider", ["gemini", "claude"])
submit = st.button("Search")

if submit and query:
    try:
        response = requests.post(
            "http://localhost:5001/tool_call",
            json={"name": "fetch_web_content", "parameters": {"query": query}}
        )
        result = response.json()
        results = result.get("results", [])

        if results and "error" not in results[0]:
            st.subheader("Results:")
            for r in results:
                st.markdown(f"**{r['title']}**\n\n[{r['url']}]({r['url']})\n\n{r['description']}")
        else:
            st.warning("No results found.")
    except Exception as e:
        st.error(f"Error: {e}")
