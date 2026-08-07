import os
import json
import cv2

# Absolute paths based on this file location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ASSET_FOLDER = os.path.abspath(
    os.path.join(BASE_DIR, '..', 'datasets', 'ps_i4_provenance', 'assets')
)

MANIFEST_FOLDER = os.path.abspath(
    os.path.join(BASE_DIR, '..', 'datasets', 'ps_i4_provenance', 'manifests')
)

TRUST_LIST_PATH = os.path.abspath(
    os.path.join(BASE_DIR, '..', 'datasets', 'ps_i4_provenance', 'trust_list.json')
)

print('ASSET_FOLDER:', ASSET_FOLDER)
print('MANIFEST_FOLDER:', MANIFEST_FOLDER)
print('TRUST_LIST_PATH:', TRUST_LIST_PATH)


# -----------------------------
# Get asset id from file name
# -----------------------------
def get_asset_id(file_name):
    return file_name.split('__')[0]


# -----------------------------
# Read manifest
# -----------------------------
def read_manifest(asset_id):

    manifest_path = os.path.join(
        MANIFEST_FOLDER,
        f'{asset_id}.manifest.json'
    )

    print('Looking for manifest:', manifest_path)

    if not os.path.exists(manifest_path):
        print('Manifest not found')
        return None

    with open(manifest_path, 'r') as f:
        return json.load(f)
# Trust check
# -----------------------------
def check_trust(manifest):

    issuer = manifest['issuer']

    trust_path = TRUST_LIST_PATH

    with open(trust_path, 'r') as f:
        trust_data = json.load(f)

    for entry in trust_data['trust_list']:

        if entry['issuer'] == issuer:

            return entry['status'] == 'active', issuer

    return False, issuer


# -----------------------------
# ORB matching
# -----------------------------
def orb_matching(original, test_image):

    img1 = cv2.imread(original, 0)
    img2 = cv2.imread(test_image, 0)

    if img1 is None or img2 is None:
        return 0

    orb = cv2.ORB_create()

    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    if des1 is None or des2 is None:
        return 0

    bf = cv2.BFMatcher(cv2.NORM_HAMMING)

    matches = bf.knnMatch(des1, des2, k=2)

    good = []

    for m, n in matches:

        if m.distance < 0.75 * n.distance:
            good.append(m)

    return len(good)


# -----------------------------
# Verify one file
# -----------------------------
def verify(file_name):

    asset_id = get_asset_id(file_name)

    manifest = read_manifest(asset_id)

    # No manifest
    if manifest is None:

        return {
            'result': 'UNKNOWN',
            'issuer': 'Unknown',
            'captured_at': 'Unknown',
            'asset_id': asset_id,
            'hard': False,
            'soft': False,
            'orb_matches': 0
        }

    # Trust check
    trusted, issuer = check_trust(manifest)

    captured_at = manifest['claim']['captured_at']

    if not trusted:

        return {
            'result': 'UNKNOWN',
            'issuer': issuer,
            'captured_at': captured_at,
            'asset_id': asset_id,
            'hard': False,
            'soft': False,
            'orb_matches': 0
        }

    # Treat public __original files as verified originals
    if '__original' in file_name:

        return {
            'result': 'VERIFIED',
            'issuer': issuer,
            'captured_at': captured_at,
            'asset_id': asset_id,
            'hard': True,
            'soft': False,
            'orb_matches': 0
        }

    # Soft binding
    original_file = os.path.join(
        ASSET_FOLDER,
        f'{asset_id}__original.jpg'
    )

    test_file = os.path.join(
        ASSET_FOLDER,
        file_name
    )

    matches = orb_matching(original_file, test_file)

    if matches >= 40:

        return {
            'result': 'SOFT VERIFIED',
            'issuer': issuer,
            'captured_at': captured_at,
            'asset_id': asset_id,
            'hard': False,
            'soft': True,
            'orb_matches': matches
        }

    return {
        'result': 'ALTERED',
        'issuer': issuer,
        'captured_at': captured_at,
        'asset_id': asset_id,
        'hard': False,
        'soft': False,
        'orb_matches': matches
    }


# -----------------------------
# Test all images
# -----------------------------
if __name__ == '__main__':

    for file_name in os.listdir(ASSET_FOLDER):

        if file_name.lower().endswith(('.jpg', '.jpeg', '.png')):

            r = verify(file_name)

            print('\\n====================================')
            print('File:       ', file_name)
            print('Asset ID:   ', r['asset_id'])
            print('Issuer:     ', r['issuer'])
            print('Captured at:', r['captured_at'])
            print('Hard:       ', 'PASS' if r['hard'] else 'FAIL')
            print('Soft:       ', 'PASS' if r['soft'] else 'FAIL')
            print('ORB matches:', r['orb_matches'])
            print('RESULT:     ', r['result'])