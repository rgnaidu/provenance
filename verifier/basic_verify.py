import hashlib
from pathlib import Path

# change this to any image inside assets folder
file_path = Path('../datasets/ps_i4_provenance/assets')

# take the first file in assets folder
asset = next(file_path.iterdir())

def sha256_file(path):
    h = hashlib.sha256()

    with open(path, 'rb') as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)

    return h.hexdigest()

print('File:', asset.name)
print('SHA256:', sha256_file(asset))