import os
import boto3
from dotenv import load_dotenv

# Charger les variables du fichier .env (uniquement en local)
load_dotenv()

def download_from_s3(bucket_name, s3_file_name):
    # boto3 va maintenant chercher automatiquement les variables 
    # AWS_ACCESS_KEY_ID et AWS_SECRET_ACCESS_KEY dans ton environnement
    s3 = boto3.client('s3')
    
    local_path = os.path.join("data", "raw", s3_file_name)
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    
    print(f"Téléchargement de {s3_file_name}...")
    s3.download_file(bucket_name, s3_file_name, local_path)
    print("Succès !")

if __name__ == "__main__":
    # Utilise tes vrais identifiants créés précédemment [cite: 110, 111]
    BUCKET = "g2-mg01-data"
    FILE_NAME = "Competency_block.csv"
    download_from_s3(BUCKET, FILE_NAME)