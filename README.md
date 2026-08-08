# Provenance, Not Detection

## Establishing What Media Actually Is When Generating Anything Is Free

A provenance-based media verification system designed to establish the origin, authenticity, and modification history of digital media.

Instead of relying only on AI-generated-content detection, this project uses provenance information, trusted issuers, cryptographic binding, and content-based soft binding to determine whether a media asset can be trusted.

---

## 1. Problem Statement

AI-generated and manipulated media is becoming increasingly difficult to distinguish from authentic content.

Traditional detection-based approaches have a major limitation:

> Generative models can improve faster than detection models.

A detector may identify today's generated content, but future generators can potentially produce content that bypasses the detector.

This project takes a different approach:

**Instead of asking "Does this look AI-generated?", we ask "Can we establish where this media came from and whether its history can be trusted?"**

---

## 2. Proposed Solution

The system establishes media provenance at the source and verifies it later.

The verification pipeline consists of:

1. Asset identification
2. Manifest lookup
3. Issuer trust verification
4. Hard-binding verification for the original asset
5. ORB-based soft-binding verification for transformed media
6. Final provenance verdict

The system produces one of the following results:

| Result          | Meaning                                                |
| --------------- | ------------------------------------------------------ |
| `VERIFIED`      | Original trusted asset with valid provenance           |
| `SOFT VERIFIED` | Transformed asset still strongly matches the original  |
| `ALTERED`       | Asset does not sufficiently match the trusted original |
| `UNTRUSTED`     | Issuer is not trusted or has been revoked              |
| `UNKNOWN`       | No provenance manifest is available                    |

---

## 3. System Architecture

```text
                    DIGITAL MEDIA
                         │
                         ▼
                 ┌─────────────────┐
                 │  Asset / Image   │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ Asset ID from   │
                 │ filename        │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ Manifest Lookup │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ Trust List      │
                 │ Verification    │
                 └────────┬────────┘
                          │
                ┌─────────┴─────────┐
                │                   │
             Original            Derived
                │                   │
                ▼                   ▼
        Hard Binding          ORB Matching
                │                   │
                ▼                   ▼
           VERIFIED        SOFT VERIFIED / ALTERED
```

---

## 4. Components

### Streamlit UI

Location:

```text
ui/app.py
```

Provides the user interface for uploading media and displaying the verification result.

### Verifier

Location:

```text
verifier/final_verifier.py
```

Responsible for:

* Asset ID extraction
* Manifest loading
* Issuer trust checking
* Original asset verification
* ORB feature matching
* Final verdict generation

### Signer

Location:

```text
signer/
```

Contains the signing-side components used to create provenance information.

Important files include:

```text
generate_keys.py
sign_file.py
public_key.pem
USER001.manifest.json
```

The private signing key is intentionally excluded from the submission for security.

### Dataset

Location:

```text
datasets/ps_i4_provenance/
```

Contains:

* Original assets
* Transformed versions
* Provenance manifests
* Trust list

### Results

Location:

```text
results/
```

Contains robustness and evaluation results.

---

## 5. Hard Binding

Hard binding establishes a strong relationship between the original media and its provenance information.

When a trusted original asset is submitted, the system verifies the associated provenance information and identifies it as:

```text
VERIFIED
```

Example:

```text
A000__original.jpg
```

Expected result:

```text
VERIFIED
Hard Binding: True
```

---

## 6. Soft Binding

Digital media may undergo legitimate transformations such as:

* Resizing
* Recompression
* Cropping
* Platform processing
* Screenshots

These transformations may change the file itself without necessarily changing its underlying visual content.

To handle this, the system uses ORB feature matching.

The original image is compared with the submitted image.

If the number of good ORB matches reaches the configured threshold, the asset is considered:

```text
SOFT VERIFIED
```

Otherwise, it may be classified as:

```text
ALTERED
```

---

## 7. Trust Model

The system maintains a trusted issuer list:

```text
datasets/ps_i4_provenance/trust_list.json
```

An issuer must have an active status in the trust list to be considered trusted.

This prevents provenance claims from being automatically accepted simply because a manifest exists.

Possible issuer states include:

```text
active
revoked
```

An inactive or unknown issuer results in:

```text
UNTRUSTED
```

---

## 8. Dataset

The project includes a provenance robustness dataset containing original assets and several transformed versions.

Example:

```text
A000__original.jpg
A000__crop_10pct.jpg
A000__platform_strip.jpg
A000__recompress_q40.jpg
A000__resize_640.jpg
A000__screenshot_sim.jpg
```

These transformations allow the verifier to be evaluated against common real-world modifications.

The dataset contains assets from `A000` through `A083`, along with provenance manifests for the available assets.

---

## 9. Verification Examples

### Original Asset

Input:

```text
A000__original.jpg
```

Result:

```text
VERIFIED
```

### Transformed Asset

Input:

```text
A000__resize_640.jpg
```

or another supported transformation.

Result may be:

```text
SOFT VERIFIED
```

when sufficient visual correspondence remains.

### Altered Asset

An asset with insufficient correspondence to the trusted original may produce:

```text
ALTERED
```

### Missing Manifest

If an asset has no corresponding provenance manifest:

```text
UNKNOWN
```

### Untrusted Issuer

If the issuer is not active in the trust list:

```text
UNTRUSTED
```

---

## 10. Project Structure

```text
provenance_not_detection/
│
├── README.md
├── requirements.txt
│
├── datasets/
│   └── ps_i4_provenance/
│       ├── README.md
│       ├── trust_list.json
│       ├── assets/
│       └── manifests/
│
├── results/
│   ├── limitataions.txt
│   ├── robustness_table.csv
│   └── summary.txt
│
├── screenshots/
│   ├── Homepage.png
│   ├── verified.png
│   ├── soft verified.png
│   └── unknown.png
│
├── signer/
│   ├── generate_keys.py
│   ├── public_key.pem
│   ├── sign_file.py
│   └── USER001.manifest.json
│
├── verifier/
│   ├── basic_verify.py
│   ├── check_hash.py
│   ├── final_verifier.py
│   ├── generate_results.py
│   ├── orb_test.py
│   └── verdict.py
│
└── ui/
    └── app.py
```

---

## 11. Installation

Clone or extract the project.

Create a Python environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 12. Running the Application

From the project root:

```bash
streamlit run ui/app.py
```

The Streamlit application will open in the browser.

---

## 13. Testing

The application can be tested using the assets available in:

```text
datasets/ps_i4_provenance/assets/
```

Recommended test categories:

1. Original assets
2. Resized assets
3. Recompressed assets
4. Cropped assets
5. Platform-processed assets
6. Screenshot-simulated assets
7. Assets without manifests
8. Assets associated with untrusted issuers

---

## 14. Evaluation

The project includes evaluation results in:

```text
results/robustness_table.csv
results/summary.txt
```

These files summarize the behavior of the verifier under different media transformations.

---

## 15. Limitations

The system is designed as a provenance verification prototype.

Important limitations include:

* ORB matching is not a cryptographic proof of content identity.
* The soft-binding threshold may require tuning for different datasets.
* Severe transformations may reduce feature correspondence.
* Provenance cannot be established when no trusted provenance information exists.
* Trust in an issuer depends on the integrity of the trust list.
* The prototype does not claim that an asset without provenance is automatically fake.

The key distinction is:

**No provenance does not necessarily mean fake. It means the system cannot establish trusted provenance.**

---

## 16. Deployment

The application is deployed using Streamlit Community Cloud.

Deployment URL:

https://provenance-nn3h5kdvh8gpta2togwglf.streamlit.app/

Source repository:

https://github.com/rgnaidu/provenance

---

## 17. Key Idea

Traditional media verification asks:


"Can we detect whether this media is AI-generated?"


Our system instead asks:


"Can we establish trusted provenance for this media?"


This shifts the focus from probabilistic detection to verifiable origin and history.

---

## 18. Conclusion

**Provenance, Not Detection** demonstrates a practical approach to media authenticity based on verifiable provenance.

By combining trusted issuers, provenance manifests, hard binding, and soft content matching, the system can distinguish between:

* Trusted original media
* Trusted transformed media
* Altered media
* Untrusted provenance
* Media with unknown provenance

The goal is not to detect every fake.

The goal is to make trustworthy media **verifiable by construction**.
