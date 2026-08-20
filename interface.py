import streamlit as st
from agents import orchestrateur, architecte, dev, po, ivvq

st.set_page_config(page_title="Centrale IA", layout="wide")

st.title("🧠 Centrale IA — Chef de Projet")

description = st.text_area("Décris ton projet :", height=150)

if st.button("Lancer le projet"):
    if not description.strip():
        st.error("Merci de décrire ton projet.")
    else:
        with st.spinner("L'équipe IA travaille..."):

            synthese = orchestrateur(
                f"Tu es chef de projet. Reformule clairement le besoin suivant : {description}"
            )

            backlog = po(
                f"À partir de ce besoin reformulé, crée un backlog complet, structuré en user stories : {synthese}"
            )

            archi = architecte(
                f"À partir de ce besoin reformulé, propose une architecture technique complète, modulaire : {synthese}"
            )

            code = dev(
                f"Commence à implémenter le cœur du système en respectant l'architecture suivante : {archi}"
            )

            tests = ivvq(
                f"Propose un plan de tests IVVQ détaillé pour valider ce système : {synthese}"
            )

        st.subheader("📌 Synthèse du chef de projet")
        st.write(synthese)

        st.subheader("📌 Backlog (PO)")
        st.write(backlog)

        st.subheader("📌 Architecture (Architecte)")
        st.write(archi)

        st.subheader("📌 Code (Développeur)")
        st.code(code, language="python")

        st.subheader("📌 Tests IVVQ")
        st.write(tests)
