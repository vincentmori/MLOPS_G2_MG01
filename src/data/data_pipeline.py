from download_data import download_from_s3
from clean_transform import clean_data

def run_pipeline():
    # 1. Download
    download_from_s3("g2-mg01-data", "Competency_block.csv", "data/raw/Competency_block.csv")
    
    # 2. Clean
    clean_data("data/raw/Competency_block.csv", "data/processed/clean_competencies.csv")

if __name__ == "__main__":
    run_pipeline()