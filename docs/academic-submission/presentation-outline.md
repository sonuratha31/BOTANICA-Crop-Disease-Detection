# BOTANICA B.Tech Minor Project Presentation

**Deck length:** 12 slides  
**Suggested duration:** 8-10 minutes plus questions  
**Citation style:** numbered references keyed to [report.md](./report.md)  
**Visual style:** existing BOTANICA palette (forest green, warm ivory, and
copper); genuine application captures only.

## Slide 1 — BOTANICA: Crop Disease Detection Using Deep Learning

- B.Tech Semester V Minor Project.
- Student, roll number, department, institution, and guide: complete from
  official records.
- One-line summary: educational image classification across 38 saved
  PlantVillage classes.
- **Visual:** `screenshots/01-home-desktop.png`.
- **Speaker note:** this project is an educational prototype, not a
  field-validated diagnostic service.

## Slide 2 — Motivation and Problem

- Plant-leaf imagery is a useful input for a computer-vision demonstration.
- Given one supported JPG/JPEG/PNG image, classify to one of 38 known
  categories.
- The classifier is closed-set and always selects among its saved classes.
- **Visual:** one of the genuine leaf images visible in
  `screenshots/03-leaf-scanner-after-upload.png`.
- **Citations:** PlantVillage research [1, 4]; related plant-disease
  classification research [5].

## Slide 3 — Objectives and User Journey

- Reuse the saved model; do not train during application use.
- Upload -> validate -> RGB/resize/preprocess -> predict -> show class and
  score -> optionally view Grad-CAM, disease information, PDF, and journal.
- Demonstrate comparison and illustrative 3D viewer as separate features.
- **Visual:** compact flow based on `architecture-diagrams.md`.

## Slide 4 — Dataset

- Local directory inventory: **54,305 images, 38 non-empty class folders**.
- Published PlantVillage study reports **54,306 images and 38 classes**
  [1, 4].
- The one-image local/published discrepancy is documented; its reason was
  not determined.
- Configured data split: 80% training / 20% validation, seed 42.
- **Speaker note:** the validation split is not a separate test set.

## Slide 5 — System Architecture

- Streamlit UI: `app.py`; six navigation destinations.
- Cached Keras model and saved class list.
- Prediction, Grad-CAM, disease information, ReportLab PDF, and
  session-based Field Journal.
- Training utilities are separate from normal application startup.
- **Visual:** use the overall architecture diagram from
  `architecture-diagrams.md`.

## Slide 6 — Methodology and Preprocessing

- Decode supported image content, convert to RGB, resize to 224 x 224.
- Convert to a batch and apply MobileNetV2 `preprocess_input` once
  (pixel values scaled to [-1, 1]) [9].
- Select the maximum of 38 model output scores and map it to the saved class
  order.
- **Visual:** inference workflow diagram.

## Slide 7 — MobileNetV2 Model

- ImageNet-pretrained MobileNetV2, `include_top=False`, frozen feature
  extractor [2, 7].
- GlobalAveragePooling2D -> Dropout (0.3) -> Dense(38, softmax).
- Input: 224 x 224 x 3; output: 38 class scores.
- **Visual:** simple five-block model diagram.

## Slide 8 — Training Configuration and Reported Results

- Five epochs; batch size 4; Adam, learning rate 0.001.
- Sparse categorical cross-entropy; accuracy metric.
- Previously reported results: train accuracy 94.36%, validation accuracy
  95.27%, train loss 0.1970, validation loss 0.1866.
- **Caveat:** supplied values, not independently reproduced for this report;
  no independent test-set results.

## Slide 9 — Grad-CAM Explainability

- Gradients for the predicted class at MobileNetV2 `out_relu`; spatially
  pooled weights, weighted feature maps, ReLU, normalization [3].
- Blend: 55% original specimen and 45% colorized heatmap.
- Grad-CAM is an explanation aid, not proof of disease presence or severity.
- **Visual:** `screenshots/04-leaf-scanner-prediction-gradcam.png` or
  `screenshots/13-diagnostic-report-existing-file.png`.

## Slide 10 — BOTANICA Application Features

- Leaf Scanner, Disease Encyclopedia, Comparison Lab, Field Journal, PDF
  report, and illustrative 3D viewer.
- **Visuals:** `screenshots/09-comparison-results.png`,
  `screenshots/11-field-journal.png`, and
  `screenshots/10-3d-leaf-viewer-controls.png`.
- The existing diagnosis report is included as
  `botanica-diagnostic-report-example.pdf`.
- Comparison scores shown are example predictions, not accuracy metrics.

## Slide 11 — Testing and Limitations

- Browser QA: sample prediction and Grad-CAM, encyclopedia, comparison,
  journal, PDF artifact opened in browser, and 3D surface/controls visible.
- Sample Apple scab score 99.92% and Apple healthy score 100.00% belong only
  to the named example inputs.
- No independently reproduced training log, independent test set,
  calibration, or field-image evaluation.
- The PDF artifact was inspected; a new download-button event was not
  triggered during the current documentation audit.

## Slide 12 — Conclusion and Future Scope

- BOTANICA demonstrates a saved-model crop-condition classification workflow
  with explanation and supporting application features.
- Supplied metrics and example scores are clearly distinguished from
  independent evaluation.
- Future scope: independent field-image evaluation, per-class metrics,
  calibration, expert-reviewed guidance, and dataset provenance/licensing
  verification.
- **References:** [1] PlantVillage study; [2] MobileNetV2; [3] Grad-CAM;
  [4]-[5] related plant-disease research; [6]-[12] official framework
  documentation. Full metadata is in `report.md`.

## Presenter checklist

- [ ] Fill title-slide identity fields using verified institutional details.
- [ ] Follow the college's final report and slide citation format.
- [ ] Describe all training numbers as previously reported, not reproduced.
- [ ] Do not call validation accuracy a test result.
- [ ] Do not present example prediction scores as evaluation accuracy.
- [ ] Use screenshots only with the evidence qualifications in
  `screenshot-checklist.md`.
