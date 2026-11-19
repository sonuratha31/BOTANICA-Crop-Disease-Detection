# BOTANICA Architecture Diagrams

These diagrams describe the inspected implementation. The training workflow
is separate from normal Streamlit startup and inference. Mermaid diagrams can
be rendered by compatible Markdown viewers.

## 1. Overall system architecture

```mermaid
flowchart LR
    U[User] --> B[Browser]
    B --> UI[Streamlit application: app.py]

    UI --> NAV{Navigation}
    NAV --> HOME[Home and model status]
    NAV --> SCAN[Leaf Scanner]
    NAV --> ENC[Disease Encyclopedia]
    NAV --> CMP[Comparison Lab]
    NAV --> VIEW[3D Leaf Viewer]
    NAV --> JOURNAL[Session Field Journal]

    CACHE[st.cache_resource] --> LOAD[Load saved model and class names]
    LOAD --> MODEL[(crop_disease_mobilenetv2.keras)]
    LOAD --> CLASSES[(class_names.txt)]
    SCAN --> INFER[Image preprocessing and prediction]
    CMP --> INFER
    INFER --> MODEL
    INFER --> CLASSES
    SCAN --> CAM[Grad-CAM explanation]
    CAM --> MODEL
    SCAN --> PDF[ReportLab PDF report]
    CAM --> PDF
    SCAN --> JOURNAL
    ENC --> INFO[Disease information lookup]
    SCAN --> INFO
    VIEW --> PLOTLY[Plotly illustrative surface]

    DATA[(PlantVillage class folders)] -. used by training utilities only .-> TRAIN[Training workflow]
    TRAIN -. saved artifact .-> MODEL
```

## 2. Image upload and prediction workflow

```mermaid
sequenceDiagram
    actor User
    participant UI as Streamlit Leaf Scanner
    participant Decoder as PIL upload validation
    participant Cache as st.cache_resource
    participant Predict as src/predict.py
    participant Model as Saved MobileNetV2 model
    participant Info as Disease information
    participant Outputs as Grad-CAM / PDF / Field Journal

    User->>UI: Upload JPG/JPEG/PNG
    UI->>Decoder: Decode actual file content
    Decoder->>Decoder: Validate JPEG/PNG; convert RGB
    Decoder-->>UI: RGB image
    User->>UI: Run AI examination
    Cache-->>Predict: Reuse loaded model and class list
    Predict->>Predict: Resize to 224x224; array + batch dimension
    Predict->>Predict: Apply MobileNetV2 preprocess_input once
    Predict->>Model: Predict one image
    Model-->>Predict: 38 softmax scores
    Predict->>Predict: Argmax; confidence = selected score x 100
    Predict-->>UI: Class name, confidence, scores
    UI->>Info: Look up class description and guidance
    UI->>Outputs: Generate/cache explanation, report, and session record
    UI-->>User: Display prediction and available outputs
```

## 3. Model training workflow

```mermaid
flowchart TD
    DIR[(PlantVillage color directory<br/>38 class folders)] --> LOAD[image_dataset_from_directory]
    LOAD --> SPLIT[Training subset and 20% validation subset<br/>seed 42]
    SPLIT --> RESIZE[Resize images to 224x224<br/>integer labels; batch size 4]
    RESIZE --> PRE[MobileNetV2 preprocess_input<br/>prefetch buffer 1]
    PRE --> BASE[MobileNetV2<br/>ImageNet weights; include_top=False<br/>base frozen]
    BASE --> GAP[GlobalAveragePooling2D]
    GAP --> DROP[Dropout 0.3]
    DROP --> DENSE[Dense 38; softmax]
    DENSE --> COMPILE[Adam lr 0.001<br/>sparse categorical cross-entropy<br/>accuracy metric]
    COMPILE --> FIT[model.fit up to 5 epochs]
    FIT --> CKPT[Recovery checkpoint each epoch]
    CKPT --> SAVED[(Final .keras model<br/>and class_names.txt)]
```

The training script can resume from valid recovery checkpoints. Training is
not part of normal application startup and was not run during documentation
preparation. The code sets a validation split of 0.20; it does not explicitly
configure a stratified split.

## 4. Grad-CAM explanation workflow

```mermaid
flowchart TD
    IMG[RGB uploaded image] --> RESIZE[Resize to 224x224]
    RESIZE --> PRE[MobileNetV2 preprocess_input]
    PRE --> FEATURE[Connected feature model]
    FEATURE --> ACT[MobileNetV2 out_relu activation]
    FEATURE --> BASEOUT[Base model output]
    BASEOUT --> HEAD[Apply classifier layers]
    HEAD --> SCORE[Select predicted class score]
    ACT --> GRAD[Gradient of score w.r.t. activation]
    SCORE --> GRAD
    GRAD --> POOL[Spatially average gradients]
    POOL --> WEIGHT[Weight feature maps]
    ACT --> WEIGHT
    WEIGHT --> RELU[Sum; ReLU; normalize heatmap]
    RELU --> SCALE[Resize heatmap to original image dimensions]
    SCALE --> COLOR[OpenCV JET color map]
    IMG --> OVERLAY[Blend original 0.55 and heatmap 0.45]
    COLOR --> OVERLAY
    OVERLAY --> DISPLAY[Display overlay]
    OVERLAY --> REPORT[Embed overlay in PDF when available]
```

In the application, the small heatmap is reused from session state for the
same uploaded-image hash. The full-resolution overlay is produced for
display/report use. Grad-CAM is an explanatory visualization, not proof of
disease presence or severity.
