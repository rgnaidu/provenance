import hashlib
import json
import base64
from datetime import datetime
from cryptography.hazmat.primitives import serialization

# File to sign
file_path = '../datasets/ps_i4_provenance/assets/A000__original.jpg'

# Calculate SHA256
sha256 = hashlib.sha256()

with open(file_path, 'rb') as f:
    while chunk := f.read(4096):
        sha256.update(chunk)

file_hash = sha256.hexdigest()

# Load private key
with open('private_key.pem', 'rb') as f:
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=None
    )

# Sign the hash
signature = private_key.sign(file_hash.encode())

signature_b64 = base64.b64encode(signature).decode()

# Create manifest
manifest = {
    'claim': {
        'asset_id': 'USER001',
        'captured_at': datetime.utcnow().isoformat() + 'Z',
        'hard_binding_sha256': file_hash
    },
    'issuer': 'gayathri-signer',
    'algorithm': 'Ed25519',
    'signature_b64': signature_b64
}

# Save manifest
with open('USER001.manifest.json', 'w') as f:
    json.dump(manifest, f, indent=2)

print('File signed successfully.')
print('Manifest saved as USER001.manifest.json')