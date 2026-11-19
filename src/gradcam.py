
import tensorflow as tf
import numpy as np
import cv2


def generate_gradcam(model, image_array):
    """
    Generate a Grad-CAM heatmap.
    image_array must be preprocessed MobileNetV2 input.
    """

    base_model = next(
        (layer for layer in model.layers if isinstance(layer, tf.keras.Model)),
        None
    )

    if base_model is None:
        raise ValueError(
            "Could not find the MobileNetV2 feature extractor."
        )

    try:
        last_conv = base_model.get_layer("out_relu")
    except ValueError as error:
        raise ValueError(
            "Could not find MobileNetV2's final convolutional activation."
        ) from error

    feature_model = tf.keras.Model(
        inputs=base_model.inputs,
        outputs=[last_conv.output, base_model.output]
    )
    base_index = next(
        index for index, layer in enumerate(model.layers)
        if layer is base_model
    )
    classifier_layers = model.layers[base_index + 1:]

    with tf.GradientTape() as tape:
        conv_outputs, features = feature_model(
            [image_array], training=False
        )
        predictions = features
        for layer in classifier_layers:
            predictions = layer(predictions, training=False)

        class_index = tf.argmax(predictions[0])
        loss = predictions[:, class_index]

    gradients = tape.gradient(loss, conv_outputs)
    if gradients is None:
        raise RuntimeError("Could not calculate gradients for Grad-CAM.")

    pooled_gradients = tf.reduce_mean(
        gradients, axis=(0, 1, 2)
    )

    conv_outputs = conv_outputs[0]

    heatmap = tf.reduce_sum(
        conv_outputs * pooled_gradients,
        axis=-1
    )

    heatmap = tf.maximum(heatmap, 0)
    heatmap = heatmap / (
        tf.reduce_max(heatmap) + 1e-8
    )

    return heatmap.numpy()


def overlay_gradcam(image, heatmap):
    original = np.array(image.convert("RGB"))
    heatmap = cv2.resize(
        heatmap,
        (original.shape[1], original.shape[0])
    )

    heatmap = np.uint8(255 * heatmap)
    colored = cv2.applyColorMap(
        heatmap, cv2.COLORMAP_JET
    )
    colored = cv2.cvtColor(
        colored, cv2.COLOR_BGR2RGB
    )

    result = cv2.addWeighted(
        original, 0.55, colored, 0.45, 0
    )

    return result
