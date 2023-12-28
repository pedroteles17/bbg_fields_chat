# Chroma has a dependency problem with older version of sqlite3
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
from rag_module import VectorDB, QueryEngine

with st.sidebar:
    "[View the source code](https://github.com/pedroteles17/bbg_fields_chat)"

st.title("Non-Official Bloomberg FLDS Navigator 🌐💹")
st.caption("RAG System for Efficient Bloomberg Field Analysis")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

if "query_engine" not in st.session_state:
    index = VectorDB(path="./chroma_db", collection_name="bloomberg_fields").initialize_index()
    st.session_state["query_engine"] = QueryEngine(index, similarity_top_k=5).initialize_query_engine()

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    msg = st.session_state.query_engine.query(prompt).response
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)