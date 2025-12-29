import pandas as pd
import os

def clean_data(input_path, output_path):
    print("Nettoyage des données...")
    df = pd.read_csv(input_path)
    
    # Exemple de transformation simple : suppression des lignes vides
    df_cleaned = df.dropna(subset=['Titre'])
    
    # Créer le dossier pour les données finales
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    df_cleaned.to_csv(output_path, index=False)
    print(f"Données nettoyées sauvegardées dans : {output_path}")

if __name__ == "__main__":
    clean_data("data/raw/Competency_block.csv", "data/processed/clean_competencies.csv")