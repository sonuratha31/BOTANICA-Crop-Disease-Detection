# BOTANICA Academic Submission — Final Review

**Review date:** 19 November 2026  
**Scope:** Academic report, presentation, references, screenshots, and a
non-training check of the existing Streamlit application.

## Passed checks

- The PowerPoint opens and contains 12 slides with 6 embedded genuine
  application screenshots. All slides were rendered and visually inspected.
- PowerPoint reports no text-frame overflow, and no slide elements extend
  beyond the slide boundaries. Text and diagrams are readable at full-slide
  size.
- The report contains an abstract and all 20 numbered chapters, including
  methodology, evaluation, limitations, future scope, and references.
- The report and presentation agree on the key project facts:
  - Local dataset inventory: 54,305 images in 38 non-empty class folders;
    published PlantVillage count: 54,306 images and 38 classes. The
    one-image difference is explicitly unresolved.
  - 80/20 training-validation split, seed 42, 224 × 224 input, batch size 4,
    and five epochs.
  - Frozen ImageNet MobileNetV2 base with GlobalAveragePooling2D,
    Dropout(0.3), Dense(38, softmax), Adam (0.001), and sparse categorical
    cross-entropy.
  - The same supplied results: 94.36% training accuracy, 95.27% validation
    accuracy, 0.1970 training loss, and 0.1866 validation loss.
- Supplied metrics are clearly distinguished from independent evaluation.
  The report does not claim test-set metrics, precision, recall, F1,
  calibration, or field-image performance. Example prediction scores are
  identified as examples, not accuracy.
- All 15 screenshot files exist and all 15 links in
  [screenshot-checklist.md](./screenshot-checklist.md) resolve. The report
  uses genuine existing captures; no screenshots or results were fabricated.
- Reference entries contain author or organization, title, year/version,
  publication or documentation source, and DOI or URL as applicable.
  Frontiers, TensorFlow, and Streamlit source pages were reachable during
  this review. DOI links for the IEEE papers resolved to IEEE Xplore, but
  IEEE blocked the browser session with an automated-traffic error (418).
- The running app returned HTTP 200 from its health endpoint. The Home page
  showed the model loaded and 38 categories; the Leaf Scanner page opened
  with JPG/PNG upload support; the 3D Leaf Viewer rendered and exposed
  zoom, pan, rotation, reset, and fullscreen controls.
- No training was run. The model, dataset, recovery checkpoints, and
  application design were not changed.

## Failed or incomplete checks

- Some genuine embedded screenshots retain large black/unused browser-canvas
  areas, especially on slides 1 and 10. The PDF-viewer capture on slide 9
  includes dark viewer chrome, and the 3D screenshot is small at presentation
  size. Images are present, but their framing reduces visual polish.
- Not every external reference destination could be live-checked from this
  environment. The browser could not load the arXiv and Elsevier pages; IEEE
  Xplore returned error 418. These access failures do not establish that the
  DOI records are broken. The reference checklist records the metadata
  verification sources and access limits.
- A new prediction upload and PDF download-button event were not triggered
  during this final review. Prior QA evidence is documented in the report
  and screenshot checklist; this review only rechecked app health,
  navigation, the uploader interface, and the live 3D viewer.

## Corrections made

- Added the missing `College/University: [Institution]` placeholder to the
  presentation title slide. No personal or institutional details were
  invented.
- Updated the report and screenshot checklist to distinguish the live
  3D-viewer control check from what is actually visible in the saved still
  screenshots.
- No application, model, dataset, checkpoint, or dependency files were
  modified.

## Remaining manual tasks

1. Replace the bracketed title/report fields with the student's name,
   roll number, college or university, department, project guide, and
   submission date.
2. Before the live presentation, replace or crop the embedded screenshots
   with genuine captures framed to remove unused black browser canvas.
   Preserve the original screenshot files and do not alter prediction
   content.
3. Open the arXiv, Elsevier, and IEEE DOI links from a normal browser or
   institutional network to confirm access; retain the current bibliographic
   records unless that check identifies a genuine URL or metadata problem.
4. If the submission requires fresh interaction evidence, trigger the PDF
   download once and capture the actual invalid-upload or narrow-viewport
   behavior. These checks are not claimed as completed here.
5. Apply the college's required citation and formatting style.

## Final submission readiness

**Conditionally ready.** The report is complete and internally consistent,
the deck has all 12 slides with no detected text overflow, and the project
evidence is appropriately qualified. Before final submission, complete the
identity fields and improve the framing of the affected slide screenshots.
External reference-link accessibility and a fresh PDF download event remain
unconfirmed. The project is still an educational classifier, not a
field-validated diagnostic service.
