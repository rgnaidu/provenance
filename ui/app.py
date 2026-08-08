import streamlit as st
import importlib.util
import os
import sys

# ----------------------------------------------------
# Import verifier
# ----------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VERIFIER_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'verifier'))
VERIFIER_PATH = os.path.join(VERIFIER_DIR, 'final_verifier.py')

if not os.path.exists(VERIFIER_PATH):
    raise FileNotFoundError(f'Unable to locate verifier module at {VERIFIER_PATH}')

spec = importlib.util.spec_from_file_location('final_verifier', VERIFIER_PATH)
if spec is None or spec.loader is None:
    raise ImportError(f'Cannot load verifier module from {VERIFIER_PATH}')

final_verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(final_verifier)
verify = final_verifier.verify

# ----------------------------------------------------
# Page configuration
# ----------------------------------------------------
st.set_page_config(
    page_title='Provenance Viewer',
    page_icon='🛡️',
    layout='wide'
)

# ----------------------------------------------------
# Header
# ----------------------------------------------------
st.title('🛡️ Provenance Viewer')

st.caption(
    'Verify media origin and edit history using manifests, trust lists, hard binding, and soft binding.'
)

uploaded_file = st.file_uploader(
    'Upload an image from the dataset',
    type=['jpg', 'jpeg', 'png']
)

# ----------------------------------------------------
# Main
# ----------------------------------------------------
if uploaded_file is not None:

    result = verify(uploaded_file.name)

    # Image preview
    st.image(
        uploaded_file,
        caption=uploaded_file.name,
        use_container_width=True
    )

    st.divider()

    # ------------------------------------------------
    # Verification Summary
    # ------------------------------------------------
    st.subheader('📋 Verification Summary')

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric('Asset ID', result['asset_id'])

    with c2:
        st.metric('Issuer', result['issuer'])

    with c3:
        st.metric(
            'Hard Binding',
            'PASS' if result['hard'] else 'FAIL'
        )

    with c4:
        st.metric(
            'Soft Binding',
            'PASS' if result['soft'] else 'FAIL'
        )

    st.divider()

    # ------------------------------------------------
    # Verdict Banner
    # ------------------------------------------------
    if result['result'] == 'VERIFIED':

        st.success(
            '🟢 Verified provenance — trusted issuer and original reference matched.'
        )

    elif result['result'] == 'SOFT VERIFIED':

        st.warning(
            '🟡 Likely derived from a signed original — cropping or platform processing detected.'
        )

    elif result['result'] == 'ALTERED':

        st.error(
            '🟠 Provenance conflict — file does not sufficiently match the trusted original.'
        )

    elif result['result'] == 'UNTRUSTED':

        st.warning(
            f'🟣 Untrusted provenance — manifest found, but issuer `{result["issuer"]}` is not trusted.'
        )

    else:

        st.info(
            '🔵 No provenance available — no manifest found for this asset.'
        )

    st.divider()

    # ------------------------------------------------
    # Two-column details
    # ------------------------------------------------
    left, right = st.columns(2)

    # Manifest information
    with left:

        st.subheader('📄 Manifest Information')

        st.markdown(
            f"""
**Asset ID:** `{result['asset_id']}`

**Issuer:** `{result['issuer']}`

**Captured at:** `{result['captured_at']}`

**Trust status:** `{result['result']}`
"""
        )

        if result['issuer'] == 'ghostsign':

            st.caption(
                'This issuer is present in the trust list but marked as revoked.'
            )

    # Binding information
    with right:

        st.subheader('🔐 Binding Information')

        st.markdown(
            f"""
**Hard binding:** `{ 'PASS' if result['hard'] else 'FAIL' }`

**Soft binding:** `{ 'PASS' if result['soft'] else 'FAIL' }`

**ORB matches:** `{result['orb_matches']}`
"""
        )

        if result['hard']:

            st.caption(
                'Byte-identical to the trusted original reference.'
            )

        elif result['soft']:

            st.caption(
                'Visual similarity passed after transformation.'
            )

        else:

            st.caption(
                'Visual similarity did not pass.'
            )

    st.divider()

    # ------------------------------------------------
    # Technical details
    # ------------------------------------------------
    with st.expander('⚙️ Technical Details', expanded=False):

        st.code(
            f"""
File: {uploaded_file.name}
Asset ID: {result['asset_id']}
Issuer: {result['issuer']}
Captured at: {result['captured_at']}
Hard binding: {result['hard']}
Soft binding: {result['soft']}
ORB matches: {result['orb_matches']}
Final result: {result['result']}
""",
            language='text'
        )

    st.divider()

    # ------------------------------------------------
    # Interpretation
    # ------------------------------------------------
    st.subheader('ℹ️ What this means')

    st.markdown(
        """
- **Verified provenance** → trusted issuer + original reference matched.
- **Likely derived from a signed original** → cropping, re-encoding, or platform processing occurred.
- **Provenance conflict** → the file does not sufficiently match the trusted original.
- **Untrusted provenance** → a manifest exists, but the issuer is revoked or not trusted.
- **No provenance available** → no manifest was found for this file.
"""
    )

    st.info(
        'Absence of provenance is **not evidence of fabrication**.'
    )

    st.warning(
        'Provenance verifies **origin and edit history**, not whether the depicted scene is true, honest, or not staged.'
    )

# ----------------------------------------------------
# Empty state
# ----------------------------------------------------
else:

    st.markdown('### Try these examples')

    st.markdown(
        """
- `A000__original.jpg` → Verified provenance
- `A000__crop_10pct.jpg` → Likely derived from a signed original
- `A001__original.jpg` → No provenance available
- `A069__original.jpg` → Untrusted provenance (ghostsign)
"""
    )

    st.divider()

    st.markdown('### Architecture')

    st.markdown(
        """
`Upload → Manifest Lookup → Trust Check → Hard Binding → Soft Binding → Verdict → UI`
"""
    )

# ----------------------------------------------------
# Footer
# ----------------------------------------------------
st.divider()

st.caption(
    'Built for the **Provenance, Not Detection** project — emphasizing uncertainty, trust, and user understanding rather than binary real/fake labels.'
)