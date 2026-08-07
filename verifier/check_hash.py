import hashlib
import json

# Read manifest
with open('../datasets/ps_i4_provenance/manifests/A000.manifest.json', 'r') as f:
    manifest = json.load(f)

manifest_hash = manifest['claim']['hard_binding_sha256']

# Calculate file hash
sha = hashlib.sha256()

with open('../datasets/ps_i4_provenance/assets/A000__original.jpg', 'rb') as f:
    while chunk := f.read(4096):
        sha.update(chunk)

file_hash = sha.hexdigest()

print('Manifest hash:')
print(manifest_hash)

print('\\nFile hash:')
print(file_hash)

print('\\nMatch:', manifest_hash == file_hash)