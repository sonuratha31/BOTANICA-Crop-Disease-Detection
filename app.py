
from pathlib import Path
from datetime import datetime
import hashlib
import sys
import io

import streamlit as st
import numpy as np
import pandas as pd
import tensorflow as tf
import plotly.graph_objects as go

from PIL import Image, UnidentifiedImageError
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader, simpleSplit
from reportlab.pdfgen import canvas

sys.path.insert(0, str(Path(__file__).parent))

from src.predict import load_model_and_classes, predict_disease
from src.gradcam import generate_gradcam, overlay_gradcam
from src.disease_info import format_disease_name, get_disease_info


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="BOTANICA | Plant Disease Field Laboratory",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# --------------------------------------------------
# BOTANICA DESIGN SYSTEM
# --------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #f4f2e9;
    color: #263d30;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: #234331 !important;
}

.botanical-label {
    color: #9a7650;
    letter-spacing: 3px;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
}

.hero {
    background: #234331;
    color: #f4f2e9;
    padding: 55px 48px;
    border-radius: 5px;
    margin: 15px 0 30px 0;
}

.hero h1 {
    color: #f4f2e9 !important;
    font-size: 55px;
    line-height: 1.08;
    margin-bottom: 12px;
}

.hero p {
    color: #d5dfd3;
    font-size: 16px;
    max-width: 650px;
}

.specimen {
    background: #e8e6da;
    padding: 22px;
    border-left: 4px solid #a66c4c;
    margin: 12px 0;
}

.report {
    background: #fffef9;
    padding: 25px;
    border: 1px solid #dedccd;
    border-radius: 4px;
}

div[data-testid="stMetric"] {
    background: #e8e6da;
    padding: 16px;
    border-radius: 4px;
}

.stButton > button {
    background: #315a40;
    color: white;
    border: none;
    border-radius: 3px;
    padding: 10px 22px;
}

.stButton > button:hover {
    background: #1f402d;
    color: white;
    border: none;
}

[data-testid="stFileUploader"] {
    background: #fffef9;
    border: 1px dashed #8a9b85;
    padding: 20px;
    border-radius: 4px;
}

hr {
    border-color: #d8d7ca;
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

@st.cache_resource
def get_model():
    return load_model_and_classes()


model = None
class_names = []
model_error = None

try:
    model, class_names = get_model()
    model_ready = True
except Exception as error:
    model_ready = False
    model_error = f"{type(error).__name__}: {error}"


if "journal" not in st.session_state:
    st.session_state.journal = []


# --------------------------------------------------
# HEADER AND NAVIGATION
# --------------------------------------------------

st.markdown("""
<div class="botanical-label">BOTANICAL RESEARCH • AI DIAGNOSTICS</div>
<h1 style="font-family:Playfair Display; margin-bottom:0;">
BOTANICA<span style="color:#a66c4c;">.</span>
</h1>
<p style="color:#718071; margin-top:0;">
PLANT DISEASE FIELD LABORATORY
</p>
""", unsafe_allow_html=True)

pages = [
    "Home",
    "Leaf Scanner",
    "Disease Encyclopedia",
    "Comparison Lab",
    "3D Leaf Viewer",
    "Field Journal"
]

page = st.radio(
    "Navigation",
    pages,
    horizontal=True,
    label_visibility="collapsed"
)

st.divider()


# --------------------------------------------------
# HELPER: IMAGE PREDICTION
# --------------------------------------------------

def run_prediction(image):
    return predict_disease(image, model, class_names)


def load_uploaded_image(uploaded_file):
    try:
        with Image.open(uploaded_file) as source:
            if source.format not in {"JPEG", "PNG"}:
                raise ValueError("Unsupported image format.")
            source.load()
            return source.convert("RGB")
    except (
        UnidentifiedImageError,
        OSError,
        ValueError,
        Image.DecompressionBombError
    ) as error:
        raise ValueError(
            "Please choose a valid, readable JPG or PNG image."
        ) from error


def save_to_journal(result):
    crop, disease = format_disease_name(result["disease"])

    st.session_state.journal.insert(0, {
        "Date": datetime.now().strftime("%d %b %Y, %I:%M %p"),
        "Crop": crop,
        "Prediction": disease,
        "Confidence": round(result["confidence"], 2)
    })


# --------------------------------------------------
# HELPER: PDF REPORT
# --------------------------------------------------

def create_pdf(result, image=None, gradcam_overlay=None):
    crop, disease = format_disease_name(result["disease"])
    info = get_disease_info(result["disease"])

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    pdf.setFillColorRGB(0.14, 0.27, 0.19)
    pdf.rect(0, height - 120, width, 120, fill=1)

    pdf.setFillColorRGB(0.96, 0.95, 0.90)
    pdf.setFont("Helvetica-Bold", 25)
    pdf.drawString(48, height - 65, "BOTANICA")

    pdf.setFont("Helvetica", 11)
    pdf.drawString(
        48, height - 88,
        "PLANT DISEASE FIELD LABORATORY"
    )

    y = height - 165

    pdf.setFillColorRGB(0.14, 0.27, 0.19)
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(48, y, "DIAGNOSTIC REPORT")

    y -= 40
    pdf.setFont("Helvetica", 11)

    lines = [
        (f"Report date: {datetime.now().strftime('%d %B %Y, %I:%M %p')}",
         "Helvetica"),
        (f"Crop: {crop}", "Helvetica"),
        (f"AI prediction: {disease}", "Helvetica"),
        (f"Prediction score: {result['confidence']:.2f}%", "Helvetica"),
    ]

    for line, font_name in lines:
        pdf.setFont(font_name, 11)
        for wrapped_line in simpleSplit(line, font_name, 11, width - 96):
            if y < 70:
                pdf.showPage()
                y = height - 60
                pdf.setFont(font_name, 11)
            pdf.drawString(48, y, wrapped_line)
            y -= 22

    if image is not None:
        report_images = [("Uploaded leaf", image)]
        if gradcam_overlay is not None:
            report_images.append((
                "Grad-CAM attention overlay",
                Image.fromarray(gradcam_overlay)
            ))

        section_height = 230
        if y - section_height < 70:
            pdf.showPage()
            y = height - 60

        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawString(48, y, "SPECIMEN AND VISUAL EXPLANATION")
        y -= 22

        image_count = len(report_images)
        image_width = (width - 116) / image_count
        image_height = 175

        for index, (caption, report_image) in enumerate(report_images):
            if report_image.mode != "RGB":
                report_image = report_image.convert("RGB")

            max_size = (720, 540)
            scale = min(
                max_size[0] / report_image.width,
                max_size[1] / report_image.height,
                1
            )
            resized_image = report_image.resize((
                max(1, round(report_image.width * scale)),
                max(1, round(report_image.height * scale))
            ), Image.Resampling.LANCZOS)

            x = 48 + index * (image_width + 20)
            pdf.setFont("Helvetica", 9)
            pdf.drawString(x, y, caption)
            pdf.drawImage(
                ImageReader(resized_image),
                x,
                y - image_height - 4,
                width=image_width,
                height=image_height,
                preserveAspectRatio=True,
                anchor="c"
            )

        y -= image_height + 28

        if gradcam_overlay is not None:
            explanation = (
                "Grad-CAM highlights image regions that influenced the "
                "model prediction. It is an explanatory visualization, "
                "not proof of a disease or its severity."
            )
        else:
            explanation = (
                "Grad-CAM was unavailable for this examination."
            )

        pdf.setFont("Helvetica", 9)
        for wrapped_line in simpleSplit(explanation, "Helvetica", 9, width - 96):
            if y < 70:
                pdf.showPage()
                y = height - 60
                pdf.setFont("Helvetica", 9)
            pdf.drawString(48, y, wrapped_line)
            y -= 14
        y -= 8

    content_lines = [
        ("OBSERVATION", "Helvetica-Bold", info["description"]),
        ("GENERAL MANAGEMENT GUIDANCE", "Helvetica-Bold", None),
    ]

    for heading, font_name, content in content_lines:
        if y < 70:
            pdf.showPage()
            y = height - 60
        pdf.setFont(font_name, 11)
        pdf.drawString(48, y, heading)
        y -= 22

        if content:
            for wrapped_line in simpleSplit(content, "Helvetica", 11, width - 96):
                if y < 70:
                    pdf.showPage()
                    y = height - 60
                    pdf.setFont("Helvetica", 11)
                pdf.drawString(48, y, wrapped_line)
                y -= 22

    pdf.setFont("Helvetica", 11)
    for item in info["management"]:
        wrapped_lines = simpleSplit("- " + item, "Helvetica", 11, width - 106)
        for wrapped_line in wrapped_lines:
            if y < 70:
                pdf.showPage()
                y = height - 60
                pdf.setFont("Helvetica", 11)
            pdf.drawString(58, y, wrapped_line)
            y -= 22

    y -= 20
    if y < 50:
        pdf.showPage()
        y = height - 60
    pdf.setFont("Helvetica-Oblique", 9)
    pdf.drawString(
        48, y,
        "AI-generated result. Verify with a qualified agricultural expert."
    )

    pdf.save()
    buffer.seek(0)
    return buffer.getvalue()


# --------------------------------------------------
# HOME
# --------------------------------------------------

if page == "Home":

    st.markdown("""
    <div class="hero">
        <div style="letter-spacing:4px;font-size:11px;color:#c6d4c3;">
            THE SCIENCE OF HEALTHIER CROPS
        </div>
        <h1>Every leaf<br>has a story.</h1>
        <p>
            Explore plant health through deep learning.
            Examine leaf specimens, understand disease patterns,
            and turn image-based predictions into useful insights.
        </p>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([1.3, 1])

    with left:
        st.markdown("### The laboratory")
        st.write(
            "BOTANICA is an educational crop disease research "
            "prototype powered by a MobileNetV2 deep-learning model "
            "trained on the PlantVillage image dataset."
        )

        st.markdown("""
        <div class="specimen">
        <b>RESEARCH METHOD</b><br><br>
        Image acquisition → Preprocessing → Deep learning →
        Disease classification → Visual explanation
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown("### Laboratory status")

        if model_ready:
            st.success("Prediction model loaded")
            st.metric("Recognized categories", len(class_names))
        else:
            st.warning(
                "The trained model is unavailable. Restore the saved model "
                "and class list to enable predictions."
            )
            with st.expander("Model loading details"):
                st.code(model_error)

        st.metric(
            "Saved examinations",
            len(st.session_state.journal)
        )

    st.markdown("### Explore the laboratory")

    a, b, c = st.columns(3)

    a.markdown("**01 — Examine**")
    a.write("Upload a leaf specimen and receive an AI prediction.")

    b.markdown("**02 — Understand**")
    b.write("Explore disease information and Grad-CAM explanations.")

    c.markdown("**03 — Document**")
    c.write("Compare specimens and save diagnostic reports.")


# --------------------------------------------------
# LEAF SCANNER
# --------------------------------------------------

elif page == "Leaf Scanner":

    st.markdown('<div class="botanical-label">SPECIMEN ANALYSIS / 01</div>',
                unsafe_allow_html=True)
    st.title("Examine a leaf specimen")
    st.write(
        "Upload a clear image of a single crop leaf for AI-based classification."
    )

    uploaded = st.file_uploader(
        "Choose a leaf photograph",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded:
        upload_key = hashlib.sha256(uploaded.getvalue()).hexdigest()
        if st.session_state.get("last_image_key") != upload_key:
            st.session_state.pop("last_result", None)
            st.session_state.pop("last_image", None)
            st.session_state.pop("last_image_key", None)
            st.session_state.pop("last_gradcam_key", None)
            st.session_state.pop("last_gradcam_heatmap", None)
            st.session_state.pop("last_gradcam_error", None)
            st.session_state.pop("last_gradcam_attempted", None)
            st.session_state.pop("last_pdf_key", None)
            st.session_state.pop("last_pdf", None)

        try:
            image = load_uploaded_image(uploaded)
        except ValueError as error:
            st.error(f"Could not read the uploaded image. {error}")
            st.stop()

        left, right = st.columns([1.1, 0.9])

        with left:
            st.image(image, caption="Uploaded specimen", use_container_width=True)

        with right:
            st.markdown("### Specimen details")
            st.write(f"Image dimensions: {image.width} × {image.height}")
            st.write("Image format: RGB")

            if not model_ready:
                st.error(
                    "Prediction is unavailable because the trained model "
                    "could not be loaded. See Home for details."
                )
            elif st.button("Run AI examination", use_container_width=True):
                with st.spinner("Examining specimen..."):
                    try:
                        result = run_prediction(image)
                    except Exception as error:
                        st.error(
                            "Could not analyze this image. Please try a "
                            "clear, valid leaf photograph."
                        )
                        with st.expander("Prediction error details"):
                            st.code(f"{type(error).__name__}: {error}")
                    else:
                        st.session_state.last_result = result
                        st.session_state.last_image = image
                        st.session_state.last_image_key = upload_key
                        st.session_state.pop("last_pdf_key", None)
                        st.session_state.pop("last_pdf", None)
                        save_to_journal(result)

        if "last_result" in st.session_state:
            result = st.session_state.last_result
            info = get_disease_info(result["disease"])
            crop, disease = format_disease_name(result["disease"])

            st.divider()
            st.markdown('<div class="botanical-label">ANALYSIS RESULT</div>',
                        unsafe_allow_html=True)
            st.title(disease)

            c1, c2, c3 = st.columns(3)
            c1.metric("Crop", crop)
            c2.metric("Prediction score", f"{result['confidence']:.2f}%")
            c3.metric("Classification", info["status"])

            st.markdown("### Observation")
            st.write(info["description"])

            st.markdown("### General management guidance")
            for suggestion in info["management"]:
                st.write("• " + suggestion)

            st.caption(
                "Prediction scores are not calibrated probabilities "
                "or guarantees of disease presence."
            )

            st.markdown("### Visual explanation — Grad-CAM")

            gradcam_overlay = None
            if st.session_state.get("last_gradcam_key") != upload_key:
                st.session_state.pop("last_gradcam_heatmap", None)
                st.session_state.pop("last_gradcam_error", None)
                st.session_state.last_gradcam_attempted = False
                st.session_state.last_gradcam_key = upload_key

            if not st.session_state.get("last_gradcam_attempted", False):
                try:
                    with st.spinner("Generating Grad-CAM explanation..."):
                        image_array = tf.keras.utils.img_to_array(
                            st.session_state.last_image.resize((224, 224))
                        )
                        image_array = np.expand_dims(image_array, axis=0)
                        image_array = (
                            tf.keras.applications.mobilenet_v2.preprocess_input(
                                image_array
                            )
                        )
                        st.session_state.last_gradcam_heatmap = generate_gradcam(
                            model, image_array
                        )
                except Exception as error:
                    st.session_state.last_gradcam_error = str(error)
                st.session_state.last_gradcam_attempted = True

            heatmap = st.session_state.get("last_gradcam_heatmap")
            if heatmap is not None:
                try:
                    overlay = overlay_gradcam(
                        st.session_state.last_image, heatmap
                    )
                    gradcam_overlay = overlay

                    g1, g2 = st.columns(2)
                    g1.image(
                        st.session_state.last_image,
                        caption="Original specimen",
                        use_container_width=True
                    )
                    g2.image(
                        overlay,
                        caption="Grad-CAM attention overlay",
                        use_container_width=True
                    )
                except Exception as error:
                    st.warning("The Grad-CAM overlay could not be displayed.")
                    with st.expander("Grad-CAM display error details"):
                        st.code(f"{type(error).__name__}: {error}")
            else:
                st.warning(
                    "Grad-CAM could not be generated for this image."
                )
                with st.expander("Grad-CAM error details"):
                    st.code(st.session_state.get(
                        "last_gradcam_error", "Unknown error"
                    ))

            if (
                st.session_state.get("last_pdf_key") != upload_key
                or "last_pdf" not in st.session_state
            ):
                try:
                    with st.spinner("Preparing diagnostic report..."):
                        pdf_data = create_pdf(
                            result,
                            st.session_state.last_image,
                            gradcam_overlay
                        )
                except Exception as error:
                    st.error(
                        "The PDF report could not be prepared. Please try "
                        "again."
                    )
                    with st.expander("PDF error details"):
                        st.code(f"{type(error).__name__}: {error}")
                else:
                    st.session_state.last_pdf = pdf_data
                    st.session_state.last_pdf_key = upload_key

            if "last_pdf" in st.session_state:
                st.download_button(
                    "Download diagnostic PDF",
                    data=st.session_state.last_pdf,
                    file_name="botanica_diagnostic_report.pdf",
                    mime="application/pdf"
                )


# --------------------------------------------------
# DISEASE ENCYCLOPEDIA
# --------------------------------------------------

elif page == "Disease Encyclopedia":

    st.markdown('<div class="botanical-label">REFERENCE COLLECTION / 02</div>',
                unsafe_allow_html=True)
    st.title("Disease encyclopedia")
    st.write("Browse the crop categories recognized by the model.")

    if model_ready:
        options = class_names
    else:
        options = [
            "Apple___Apple_scab",
            "Apple___Black_rot",
            "Apple___healthy",
            "Corn_(maize)___Common_rust_",
            "Grape___Black_rot",
            "Potato___Early_blight",
            "Potato___Late_blight",
            "Tomato___Early_blight",
            "Tomato___Late_blight",
            "Tomato___healthy"
        ]

    selected = st.selectbox(
        "Select a crop condition",
        options,
        format_func=lambda x: " — ".join(format_disease_name(x))
    )

    info = get_disease_info(selected)

    st.markdown('<div class="report">', unsafe_allow_html=True)
    st.markdown(f"### {info['crop']} / {info['disease']}")
    st.write(info["description"])
    st.markdown("**General guidance**")

    for item in info["management"]:
        st.write("• " + item)

    st.markdown('</div>', unsafe_allow_html=True)

    st.caption(
        "This encyclopedia currently provides general educational "
        "summaries. It is not a complete agricultural treatment database."
    )


# --------------------------------------------------
# COMPARISON LAB
# --------------------------------------------------

elif page == "Comparison Lab":

    st.markdown('<div class="botanical-label">SPECIMEN COMPARISON / 03</div>',
                unsafe_allow_html=True)
    st.title("Healthy vs diseased")
    st.write("Compare two leaf photographs side by side.")

    col1, col2 = st.columns(2)

    with col1:
        healthy_file = st.file_uploader(
            "Upload first specimen",
            type=["jpg", "jpeg", "png"],
            key="compare_one"
        )

    with col2:
        second_file = st.file_uploader(
            "Upload second specimen",
            type=["jpg", "jpeg", "png"],
            key="compare_two"
        )

    if healthy_file and second_file:
        try:
            img1 = load_uploaded_image(healthy_file)
            img2 = load_uploaded_image(second_file)
        except ValueError as error:
            st.error(f"Could not read the uploaded specimens. {error}")
            st.stop()

        left, right = st.columns(2)

        with left:
            st.image(img1, caption="Specimen A", use_container_width=True)

        with right:
            st.image(img2, caption="Specimen B", use_container_width=True)

        if model_ready and st.button("Compare specimens"):
            try:
                with st.spinner("Analyzing both images..."):
                    r1 = run_prediction(img1)
                    r2 = run_prediction(img2)
            except Exception as error:
                st.error(
                    "The specimens could not be compared. Please verify "
                    "both images and try again."
                )
                with st.expander("Comparison error details"):
                    st.code(f"{type(error).__name__}: {error}")
            else:
                a, b = st.columns(2)

                with a:
                    crop, disease = format_disease_name(r1["disease"])
                    st.subheader("Specimen A")
                    st.write(f"**{crop}:** {disease}")
                    st.metric("Prediction score", f"{r1['confidence']:.2f}%")

                with b:
                    crop, disease = format_disease_name(r2["disease"])
                    st.subheader("Specimen B")
                    st.write(f"**{crop}:** {disease}")
                    st.metric("Prediction score", f"{r2['confidence']:.2f}%")

                st.info(
                    "The two predictions are independent. The comparison "
                    "does not establish disease severity or progression."
                )

        elif not model_ready:
            st.warning(
                "Specimen comparison is unavailable because the trained "
                "model could not be loaded. See Home for details."
            )


# --------------------------------------------------
# INTERACTIVE 3D LEAF VIEWER
# --------------------------------------------------

elif page == "3D Leaf Viewer":

    st.markdown('<div class="botanical-label">BOTANICAL MORPHOLOGY / 04</div>',
                unsafe_allow_html=True)
    st.title("Interactive leaf viewer")
    st.write(
        "Explore an illustrative 3D leaf surface. This is an educational "
        "visualization, not a scan of the uploaded specimen."
    )

    u = np.linspace(-1, 1, 90)
    v = np.linspace(0, 1, 90)
    U, V = np.meshgrid(u, v)

    width = 0.55 * np.sin(np.pi * V) ** 0.8
    X = U * width
    Y = V * 2.2
    Z = 0.10 * np.cos(U * np.pi) * np.sin(V * np.pi)

    fig = go.Figure(data=[
        go.Surface(
            x=X,
            y=Y,
            z=Z,
            colorscale=[
                [0, "#78936b"],
                [0.5, "#426b47"],
                [1, "#234331"]
            ],
            showscale=False,
            hoverinfo="skip"
        )
    ])

    # Central leaf vein
    fig.add_trace(go.Scatter3d(
        x=np.zeros(90),
        y=np.linspace(0, 2.2, 90),
        z=0.12 * np.sin(np.linspace(0, np.pi, 90)),
        mode="lines",
        line=dict(color="#e6d9a8", width=5),
        name="Central vein"
    ))

    fig.update_layout(
        height=570,
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="#f4f2e9",
        scene=dict(
            bgcolor="#f4f2e9",
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            aspectmode="manual",
            aspectratio=dict(x=1, y=1.7, z=0.3)
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "Drag to rotate. Select Zoom or Pan in the viewer toolbar, then drag "
        "to adjust the view. Use Reset camera to return to the starting view."
    )


# --------------------------------------------------
# FIELD JOURNAL
# --------------------------------------------------

elif page == "Field Journal":

    st.markdown('<div class="botanical-label">RESEARCH ARCHIVE / 05</div>',
                unsafe_allow_html=True)
    st.title("Field journal")
    st.write("A session-based record of your specimen examinations.")

    if st.session_state.journal:
        journal_df = pd.DataFrame(st.session_state.journal)

        st.dataframe(
            journal_df,
            use_container_width=True,
            hide_index=True
        )

        csv_data = journal_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Export journal as CSV",
            data=csv_data,
            file_name="botanica_field_journal.csv",
            mime="text/csv"
        )

        if st.button("Clear field journal"):
            st.session_state.journal = []
            st.rerun()

    else:
        st.markdown("""
        <div class="specimen">
        <b>NO SPECIMENS RECORDED</b><br><br>
        Your examinations will appear here after you run the leaf scanner.
        </div>
        """, unsafe_allow_html=True)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.markdown("""
<p style="text-align:center;color:#758474;font-size:12px;">
BOTANICA — PLANT DISEASE FIELD LABORATORY<br>
An educational deep-learning project using the PlantVillage dataset.
</p>
""", unsafe_allow_html=True)
