# BOTANICA Screenshot Record and Checklist

All files in `screenshots/` were captured from the running local BOTANICA
application with the integrated browser, or are absent as explicitly noted.
The captures are genuine and unaltered. Source images used for prediction
and comparison are existing PlantVillage files in the local dataset; their
results are example outputs, not evaluation metrics.

## Genuine captures saved

| File | Capture and evidence |
| --- | --- |
| [01-home-desktop.png](./screenshots/01-home-desktop.png) | Home page, model-loaded message, recognized category count. |
| [02-leaf-scanner-before-upload.png](./screenshots/02-leaf-scanner-before-upload.png) | Leaf Scanner before selecting an image. |
| [03-leaf-scanner-after-upload.png](./screenshots/03-leaf-scanner-after-upload.png) | Scanner showing an actual Apple scab JPG specimen and image details. |
| [04-leaf-scanner-prediction-gradcam.png](./screenshots/04-leaf-scanner-prediction-gradcam.png) | Actual Apple scab prediction (99.92%), disease guidance, original image and generated Grad-CAM overlay. |
| [04-leaf-scanner-prediction.png](./screenshots/04-leaf-scanner-prediction.png) | Full scanner result and report control after the prediction. |
| [05-disease-information.png](./screenshots/05-disease-information.png) | Scanner result with the model's Apple scab description and general guidance. |
| [07-disease-encyclopedia.png](./screenshots/07-disease-encyclopedia.png) | Encyclopedia displaying Apple scab information. |
| [08-comparison-specimens.png](./screenshots/08-comparison-specimens.png) | Two actual uploaded PlantVillage specimens before running comparison. |
| [09-comparison-results.png](./screenshots/09-comparison-results.png) | Comparison outputs: Apple healthy 100.00% and Apple scab 99.92%. These are sample outputs only. |
| [10-3d-leaf-viewer.png](./screenshots/10-3d-leaf-viewer.png) | Genuine viewer page capture with the rendered illustrative surface. |
| [10-3d-leaf-viewer-controls.png](./screenshots/10-3d-leaf-viewer-controls.png) | Genuine capture of the viewer surface; the toolbar is not clearly visible in this still. Controls were confirmed in the live viewer during final review. |
| [10-3d-leaf-viewer-rotated.png](./screenshots/10-3d-leaf-viewer-rotated.png) | Genuine browser capture from the viewer interaction attempt; the included stills do not clearly show the Plotly toolbar. |
| [11-field-journal.png](./screenshots/11-field-journal.png) | Session journal containing the Apple scab examination generated during browser QA. |
| [12-pdf-download-configuration.png](./screenshots/12-pdf-download-configuration.png) | Scanner result and configured PDF download button. |
| [13-diagnostic-report-existing-file.png](./screenshots/13-diagnostic-report-existing-file.png) | Genuine existing project-generated diagnostic PDF opened in the browser viewer. |

The opened PDF is also included as
[botanica-diagnostic-report-example.pdf](./botanica-diagnostic-report-example.pdf).
It is a real existing output, not a document recreated for these materials.

The PlantVillage files used for sample interactions were an Apple scab image
(`00075aa8-d81a-4184-8541-b692b78d398a___FREC_Scab 3335.JPG`) and an Apple
healthy image
(`0055dd26-23a7-4415-ac61-e0b44ebfaf80___RS_HL 5672.JPG`).

## Still to capture or confirm

- [ ] **PDF download-button event:** an existing genuine report was opened
  and inspected, but the download button was not re-triggered for this
  documentation pass.
- [ ] **Mobile/narrow viewport:** capture a real narrow-width view (for
  example 375 px) if responsive behavior is included in the submission.
- [ ] **Invalid image message:** optional capture of the actual user-facing
  error if invalid-upload handling is discussed.

## Capture provenance and limits

- The screenshots were captured from the genuine local Streamlit app in the
  earlier QA session. The server was stopped during the document audit and
  subsequently restarted; the homepage rendered and reported the model
  loaded with 38 categories. No new application screenshots were fabricated
  during this documentation pass.
- The prediction, comparison, Grad-CAM, and journal screenshots are actual
  application outputs for the local examples above.
- No score in these screenshots is a model accuracy or held-out test
  metric.
- The 3D viewer controls and surface are visible in genuine screenshots.
- The existing PDF file was opened and visually inspected. This is evidence
  of a real report artifact but does not independently prove a fresh browser
  download-button event during the document audit.
