import sys
import os
import argparse
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()


def check_gemini_api_key():
    return bool(os.environ.get("GEMINI_API_KEY"))

def ask_gemini(prompt):
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    
    model = genai.GenerativeModel("gemini-1.5-pro")
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error querying Gemini: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="Ask Gemini questions with web search capability")
    parser.add_argument("query", nargs="*", help="The question to ask Gemini")
    args = parser.parse_args()

    if not check_gemini_api_key():
        print("Error: GEMINI_API_KEY is missing from environment")
        sys.exit(1)

    query = " ".join(args.query) if args.query else input("Ask Gemini: ")

    print(f"Searching for {query}")

    answer = ask_gemini(query)
    print("Answer:", answer)

if __name__ == "__main__":
    main()
