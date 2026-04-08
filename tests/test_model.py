import joblib
import numpy as np


def test_model_load_and_predict():
    model = joblib.load("model/model.pkl")
    # Sample iris data: [sepal length, sepal width, petal length, petal width]
    sample_data = [
        [5.1, 3.5, 1.4, 0.2],  # Setosa
        [6.7, 3.1, 4.4, 1.4],  # Versicolour
        [7.2, 3.6, 6.1, 2.5],  # Virginica
    ]
    predictions = model.predict(sample_data)
    assert len(predictions) == 3
    assert all(pred in [0, 1, 2] for pred in predictions)
    # Basic check: first should be 0 (setosa), etc.
    assert predictions[0] == 0
    assert predictions[1] == 1
    assert predictions[2] == 2
