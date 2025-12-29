import joblib
import os

# Variable globale pour stocker le modèle en mémoire
_model = None

def get_model():
    """Charge le modèle une seule fois et le garde en mémoire (Singleton)"""
    global _model
    if _model is None:
        model_path = os.path.join("models", "recommender_model.joblib")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"L'artefact {model_path} est introuvable. "
                                    "Lancez d'abord le pipeline d'entraînement.")
        
        print(f"Chargement du modèle depuis {model_path}...")
        _model = joblib.load(model_path)
    
    return _model