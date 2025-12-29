# Utiliser une image Python légère comme base
FROM python:3.10-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Installer les dépendances système nécessaires pour certains packages ML
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copier le fichier des dépendances
COPY requirements.txt .

# Installer les bibliothèques Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code source (src) et le dossier models
COPY src/ ./src/
COPY models/ ./models/

# Exposer le port sur lequel l'API va tourner
EXPOSE 8000

# Commande pour lancer l'API avec uvicorn 
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]