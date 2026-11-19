
from pathlib import Path
import tensorflow as tf

from preprocessing import load_datasets, IMAGE_SIZE, BATCH_SIZE

# Configuration
NUM_CLASSES = 38
EPOCHS = 5
MODEL_DIR = Path("models")
MODEL_DIR.mkdir(exist_ok=True)
CHECKPOINT_DIR = MODEL_DIR / "recovery"
CHECKPOINT_DIR.mkdir(exist_ok=True)

# Load dataset
train_ds, val_ds, class_names = load_datasets()

assert len(class_names) == NUM_CLASSES, (
    f"Expected {NUM_CLASSES} classes, got {len(class_names)}"
)

class_names_path = MODEL_DIR / "class_names.txt"
saved_class_names = []
if class_names_path.exists():
    with open(class_names_path, "r", encoding="utf-8") as f:
        saved_class_names = f.read().splitlines()
    if saved_class_names and saved_class_names != class_names:
        raise ValueError(
            "Saved class names do not match the dataset class order."
        )

if not saved_class_names:
    with open(class_names_path, "w", encoding="utf-8") as f:
        f.write("\n".join(class_names))

# MobileNetV2 preprocessing
preprocess = tf.keras.applications.mobilenet_v2.preprocess_input

train_ds = train_ds.map(
    lambda x, y: (preprocess(x), y),
    num_parallel_calls=tf.data.AUTOTUNE
)

val_ds = val_ds.map(
    lambda x, y: (preprocess(x), y),
    num_parallel_calls=tf.data.AUTOTUNE
)

def build_model():
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(*IMAGE_SIZE, 3),
        include_top=False,
        weights="imagenet"
    )
    base_model.trainable = False

    inputs = tf.keras.Input(shape=(*IMAGE_SIZE, 3))
    x = base_model(inputs, training=False)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dropout(0.3)(x)
    outputs = tf.keras.layers.Dense(
        NUM_CLASSES,
        activation="softmax"
    )(x)
    model = tf.keras.Model(inputs, outputs)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )
    return model


def load_recovery_checkpoint():
    checkpoints = []
    for checkpoint_path in CHECKPOINT_DIR.glob("epoch-*.keras"):
        try:
            completed_epoch = int(
                checkpoint_path.stem.removeprefix("epoch-")
            )
        except ValueError:
            continue
        if 1 <= completed_epoch <= EPOCHS:
            checkpoints.append((completed_epoch, checkpoint_path))

    for completed_epoch, checkpoint_path in sorted(
        checkpoints, reverse=True
    ):
        try:
            recovered_model = tf.keras.models.load_model(checkpoint_path)
            if recovered_model.input_shape != (None, *IMAGE_SIZE, 3):
                raise ValueError("Unexpected checkpoint input shape.")
            if recovered_model.output_shape[-1] != NUM_CLASSES:
                raise ValueError("Unexpected checkpoint output shape.")
            if recovered_model.optimizer is None:
                raise ValueError("Checkpoint does not contain optimizer state.")
        except Exception as exc:
            print(
                f"Could not recover checkpoint {checkpoint_path}: {exc}"
            )
            continue

        print(
            f"Resuming from completed epoch {completed_epoch}: "
            f"{checkpoint_path}"
        )
        return recovered_model, completed_epoch

    if checkpoints:
        raise RuntimeError(
            "Recovery checkpoint files were found, but none could be "
            "loaded successfully. Training was stopped to avoid restarting "
            "from epoch 1."
        )

    print("No recovery checkpoint found; starting from epoch 1.")
    return build_model(), 0


model, completed_epochs = load_recovery_checkpoint()
model.summary()

checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=str(CHECKPOINT_DIR / "epoch-{epoch:02d}.keras"),
    save_best_only=False,
    save_weights_only=False,
    save_freq="epoch"
)

model.fit(
    train_ds,
    validation_data=val_ds,
    initial_epoch=completed_epochs,
    epochs=EPOCHS,
    callbacks=[checkpoint_callback]
)

model.save(MODEL_DIR / "crop_disease_mobilenetv2.keras")

print("Training completed!")
print("Model saved successfully.")
