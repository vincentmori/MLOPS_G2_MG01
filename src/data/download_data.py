import boto3
import os

def download_from_s3(bucket_name, s3_file_name):
    s3 = boto3.client('s3')
    
    # On définit le chemin vers le dossier data à la racine du projet
    # ../../ remonte de src/data/ vers la racine
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    local_dir = os.path.join(base_dir, "data", "raw")
    local_file_path = os.path.join(local_dir, s3_file_name)
    
    # Créer le dossier data/raw s'il n'existe pas
    os.makedirs(local_dir, exist_ok=True)
    
    print(f"Téléchargement vers : {local_file_path}")
    s3.download_file(bucket_name, s3_file_name, local_file_path)
    return local_file_path

if __name__ == "__main__":
    # Utilise tes vrais identifiants créés précédemment [cite: 110, 111]
    BUCKET = "g2-mg01-data"
    FILE_NAME = "Competency_block.csv"
    download_from_s3(BUCKET, FILE_NAME)