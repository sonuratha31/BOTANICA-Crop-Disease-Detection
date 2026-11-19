# BOTANICA — Crop Disease Detection

BOTANICA is an educational B.Tech minor project that uses a trained deep-learning image classifier to explore crop leaf health. Its Streamlit interface combines image-based predictions with disease reference information, a Grad-CAM visualization, a downloadable report, a session-based field journal, specimen comparison, and an illustrative 3D leaf viewer.

## Problem statement

Visible crop diseases can affect plant health and yield, while identifying symptoms from images can be difficult. BOTANICA demonstrates how a convolutional neural network trained on labeled leaf images can classify selected crop conditions. It is a research and learning prototype, not a substitute for field inspection or advice from an agricultural professional.

## Objectives

- Classify an uploaded leaf image among the model's 38 PlantVillage categories.
- Explain the image classification with a Grad-CAM heatmap.
- Present general educational information for the recognized crop condition.
- Provide practical tools to compare specimens, record examinations, and export a PDF report.

## Technology stack

- Python 3.11
- TensorFlow / Keras
- Streamlit
- NumPy, Pandas, and Pillow
- OpenCV for Grad-CAM overlays
- Plotly for the interactive 3D viewer
- ReportLab for PDF reports

The project is configured for CPU inference and does not require GPU setup.

## Dataset

The classifier was trained on the PlantVillage image dataset. The preprocessing code expects color images organized into class-named folders at:

`dataset/raw/plantvillage dataset/color/`

The saved class list contains 38 categories. Dataset loading and preprocessing are used by the training utilities; the Streamlit application does not load the dataset during normal startup or inference.

## Model and reported training results

The existing model is `models/crop_disease_mobilenetv2.keras`. Its architecture is MobileNetV2 with ImageNet weights and the convolutional base frozen, followed by Global Average Pooling, Dropout (0.3), and a 38-unit softmax output layer. The saved model accepts 224 × 224 RGB images. Training configuration in `src/train.py` uses Adam (learning rate 0.001), sparse categorical cross-entropy, batch size 4, and five epochs.

The project-provided results for the completed five-epoch run are:

| Metric | Reported result |
| --- | ---: |
| Training accuracy | 94.36% |
| Validation accuracy | 95.27% |
| Training loss | 0.1970 |
| Validation loss | 0.1866 |

These are the supplied training results; the repository does not include a training log to independently verify them. The trained model and recovery checkpoints are retained in `models/` and `models/recovery/`. Running the application does not train or modify them.

## Features

- **Home:** Project overview and model availability status.
- **Leaf Scanner:** Upload a JPG or PNG image, receive a predicted category and confidence score, and view general educational guidance.
- **Grad-CAM:** View a heatmap overlay showing image regions that contributed to the predicted class.
- **Disease Encyclopedia:** Browse the categories recognized by the loaded model.
- **PDF Diagnosis Report:** Download a report with BOTANICA branding, the uploaded leaf, predicted condition, confidence, report date/time, disease information, and the Grad-CAM overlay and explanation when available.
- **Field Journal:** Review and export scanner records as CSV. Records are session-based and are cleared when the Streamlit session ends.
- **Healthy vs Diseased Comparison:** View two uploaded specimens and compare their independent predictions.
- **3D Leaf Viewer:** Interact with an illustrative leaf surface; it is not generated from an uploaded specimen.

Prediction scores are model outputs, not calibrated probabilities or guarantees of disease presence. Performance on real-world images can differ from performance on the training and validation data.

## Project structure

```text
BOTANICA/
├── app.py
├── requirements.txt
├── README.md
├── models/
│   ├── class_names.txt
│   ├── crop_disease_mobilenetv2.keras
│   └── recovery/
│       ├── epoch-01.keras
│       ├── epoch-02.keras
│       ├── epoch-03.keras
│       ├── epoch-04.keras
│       └── epoch-05.keras
├── src/
│   ├── __init__.py
│   ├── disease_info.py
│   ├── gradcam.py
│   ├── predict.py
│   ├── preprocessing.py
│   └── train.py
└── dataset/
    └── raw/plantvillage dataset/color/
```

## Installation

Use the existing project virtual environment on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

The environment used for project verification was Python 3.11.9, TensorFlow 2.21.0, and Streamlit 1.67.0.

## Run the application

From the project directory, with `.venv` active:

```powershell
python -m streamlit run app.py
```

Open the local URL printed by Streamlit. The model loads on application startup and is cached as a Streamlit resource so reruns reuse the loaded instance.

## Use the Leaf Scanner

1. Open **Leaf Scanner** in the navigation.
2. Upload a clear JPG, JPEG, or PNG image showing a leaf.
3. Select **Run AI examination**.
4. Review the predicted crop condition, score, and general guidance. When available, inspect the Grad-CAM overlay.
5. Download the PDF report if needed. The diagnosis is also recorded in the current session's Field Journal.

For best results, use a well-lit image with a clearly visible leaf. Treat the output as an educational prediction and confirm suspected disease with qualified local expertise.

## Limitations and future improvements

- Training and validation use PlantVillage images; field images may differ in background, lighting, camera quality, crop variety, and symptom severity.
- Model confidence is not calibrated and does not guarantee a diagnosis.
- Encyclopedia content is general guidance, not a complete treatment database.
- The field journal is kept only for the current Streamlit session.
- The 3D leaf model is illustrative and does not represent the uploaded specimen.
- Future work could evaluate the model on independent field images, calibrate confidence, enrich and review the agricultural reference content, and provide persistent user-controlled journal storage.
