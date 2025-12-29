import pandas as pd
from sentence_transformers import SentenceTransformer, util
import joblib
import os
import json
import torch

def train_model():
    # 1. Lire les données finales (venant de src/data/clean_transform.py)
    input_path = "data/processed/clean_competencies.csv"
    if not os.path.exists(input_path):
        raise FileNotFoundError("Lancez d'abord le pipeline de données !")
    
    df = pd.read_csv(input_path)
    
    # 2. Entraîner le modèle (Générer les embeddings de référence)
    print("Chargement du modèle SentenceTransformer...")
    # On utilise ton modèle spécifique
    model = SentenceTransformer('multi-qa-mpnet-base-dot-v1')
    
    # Préparation du texte comme dans ton analyse.py
    df['combined_text'] = df['Titre'].fillna('') + " " + df['Compétences'].fillna('')
    
    print("Génération des embeddings pour les blocs de compétences...")
    # C'est ici l'étape d'"entraînement" : on fige la connaissance des blocs
    block_embeddings = model.encode(df['combined_text'].tolist(), convert_to_tensor=True)
    
    # 3. Générer un rapport de performance
    # On calcule la similarité interne pour vérifier la qualité des données
    sample_sim = util.cos_sim(block_embeddings[0:1], block_embeddings)
    
    report = {
        "model_name": "multi-qa-mpnet-base-dot-v1",
        "num_records": len(df),
        "embedding_dimension": block_embeddings.shape[1],
        "status": "Success",
        "sample_similarity_mean": float(sample_sim.mean())
    }
    
    os.makedirs("reports", exist_ok=True)
    with open("reports/train_report.json", "w") as f:
        json.dump(report, f, indent=4)
    print("Rapport généré dans /reports.")

    # 4. Exporter le modèle dans models/
    os.makedirs("models", exist_ok=True)
    model_artifacts = {
        "model_name": "multi-qa-mpnet-base-dot-v1", # Pour que l'API sache quoi charger
        "block_embeddings": block_embeddings,
        "df_reference": df
    }
    
    joblib.dump(model_artifacts, "models/recommender_model.joblib")
    print("Modèle exporté avec succès dans models/recommender_model.joblib")

if __name__ == "__main__":
    train_model()