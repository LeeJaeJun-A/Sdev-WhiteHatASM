import json
from backend.database.mongodb import cve_collection

json_file_path = 'backend/core/json/cve.json'

def load_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
    
def insert_json_to_db(collection, data):
    collection.delete_many({})
    
    if 'cve_list' in data:
        collection.insert_many(data['cve_list'])
    else:
        print("Check your json file again.")
        
def main():
    data = load_json_file(json_file_path)
    
    insert_json_to_db(cve_collection, data)
    
    print("Data successfully loaded into MongoDB.")
    
if __name__ == "__main__":
    main()

# run "python -m backend.core.cve"