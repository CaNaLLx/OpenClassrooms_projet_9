import numpy as np


def convertir_predictions_setfit(predictions):
    if hasattr(predictions, "detach"):
        predictions = predictions.detach().cpu().numpy()
    mapping = {
        "0": 0, "1": 1,
        "négatif": 0, "positif": 1,
        "negative": 0, "positive": 1,
        "negatif": 0,
    }
    labels = []
    for prediction in np.asarray(predictions).reshape(-1):
        key = str(prediction).strip().lower()
        if key not in mapping:
            raise ValueError(f"Label inconnu : {prediction}")
        labels.append(mapping[key])
    return np.asarray(labels, dtype=int)
