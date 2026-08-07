import os
import csv
from final_verifier import verify

ASSET_FOLDER = '../datasets/ps_i4_provenance/assets'

os.makedirs('../results', exist_ok=True)

with open('../results/robustness_table.csv', 'w', newline='') as f:

    writer = csv.writer(f)

    writer.writerow([
        'file',
        'asset_id',
        'issuer',
        'captured_at',
        'hard',
        'soft',
        'orb_matches',
        'result'
    ])

    for file_name in os.listdir(ASSET_FOLDER):

        if file_name.lower().endswith(('.jpg', '.jpeg', '.png')):

            r = verify(file_name)

            writer.writerow([
                file_name,
                r['asset_id'],
                r['issuer'],
                r['captured_at'],
                r['hard'],
                r['soft'],
                r['orb_matches'],
                r['result']
            ])

print('robustness_table.csv created')