# BOTANICA Project Report Outline

This outline is grounded in the current BOTANICA implementation and verified
project inventory. Add institutional details, approved citation style, and
primary-source references only after confirming them with the project
submission requirements. Do not present supplied training metrics as
independently reproduced results.

## 1. Introduction

- Introduce the educational crop-leaf image classification problem.
- Explain the project scope: classifying one uploaded image into one of the
  saved PlantVillage categories.
- Describe BOTANICA as a research and learning prototype, not an agricultural
  diagnostic authority.
- Cite verified sources for crop-disease context and image classification;
  completed references [1], [4], and [5] are in
  [report.md](./report.md).

## 2. Problem Statement

- State the project problem: demonstrating image-based classification of crop
  leaf conditions through a usable application.
- Define the input (a supported JPG/JPEG/PNG leaf image) and output (one
  model class and its softmax score shown as a percentage).
- Bound the claim: model scores are not calibrated probabilities and do not
  guarantee disease presence.

## 3. Objectives

- Classify an image among 38 saved disease/healthy categories.
- Apply the trained MobileNetV2 model without retraining it at application
  runtime.
- Provide disease information, a Grad-CAM visualization, a PDF report, a
  session-based field journal, specimen comparison, and an illustrative 3D
  viewer.
- Preserve the trained model and existing project interface.

## 4. Existing System

- Describe manual visual inspection and prior image-classification
  approaches only after sourcing claims from authoritative literature.
- Compare relevant approaches by dataset, model, evaluation protocol, and
  stated limitations.
- Do not claim that manual inspection is inaccurate or that BOTANICA
  outperforms another system without evidence.
- Use verified primary research [1], [4], and [5] in
  [report.md](./report.md); do not compare metrics across differing
  experimental protocols.

## 5. Proposed System

- Present BOTANICA's implemented workflow from upload through model inference,
  disease information, Grad-CAM, and report/journal outputs.
- Distinguish the comparison, encyclopedia, and illustrative viewer features
  from the core prediction path.
- State that the encyclopedia gives general guidance and the 3D surface is
  illustrative, not derived from an uploaded leaf.

## 6. Literature Review

Organize the review around:

- PlantVillage dataset provenance and known dataset characteristics.
- MobileNetV2 and transfer learning for image classification.
- Crop/plant disease classification methods and evaluation practice.
- Grad-CAM and the limits of visual explanations.
- Dataset shift between curated leaf images and field photographs.

For each claim, add a verified primary or authoritative citation. No
references were present in the inspected project documentation; see the
[reference research checklist](./reference-research-checklist.md).

## 7. Technology Stack

- Python 3.11.9, TensorFlow/Keras 2.21.0, and Streamlit 1.67.0 were recorded
  in the previously verified environment.
- NumPy and Pillow support inference/image handling; OpenCV supports the
  Grad-CAM overlay; Plotly renders the 3D viewer; ReportLab builds PDFs;
  Pandas supports the Field Journal.
- `requirements.txt` lists dependencies without version pins. Verify exact
  versions in the submission environment before citing them as fixed
  requirements.

## 8. Dataset Description

- Identify PlantVillage and the local class-folder path:
  `dataset/raw/plantvillage dataset/color/`.
- The current directory inventory contains **54,305 image files across 38
  class folders**. The folders match the saved class-name list.
- State the observed extensions: 54,303 `.jpg`, one `.jpeg`, and one `.png`.
- Explain that training code uses a 20% validation split with seed 42,
  integer labels, and batch size 4.
- Cite the dataset's authoritative source and verify any licensing or
  collection details before submission.

## 9. System Architecture

- Include the diagrams in [Architecture Diagrams](./architecture-diagrams.md).
- Describe `app.py`, prediction/class loading, the saved model, class names,
  Grad-CAM, disease information, PDF generation, and session state.
- Explain that `st.cache_resource` caches model loading and that normal app
  startup does not load the training dataset.

## 10. Methodology

- Describe the two distinct workflows:
  1. training/validation, documented from `src/preprocessing.py` and
     `src/train.py`;
  2. application inference, documented from `src/predict.py` and `app.py`.
- Explain that the training script supports recovery from saved epoch
  checkpoints, but this submission preparation did not run training.
- Avoid implying that application QA is an independent model evaluation.

## 11. Image Preprocessing

- Training data is loaded from class-named directories at 224 × 224 pixels,
  with integer labels and batches of four.
- Training and inference call
  `tf.keras.applications.mobilenet_v2.preprocess_input`.
- Inference decodes a supported image, converts it to RGB, resizes to
  224 × 224, adds a batch dimension, then preprocesses it once.
- The application checks decoded content so a file merely renamed to `.png`
  is not accepted as a PNG if its actual format is unsupported.

## 12. MobileNetV2 Model Architecture

- The saved `.keras` archive contains a Functional model with a nested
  `mobilenetv2_1.00_224` base marked non-trainable.
- Training code creates MobileNetV2 with ImageNet weights and
  `include_top=False`.
- The classifier head is GlobalAveragePooling2D, Dropout (0.3), and a
  38-unit Dense softmax output.
- The saved model input metadata is `[None, 224, 224, 3]`.
- Cite the original architecture [2] and official TensorFlow/Keras
  documentation [6]-[9] in [report.md](./report.md).

## 13. Model Training and Evaluation

- Report the configured optimizer (Adam, learning rate 0.001), loss
  (sparse categorical cross-entropy), accuracy metric, batch size 4, and five
  epochs.
- Explain the 80/20 train/validation configuration and seed 42 from the
  preprocessing code.
- Present the four supplied metrics in a clearly labelled table:

  | Metric | Supplied result |
  | --- | ---: |
  | Training accuracy | 94.36% |
  | Validation accuracy | 95.27% |
  | Training loss | 0.1970 |
  | Validation loss | 0.1866 |

- State prominently that these are supplied project results, not
  independently reproduced during QA; no training log was found. Do not
  relabel validation metrics as test metrics.
- Do not add precision, recall, F1, confusion-matrix, or test-set results
  unless those are produced from a documented evaluation.

## 14. Grad-CAM Explainability

- Describe the selected nested MobileNetV2 activation (`out_relu`), gradient
  calculation for the predicted class, spatially pooled gradient weights,
  weighted activation sum, ReLU, and normalization.
- Explain that the heatmap is resized to the original image, colorized with
  OpenCV JET, and blended with the image (0.55 original, 0.45 heatmap).
- State that Grad-CAM highlights influential image regions; it does not prove
  disease presence, causality, or severity.
- Cite the original Grad-CAM source [3] in
  [report.md](./report.md).

## 15. Application Design and Implementation

- Describe the existing Streamlit navigation: Home, Leaf Scanner, Disease
  Encyclopedia, Comparison Lab, 3D Leaf Viewer, and Field Journal.
- Document cached model loading, per-upload Grad-CAM heatmap reuse, and
  per-upload report-byte reuse.
- Describe the session-based journal, PDF contents, and error presentation.
- Explain that the 3D Plotly surface is generated from a parametric mesh and
  is not a specimen scan.
- Do not redesign or claim additional features not present in the source.

## 16. Testing and Results

- Separate implementation checks, browser feature checks, and model
  evaluation results.
- Report prior QA evidence: scanner prediction and Grad-CAM rendered on a
  PlantVillage example; healthy/diseased comparison, encyclopedia, viewer,
  journal, and PDF generation were exercised.
- A prior browser comparison observed Apple healthy at 100.00% and Apple scab
  at 99.92%. Label these only as outputs for two example images, not as
  accuracy or a held-out evaluation.
- The PDF helper produced valid bytes, embedded the uploaded leaf and
  Grad-CAM image, and paginated long content in a direct helper test.
- State that an actual browser-saved PDF download was not confirmed by the
  browser automation session.
- Include only test procedures and outputs that can be documented or
  reproduced; attach genuine screenshots from the
  [Screenshot Checklist](./screenshot-checklist.md).

## 17. Limitations

- The supplied training results do not establish performance on field images.
- PlantVillage imagery may differ from field conditions in background,
  lighting, camera, crop variety, and symptom severity.
- No independent test-set metrics or calibration results were found.
- Model scores are not calibrated probabilities.
- Disease information is general educational content.
- Grad-CAM is an explanation aid, not proof.
- Field Journal data is session-based; the 3D model is illustrative.

## 18. Future Scope

- Evaluate on a documented, independent set of field images.
- Report appropriate per-class metrics and confusion matrices after a
  reproducible evaluation.
- Investigate class balance, split methodology, data leakage, and confidence
  calibration.
- Review disease guidance with qualified agricultural experts.
- Consider user-controlled persistent journal storage and accessibility
  improvements.
- Any new model training or dataset changes require a separate approved
  project phase.

## 19. Conclusion

- Summarize the implemented educational classification application and its
  integrated explanation/reporting features.
- Restate the scope and limitations without claiming guaranteed diagnosis or
  field-level performance.
- Cite only verified results and note which work remains future evaluation.

## 20. References

- The complete working bibliography is in [report.md](./report.md); adapt
  formatting to the institution's required citation style before submission.
- Source verification notes are in
  [reference-research-checklist.md](./reference-research-checklist.md).

## Suggested appendices

- Verified project specifications and class-list inventory.
- Architecture diagrams.
- Genuine application screenshots.
- Exact environment/version record and test procedure.
- Any authoritative dataset/model sources added during reference research.
