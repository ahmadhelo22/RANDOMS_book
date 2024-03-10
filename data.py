import json

def read(fjle_path):
    with open(fjle_path, 'r') as f :
        data = json.load(f)
        return data
    
def write(file_path, data):
    with open(file_path, 'w') as f :
        json.dump(data, f, indent=2)

