# Verified BOTANICA Project Specifications

## Evidence status

Project files, the saved Keras archive metadata, class names, and dataset
directory inventory were inspected for this documentation pass. Browser QA
facts below refer to previously completed QA sessions. Training was not run,
and the supplied training metrics were not reproduced.

## Dataset

| Property | Verified detail |
| --- | --- |
| Dataset | PlantVillage color-image directory |
| Project path | `dataset/raw/plantvillage dataset/color/` |
| Image files counted in current inventory | 54,305 |
| Class folders | 38 |
| Class-name mapping | `models/class_names.txt` contains 38 names matching the sorted class-folder names |
| File extensions observed | 54,303 `.jpg`, 1 `.jpeg`, 1 `.png` |
| Empty class folders | None |
| Split configured by source | 20% validation via `validation_split=0.20`, seed 42 |
| Dataset-loading implementation | `src/preprocessing.py` |

The code uses `image_dataset_from_directory` with integer labels, image size
224 × 224, batch size 4, and a prefetch buffer of 1. It does not explicitly
request a stratified split or configure data augmentation. Dataset provenance,
licensing, and the original source citation still require authoritative
research.

## Model and training configuration

| Property | Verified detail |
| --- | --- |
| Saved model | `models/crop_disease_mobilenetv2.keras` |
| Saved model format | Keras `.keras` archive; Functional model |
| Input metadata | `[None, 224, 224, 3]` |
| Feature extractor | `mobilenetv2_1.00_224`, non-trainable |
| Backbone configuration in source | `MobileNetV2(weights="imagenet", include_top=False)` |
| Classification head | GlobalAveragePooling2D → Dropout(0.3) → Dense(38, softmax) |
| Optimizer | Adam, learning rate 0.001 |
| Loss / metric | Sparse categorical cross-entropy / accuracy |
| Batch size / epochs | 4 / 5 |
| Recovery files | `models/recovery/epoch-01.keras` through `epoch-05.keras` |
| Training source | `src/train.py` and `src/preprocessing.py` |

The model archive metadata and training source agree on the classifier
structure. The loader also validates the input shape and checks that class
names are unique and match the model output count.

### Supplied training results

These results were supplied for the completed training run and are repeated
in the existing `README.md`. No training log was found, and these metrics
were not independently reproduced during QA.

| Metric | Supplied result |
| --- | ---: |
| Training accuracy | 94.36% |
| Validation accuracy | 95.27% |
| Training loss | 0.1970 |
| Validation loss | 0.1866 |

Do not describe validation accuracy as test accuracy. Do not infer
precision, recall, F1 score, calibration, or real-world performance from
these four values.

## Inference and application

- `app.py` provides Home, Leaf Scanner, Disease Encyclopedia, Comparison Lab,
  3D Leaf Viewer, and Field Journal navigation.
- Model and class loading is wrapped in `st.cache_resource`.
- Normal application startup does not call the training dataset loader.
- `src/predict.py` validates model/class files and model input/output sizes;
  inference converts to RGB, resizes to 224 × 224, applies
  MobileNetV2 preprocessing once, and maps the maximum score to the saved
  class order.
- The displayed confidence is the selected softmax score multiplied by 100.
  It is not a calibrated probability.
- The Field Journal is held in Streamlit session state.
- The PDF includes BOTANICA branding, report date/time, crop/disease,
  confidence, disease information, the uploaded image, and the Grad-CAM
  overlay/explanation when available.
- The Plotly viewer draws an illustrative parametric surface and central
  vein; it is not generated from the uploaded specimen.

## Grad-CAM

`src/gradcam.py` locates the nested MobileNetV2 model and `out_relu` feature
activation, computes gradients for the predicted-class score, spatially pools
the gradients, weights the feature maps, applies ReLU and normalization, then
returns a heatmap. The app resizes and colorizes the heatmap with OpenCV and
blends it with the original image. The heatmap is reused per uploaded-image
hash in session state.

## Technology and environment

The previously verified environment was Python 3.11.9, TensorFlow 2.21.0,
and Streamlit 1.67.0. `requirements.txt` lists TensorFlow, Streamlit, NumPy,
Pandas, Matplotlib, Seaborn, scikit-learn, OpenCV, Pillow, Plotly, and
ReportLab without version pins. Do not infer that every listed package is
used by the inference path.

The application UI and styling are implemented in `app.py`. No separate
stylesheets or page modules were found in the project root/source inventory.

## QA evidence and boundaries

- Prior browser QA exercised the Home page, scanner, encyclopedia,
  comparison, 3D viewer, and Field Journal.
- Genuine unaltered browser captures of the Home page, upload/result states,
  Grad-CAM, encyclopedia, comparison, rendered 3D surface, and session
  journal are included in `docs/academic-submission/screenshots/`.
- A scanner sample displayed Apple scab at 99.92%; comparison samples
  displayed Apple healthy at 100.00% and Apple scab at 99.92%. These are
  outputs for specific PlantVillage examples, not model accuracy or an
  independent evaluation.
- An existing BOTANICA diagnostic PDF was opened in the browser and visually
  inspected. It contains branding, date/time, a sample prediction and score,
  the uploaded image, Grad-CAM overlay, observation, and guidance. A copy is
  included as `botanica-diagnostic-report-example.pdf`. The browser
  download-button event was not re-triggered during the current documentation
  audit.
- The trained model, dataset, and recovery checkpoints were preserved;
  training was not run during QA or this documentation pass. After the
  document audit, the app was started using the project `.venv`; the
  homepage rendered in the integrated browser and reported the model loaded
  with 38 categories. This startup check did not re-test upload, prediction,
  or the PDF download event.

## Project files referenced

- `app.py`
- `src/preprocessing.py`
- `src/train.py`
- `src/predict.py`
- `src/gradcam.py`
- `src/disease_info.py`
- `models/class_names.txt`
- `models/crop_disease_mobilenetv2.keras`
- `models/recovery/epoch-01.keras` through `epoch-05.keras`
- `requirements.txt`
- `README.md`
