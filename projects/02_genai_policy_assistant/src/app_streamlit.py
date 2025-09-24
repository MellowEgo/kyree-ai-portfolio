import streamlit as st
from retriever import retrieve
from chains import answer

st.title("Policy Assistant (RAG Demo)")
q = st.text_input("Ask a policy question:")
if q:
    ctx = retrieve(q)
    out = answer(q)
    st.write("Answer:", out['answer'])
    st.write("Sources:", out['sources'])
    st.write("Context:", ctx)