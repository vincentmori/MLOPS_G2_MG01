from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
import time
from sentence_transformers import SentenceTransformer, util
from src.api.model_loader import get_model

app = FastAPI(title="MLOps Job Recommender API")

# --- Stockage des KPIs en mémoire ---
kpi_store = {
    "total_requests": 0,
    "total_latency": 0.0,
    "last_confidence_score": 0.0,
    "model_name": "multi-qa-mpnet-base-dot-v1"
}

# --- Schémas de données ---
class Skill(BaseModel):
    name: str
    level: int

class UserInput(BaseModel):
    experiences: str
    interests: str
    skills: list[Skill]
    top_n: int = 3

# --- Endpoints de Métriques ---
@app.get("/metrics")
def get_all_metrics():
    """Résumé global des KPIs"""
    avg_latency = kpi_store["total_latency"] / kpi_store["total_requests"] if kpi_store["total_requests"] > 0 else 0
    return {
        "system": {
            "requests": kpi_store["total_requests"],
            "avg_latency": round(avg_latency, 4)
        },
        "model": {
            "confidence_score": round(kpi_store["last_confidence_score"], 4),
            "version": kpi_store["model_name"]
        }
    }

@app.get("/metrics/system")
def get_system_metrics():
    """Métriques de performance brute (Throughput & Latency)"""
    avg_latency = kpi_store["total_latency"] / kpi_store["total_requests"] if kpi_store["total_requests"] > 0 else 0
    return {
        "throughput": kpi_store["total_requests"],
        "latency_avg_seconds": round(avg_latency, 4)
    }

@app.get("/metrics/model")
def get_model_metrics():
    """Métriques spécifiques au ML (Score de confiance)"""
    return {
        "last_prediction_confidence": round(kpi_store["last_confidence_score"], 4),
        "status": "active"
    }

# --- Endpoint de Prédiction avec Logique de Pondération ---
# Chargement global au démarrage
artifacts = get_model()
model = SentenceTransformer(artifacts['model_name'])
block_embeddings = artifacts['block_embeddings']
df_ref = artifacts['df_reference']

@app.post("/predict")
def predict(data: UserInput):
    start_time = time.time()
    try:
        # Logique de pondération des compétences
        exp_emb = model.encode(data.experiences, convert_to_tensor=True)
        int_emb = model.encode(data.interests, convert_to_tensor=True)
        
        user_emb = (exp_emb + int_emb) / 2

        if data.skills:
            weighted_skills = []
            for s in data.skills:
                weighted_skills.extend([s.name] * s.level)
            
            skills_text = " ".join(weighted_skills)
            skill_emb = model.encode(skills_text, convert_to_tensor=True)
            user_emb = user_emb + skill_emb

        user_emb = torch.nn.functional.normalize(user_emb, p=2, dim=0) 

        # Calcul de similarité
        # block_embeddings a été pré-calculé dans train.py
        similarities = util.cos_sim(user_emb, block_embeddings)[0]

        # Top N
        top_k = torch.topk(similarities, k=data.top_n)
        
        results = []
        for score, idx in zip(top_k.values, top_k.indices):
            results.append({
                "job": df_ref.iloc[idx.item()]['Job'],
                "score": round(float(score), 4)
            })

        # --- Mise à jour des KPIs ---
        latency = time.time() - start_time
        kpi_store["total_requests"] += 1
        kpi_store["total_latency"] += latency
        kpi_store["last_confidence_score"] = float(top_k.values[0])

        return {
            "recommendations": results,
            "metadata": {"latency": round(latency, 4)}
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "healthy"}