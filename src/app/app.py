import streamlit as st
import requests

# --- Configuration de la page ---
st.set_page_config(page_title="Job Recommender G2-MG01", layout="wide", page_icon="🚀")

# --- URL App Runner en dur (pas de secrets à configurer) ---
API_BASE_URL = "https://wiavajvtnx.us-east-1.awsapprunner.com"

st.title("🚀 Assistant de Recommandation de Métiers")
st.markdown("Identifiez les opportunités qui correspondent le mieux à votre expertise technique.")

# --- Barre latérale : Monitoring (KPIs Fiche 2) ---
with st.sidebar:
    st.header("📊 Monitoring API (AWS)")
    st.write(f"📡 API : `{API_BASE_URL.split('//')[-1]}`")
    
    if st.button("Actualiser les métriques"):
        try:
            # Appel à l'endpoint /metrics de ton FastAPI sur AWS
            m_res = requests.get(f"{API_BASE_URL}/metrics", timeout=5)
            if m_res.status_code == 200:
                data = m_res.json()
                st.metric("Requêtes totales", data["system"]["requests"])
                st.metric("Latence moyenne", f"{data['system']['avg_latency']}s")
                st.success("Métriques à jour ✅")
        except:
            st.error("L'API AWS ne répond pas.")

# --- Formulaire principal ---
col1, col2 = st.columns([2, 1])

with col1:
    with st.form("user_profile"):
        exp = st.text_area("💼 Vos expériences passées :", placeholder="Ex: Développeur fullstack pendant 2 ans...")
        interests = st.text_area("🎯 Vos centres d'intérêt :", placeholder="Ex: Data science, NLP...")
        
        st.write("---")
        st.subheader("🛠️ Compétence technique principale")
        s1 = st.text_input("Compétence (ex: Python)", placeholder="Python")
        l1 = st.slider("Niveau de maîtrise (1-5)", 1, 5, 3)
        
        submit = st.form_submit_button("Calculer la compatibilité")

# --- Logique de recommandation ---
if submit:
    if not exp or not interests:
        st.warning("Veuillez remplir les champs 'Expériences' et 'Intérêts'.")
    else:
        payload = {
            "experiences": exp,
            "interests": interests,
            "skills": [{"name": s1, "level": l1}] if s1 else [],
            "top_n": 3
        }
        
        with st.spinner("Analyse sémantique sur AWS..."):
            try:
                # Requête POST vers ton App Runner
                response = requests.post(f"{API_BASE_URL}/predict", json=payload, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    results = data["recommendations"]
                    
                    st.success("Top 3 des métiers recommandés :")
                    
                    for res in results:
                        with st.expander(f"🎯 {res['job']}", expanded=True):
                            score_pct = res['score'] * 100
                            st.write(f"**Compatibilité :** {score_pct:.2f}%")
                            st.progress(res['score'])
                else:
                    st.error(f"Erreur API ({response.status_code})")
            except Exception as e:
                st.error("L'API sur AWS est injoignable. Vérifiez le statut 'Running' sur App Runner.")

with col2:
    st.info("""
    **Architecture MLOps**
    - **Frontend** : Streamlit Cloud
    - **Backend** : FastAPI sur AWS App Runner
    - **Modèle** : SBERT (Sentence-Transformers)
    """)
    st.image("https://upload.wikimedia.org/wikipedia/commons/0/05/Scikit_learn_logo_small.svg", width=80)