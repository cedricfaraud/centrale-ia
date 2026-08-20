import streamlit as st
from agents import run_orchestrateur_multi_agents

st.set_page_config(page_title="Centrale IA", layout="wide")

st.title("🧠 Centrale IA — Orchestrateur Multi‑Agents")

description = st.text_area("Décris ton projet :", height=150)

if st.button("Lancer orchestrateur multi-agents"):
    if not description.strip():
        st.error("Merci de décrire ton projet.")
    else:
        with st.spinner("Les agents travaillent..."):
            result = run_orchestrateur_multi_agents(description)

        st.subheader("📌 Résultat multi‑agents")
        st.markdown(result)
