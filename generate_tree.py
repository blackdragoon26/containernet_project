from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
import pickle

# Load iris dataset
X, y = load_iris(return_X_y=True)

# Train a simple tree
clf = DecisionTreeClassifier(max_depth=3, random_state=42)
clf.fit(X, y)

# Save the model
with open('tree_model.pkl', 'wb') as f:
    pickle.dump(clf, f)

print("✅ tree_model.pkl generated!")

