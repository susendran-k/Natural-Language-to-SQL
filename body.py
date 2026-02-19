import os
from llama_index.core import Settings
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core.query_engine import NLSQLTableQueryEngine

# 1. Import the already-created connection from your main file
from main import sql_database

# 2. Setup your API Key
os.environ["GOOGLE_API_KEY"] = "your-key"

# 3. Configure the "Brain" (Gemini)
# We set these globally so the Query Engine knows what to use
llm = Gemini(model_name="models/gemini-2.5-flash")
embed_model = GeminiEmbedding(model_name="models/text-embedding-004")

Settings.llm = llm
Settings.embed_model = embed_model

# 4. Initialize the Query Engine
# It uses the 'sql_database' we imported from main.py
query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database,
    tables=["aadhar"]  # Matches your table name in main.py
)


def ask_aadhar(question):
    """
    Function to be called by your future UI.
    It takes English, returns the AI's summary.
    """
    response = query_engine.query(question)
    return response


# --- Quick Test ---
if __name__ == "__main__":
    print("\n--- Testing Aadhar Insight ---")
    user_q = "How many rows are in the aadhar table?"
    result = ask_aadhar(user_q)

    print(f"SQL Generated: {result.metadata.get('sql_query')}")
    print(f"AI Response: {result.response}")