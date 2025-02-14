import joblib

def save(self):
    """Save the trained HDBSCAN model"""
    print(f"Saving model to {self.model_path}")
    return joblib.dump(self.model, self.model_path)

def load(self):
    """Load the trained HDBSCAN model"""
    print(f"Loading model from {self.model_path}")
    return joblib.load(self.model_path)
