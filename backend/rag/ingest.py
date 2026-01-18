import csv
import os
import uuid
import sys

# Add root directory to path so we can import backend modules
sys.path.append(os.getcwd())

from backend.rag.vector_store import get_vector_store

def ingest_food_data(csv_path="data/food_database.csv"):
    print(f"Loading data from {csv_path}...")
    
    if not os.path.exists(csv_path):
        print(f"Error: File {csv_path} not found.")
        return

    collection = get_vector_store()
    
    documents = []
    metadatas = []
    ids = []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Create a descriptive text for embedding
            # "Couscous with Lamb: 900 cal, 35g protein..."
            text_content = (
                f"{row['name']} ({row['category']}): "
                f"{row['calories_100g']} calories per 100g. "
                f"Macros: {row['protein_100g']}g Protein, {row['fat_100g']}g Fat, {row['carbs_100g']}g Carbs. "
                f"Approx price: {row['price_tnd']} TND."
            )
            
            documents.append(text_content)
            metadatas.append({
                "name": row['name'],
                "category": row['category'],
                "calories": int(row['calories_100g']),
                "price": float(row['price_tnd'])
            })
            ids.append(str(uuid.uuid4()))

    if documents:
        print(f"Ingesting {len(documents)} items into ChromaDB...")
        # Add in batches to avoid hitting limits (though Chroma handles this well usually)
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            end = min(i + batch_size, len(documents))
            collection.add(
                documents=documents[i:end],
                metadatas=metadatas[i:end],
                ids=ids[i:end]
            )
        print("Ingestion complete!")
    else:
        print("No data found to ingest.")

if __name__ == "__main__":
    # Path is already adjusted at top of file
    ingest_food_data()
