from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
import base64

# Generate private key
private_key = Ed25519PrivateKey.generate()

# Generate public key
public_key = private_key.public_key()

# Save private key
with open('private_key.pem', 'wb') as f:
    f.write(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    )

# Save public key
with open('public_key.pem', 'wb') as f:
    f.write(
        public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
    )

# Print base64 public key
public_key_b64 = base64.b64encode(
    public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )
).decode()

print('Public Key (base64):')
print(public_key_b64)
print('\\nKeys saved in signer folder.')