import streamlit as st
from body import ask_aadhar
import pandas as pd
import plotly.express as px
from database_connection import engine


# 1. Page Configuration
st.set_page_config(page_title="Aadhar Insight AI", page_icon="🏛️", layout="wide")

# 2. Custom CSS for "Elegant Light Mode"
st.markdown("""
    <style>
    /* White/Light Grey Background */
    /* 1. Main App Background */
    .stApp {
        background-color: #FFFFFF; /* Pure White background */
        color: #1E1E1E; /* Dark Grey text for readability */
    }
    
    /* 2. Top Header Styling */
    .main-header {
        text-align: center;
        font-size: 3.5rem;
        font-weight: 800;
        /* Change the hex codes below for different blue shades */
        background: -webkit-linear-gradient(#007BFF, #00C6FF); 
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    /* 3. Sub-text Styling */
    .sub-text {
        text-align: center;
        color: #5F7D96; /* Muted steel blue */
        font-size: 1.2rem;
        font-weight: 400;
        margin-bottom: 2rem;
    }

    /* 4. Chat Bubble Styling */
    .stChatMessage {
        background-color: #F8FAFC; /* Extremely light blue-tinted white */
        border-radius: 20px;
        border: 1px solid #E2E8F0; /* Soft border */
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); /* Subtle shadow for "Wow" effect */
    }

    /* 5. Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #F1FBFF; /* Very light sky blue sidebar */
        border-right: 1px solid #D1E9FF;
    }
    
    /* 6. Code Block Styling (Generated SQL) */
    code {
        color: #0366d6 !important; /* GitHub-style blue code */
        background-color: #f6f8fa !important;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. UI Header
st.markdown('<h1 class="main-header">Aadhar Insight</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">Sophisticated Data Intelligence</p>', unsafe_allow_html=True)
st.divider()

# 4. Chat Interface Logic
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. User Input and Logic
if prompt := st.chat_input("Ask about Aadhar data..."):
    # Store user query
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🤖 Analyzing 2.2M Rows..."):
            try:
                response = ask_aadhar(prompt)
                sql_query = response.metadata.get('sql_query')

                # 1. Main AI Analysis text (Always visible)
                st.subheader("💡 Analysis")
                st.markdown(response.response)

                if sql_query:
                    import pandas as pd
                    import plotly.express as px
                    from database_connection import engine

                    df = pd.read_sql(sql_query, engine)

                    if not df.empty:
                        # --- BOX 1: DOWNLOAD (Visible Button) ---
                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 Download Result CSV",
                            data=csv,
                            file_name='aadhar_export.csv',
                            mime='text/csv',
                        )

                        # --- BOX 2: VISUALIZATION (Expander) ---
                        if len(df.columns) >= 2 and len(df) > 1:
                            with st.expander("📊 View Data Visualization"):
                                fig = px.bar(
                                    df,
                                    x=df.columns[0],
                                    y=df.columns[1],
                                    template="plotly_white",
                                    color_discrete_sequence=['#007BFF']
                                )
                                st.plotly_chart(fig, use_container_width=True)

                        # --- BOX 3: RAW DATA (Expander) ---
                        with st.expander("🔍 View Raw Data Table"):
                            st.dataframe(df, use_container_width=True)

                        # --- BOX 4: SQL CODE (Expander) ---
                        with st.expander("💻 View Generated SQL Query"):
                            st.code(sql_query, language="sql")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response.response,
                    "sql": sql_query
                })

            except Exception as e:
                st.error(f"Error: {e}")
# 6. Sidebar for Metadata Info
with st.sidebar:
    st.title("🏛️ Aadhar Insight")
    st.markdown("---")
    st.markdown("### 🔍 What can I ask?")
    st.write("""
    Try asking about:
    - **Counts:** 'Total enrollees by State'
    - **Failures:** 'Top 5 districts with biometric errors'
    - **Trends:** 'Monthly enrollment progress'
    """)
    st.markdown("---")
    st.info("System optimized for PostgreSQL processing on 2.2M records.")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()