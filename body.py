import os

from dotenv import load_dotenv
from llama_index.core import Settings
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.core import PromptTemplate

# 1. Import the already-created connection from your main file
from database_connection import sql_database
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
# 2. Setup  API Key
os.environ["GOOGLE_API_KEY"] = api_key

# 3. Configure the "Brain" (Gemini)
# We set these globally so the Query Engine knows what to use
llm = Gemini(model_name="models/gemini-2.5-flash")
embed_model = GeminiEmbedding(model_name="models/text-embedding-004")

Settings.llm = llm
Settings.embed_model = embed_model

wow_prompt = PromptTemplate(
    "You are Aadhar Insight, a sophisticated AI data partner. "
    "When you explain data, be professional, insightful, and enthusiastic. "
    "Instead of just saying 'There are 10 rows', say 'Upon analyzing the 2.2 million records, "
    "I've discovered that there are exactly 10 entries matching your criteria.' "
    "Here is the data: {query_str}"
)

# 4. Initialize the Query Engine
# It uses the 'sql_database' we imported from database_connection.py
query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database,
    tables=["aadhar"]  # Matches your table name in database_connection.py
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