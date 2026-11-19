
from pathlib import Path
import tensorflow as tf

# Dataset directory
DATASET_DIR = Path(
    "dataset/raw/plantvillage dataset/color"
)

# Image configuration
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 4
SEED = 42

def load_datasets():
    if not DATASET_DIR.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_DIR.resolve()}"
        )

    train_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_DIR,
        validation_split=0.20,
        subset="training",
        seed=SEED,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="int"
    )

    val_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_DIR,
        validation_split=0.20,
        subset="validation",
        seed=SEED,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="int"
    )

    class_names = train_ds.class_names

    # Optimize data loading
    train_ds = train_ds.prefetch(buffer_size=1)
    val_ds = val_ds.prefetch(buffer_size=1)

    return train_ds, val_ds, class_names


if __name__ == "__main__":
    train_ds, val_ds, class_names = load_datasets()

    print("\nDataset loaded successfully!")
    print("Number of classes:", len(class_names))
    print("Classes:", class_names)
