import chromadb
from dotenv import load_dotenv
import os

load_dotenv()

def chunk_text(text, chunk_size):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

text_files_directory = "../"

documents = []

for filename in os.listdir(text_files_directory):
    if filename.endswith(".txt"):
        filepath = os.path.join(text_files_directory, filename)
        with open(filepath, 'r') as file:
            content = file.read()
            chunks = chunk_text(content, chunk_size=250)
            for i, chunk in enumerate(chunks):
                doc_id = f"{filename}_chunk_{i}"
                documents.append({"id": doc_id, "content": chunk})


storage_path = os.getenv('STORAGE_PATH')
if storage_path is None:
    raise ValueError('STORAGE_PATH environment variable is not set')

client = chromadb.PersistentClient(path=storage_path)

collection = client.get_or_create_collection(name="database_systems")

for doc in documents:
    collection.add(
        ids= doc['id'],
        documents= doc['content']
    )
    

    
    
print(collection.count())