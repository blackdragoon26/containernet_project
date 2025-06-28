import requests
import numpy as np
from sklearn.datasets import load_iris

X, _ = load_iris(return_X_y=True)
sample = X[0].tolist()

r = requests.post('http://10.0.0.251:5000/infer', json={'features': sample, 'node': 0})
print(r.json())

