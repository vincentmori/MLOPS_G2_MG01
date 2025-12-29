import streamlit as st
import requests

st.set_page_config(page_title="Job Recommender G2-MG01", layout="centered")

st.title("🚀 Assistant de Recommandation de Métiers")
st.markdown("Trouvez les blocs de compétences qui correspondent à votre profil.")

with st.form("user_profile"):
    exp = st.text_area("Vos expériences passées :", placeholder="Ex: Développeur fullstack pendant 2 ans...")
    interests = st.text_area("Vos centres d'intérêt :", placeholder="Ex: Data science, Cloud Computing...")
    
    st.write("### Vos Compétences clés")
    # On peut simplifier l'ajout de skills pour la démo
    skill_1 = st.text_input("Compétence 1")
    level_1 = st.slider("Niveau 1", 1, 5, 3)
    
    submit = st.form_submit_button("Obtenir des recommandations")

if submit:
    # Construction du JSON pour l'API
    payload = {
        "experiences": exp,
        "interests": interests,
        "skills": [{"name": skill_1, "level": level_1}] if skill_1 else [],
        "top_n": 3
    }
    
    try:
        # Appel à l'API (on utilisera l'URL locale pour tester)
        response = requests.post("http://localhost:8000/predict", json=payload)
        
        if response.status_code == 200:
            results = response.json()["recommendations"]
            st.success("Voici les meilleures correspondances :")
            
            for res in results:
                with st.expander(f"🎯 {res['job']}"):
                    st.write(f"**Score de confiance :** {res['score'] * 100:.2f}%")
                    st.progress(res['score'])
        else:
            st.error("Erreur lors de la communication avec l'API.")
    except Exception as e:
        st.error(f"L'API ne semble pas répondre. Vérifiez que votre conteneur Docker tourne. ({e})")