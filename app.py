import streamlit as st
from body import ask_aadhar

# 1. Page Configuration
st.set_page_config(page_title="Aadhar Insight AI", page_icon="📊")

st.title("🇮🇳 Aadhar Insight AI")
st.markdown("Query 2.2M Aadhar records using plain English.")

# 2. Sidebar for info
with st.sidebar:
    st.header("System Status")
    st.success("Connected to PostgreSQL")
    st.info("Model: Gemini-1.5-Flash")

# 3. Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. User Input
if prompt := st.chat_input("Ex: What is the failure rate in the North region?"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 5. Get AI Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking and querying database..."):
            try:
                # Call your logic from body.py
                response = ask_aadhar(prompt)

                # Show the SQL generated (Data Analysts love transparency!)
                sql_used = response.metadata.get('sql_query', 'No SQL generated')
                st.code(sql_used, language="sql")

                # Show the final answer
                full_response = response.response
                st.markdown(full_response)

                # Save to history
                st.session_state.messages.append({"role": "assistant", "content": full_response})

            except Exception as e:
                st.error(f"Error: {e}")