import pandas as pd
from sentence_transformers import SentenceTransformer, util
import joblib
import os
import json
import torch

def train_model():
    # 1. Lire les données finales
    input_path = "data/processed/clean_competencies.csv"
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Fichier {input_path} introuvable. Lancez d'abord le pipeline !")
    
    # Lecture du CSV 
    df = pd.read_csv(input_path)
    
    # 2. Entraîner le modèle
    print("Chargement du modèle SentenceTransformer...")
    model = SentenceTransformer('multi-qa-mpnet-base-dot-v1')
    
    # On gère les éventuels noms de colonnes avec/sans majuscules pour être robuste
    job_col = 'Job' if 'Job' in df.columns else 'job'
    comp_col = 'Competences' if 'Competences' in df.columns else 'competences'
    
    df['combined_text'] = df[job_col].fillna('') + " : " + df[comp_col].fillna('')
    
    print(f"Génération des embeddings pour {len(df)} blocs de compétences...")
    block_embeddings = model.encode(df['combined_text'].tolist(), convert_to_tensor=True)
    
    # 3. Générer le rapport de performance (KPI d'entraînement)
    # Calcul de la similarité cosinus pour le rapport
    sample_sim = util.cos_sim(block_embeddings[0:1], block_embeddings)
    
    report = {
        "model_name": "multi-qa-mpnet-base-dot-v1",
        "num_records": len(df),
        "embedding_dimension": int(block_embeddings.shape[1]),
        "status": "Success",
        "sample_similarity_mean": float(sample_sim.mean())
    }
    
    os.makedirs("reports", exist_ok=True)
    with open("reports/train_report.json", "w") as f:
        json.dump(report, f, indent=4)
    print("✅ Rapport généré dans /reports/train_report.json")

    # 4. Exporter les artefacts pour l'API
    os.makedirs("models", exist_ok=True)
    model_artifacts = {
        "model_name": "multi-qa-mpnet-base-dot-v1",
        "block_embeddings": block_embeddings,
        "df_reference": df # Contient Job, Competences et combined_text
    }
    
    joblib.dump(model_artifacts, "models/recommender_model.joblib")
    print("🚀 Modèle exporté : models/recommender_model.joblib")

if __name__ == "__main__":
    train_model()