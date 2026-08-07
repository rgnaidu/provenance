import streamlit as st
import sys
import os

# Add verifier folder to Python path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VERIFIER_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'verifier'))
sys.path.append(VERIFIER_DIR)

from final_verifier import verify

st.set_page_config(
    page_title='Provenance Viewer',
    page_icon='📷',
    layout='centered'
)

# ---------- Custom CSS ----------
st.markdown(
    """
    <style>
    .main {
        padding-top: 1rem;
    }
    .status-card {
        border-radius: 16px;
        padding: 1rem 1.2rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(128,128,128,0.25);
    }
    .status-title {
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }
    .status-sub {
        font-size: 0.95rem;
        opacity: 0.9;
    }
    .green {
        background: rgba(16,185,129,0.12);
        border-color: rgba(16,185,129,0.35);
    }
    .yellow {
        background: rgba(245,158,11,0.12);
        border-color: rgba(245,158,11,0.35);
    }
    .orange {
        background: rgba(249,115,22,0.12);
        border-color: rgba(249,115,22,0.35);
    }
    .blue {
        background: rgba(59,130,246,0.12);
        border-color: rgba(59,130,246,0.35);
    }
    .detail-box {
        border-radius: 14px;
        padding: 1rem 1.2rem;
        border: 1px solid rgba(128,128,128,0.18);
        background: rgba(255,255,255,0.02);
    }
    .footer-note {
        font-size: 0.9rem;
        opacity: 0.85;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- Header ----------
st.title('📷 Provenance Viewer')
st.write(
    'Check whether an image has trusted provenance information and whether it appears unchanged or derived from a signed original.'
)

uploaded_file = st.file_uploader(
    'Choose an image',
    type=['jpg', 'jpeg', 'png']
)

if uploaded_file is not None:

    st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)

    st.divider()

    result = verify(uploaded_file.name)

    # ---------- Status ----------
    if result['result'] == 'VERIFIED':

        st.markdown(
            """
            <div class='status-card green'>
                <div class='status-title'>🟢 Verified provenance</div>
                <div class='status-sub'>
                    Trusted issuer found and this image matches the signed original reference.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    elif result['result'] == 'SOFT VERIFIED':

        st.markdown(
            """
            <div class='status-card yellow'>
                <div class='status-title'>🟡 Likely derived from a signed original</div>
                <div class='status-sub'>
                    Exact bytes changed, but the image remains visually consistent with the trusted original.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    elif result['result'] == 'ALTERED':

        st.markdown(
            """
            <div class='status-card orange'>
                <div class='status-title'>🟠 Provenance conflict</div>
                <div class='status-sub'>
                    The file does not sufficiently match the trusted original for this asset.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        if result['issuer'] == 'Unknown':

            st.markdown(
                """
                <div class='status-card blue'>
                    <div class='status-title'>🔵 No provenance available</div>
                    <div class='status-sub'>
                        No manifest was found for this image in the current dataset.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                """
                <div class='status-card blue'>
                    <div class='status-title'>🔵 Untrusted provenance</div>
                    <div class='status-sub'>
                        A provenance record exists, but the issuer is not currently trusted.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # ---------- Details ----------
    st.subheader('Provenance details')

    hard_status = 'PASS' if result['hard'] else 'FAIL'
    soft_status = 'PASS' if result['soft'] else 'FAIL'

    st.markdown(
        f"""
        <div class='detail-box'>
            <b>Asset ID:</b> {result['asset_id']}<br><br>
            <b>Issuer:</b> {result['issuer']}<br><br>
            <b>Captured at:</b> {result['captured_at']}<br><br>
            <b>Hard binding:</b> {hard_status}<br><br>
            <b>Soft binding:</b> {soft_status}<br><br>
            <b>ORB matches:</b> {result['orb_matches']}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # ---------- Explanation ----------
    st.subheader('What this means')

    st.markdown(
        """
- **Verified provenance** → trusted issuer + original reference matched.
- **Likely derived from a signed original** → the file was changed by cropping, re-encoding, or platform processing, but still appears related to the trusted original.
- **Provenance conflict** → the file does not sufficiently match the trusted original.
- **No provenance available** → no manifest was found.
- **Untrusted provenance** → a manifest exists, but the issuer is revoked or not trusted.
        """
    )

    st.info(
        'Absence of provenance is **not evidence of fabrication**.'
    )

    st.warning(
        'Provenance verifies **origin and edit history**, not whether the scene is true, honest, or not staged.'
    )

else:

    st.markdown(
        """
        ### Try these examples

        - **A000__original.jpg** → Verified provenance
        - **A000__crop_10pct.jpg** → Likely derived from a signed original
        - **A001__original.jpg** (revoked issuer) → Untrusted provenance
        - **A070__original.jpg** (no manifest) → No provenance available
        """
    )

    st.caption(
        'Upload an image from the dataset to see issuer, capture time, and provenance status.'
    )

st.divider()

st.markdown(
    """
    <div class='footer-note'>
        Built for the <b>Provenance, Not Detection</b> project — emphasizing cryptographic provenance, uncertainty, and user understanding rather than binary real/fake labels.
    </div>
    """,
    unsafe_allow_html=True
)