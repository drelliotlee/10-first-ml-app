import logging
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import joblib
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def train():
    logger.info("Loading iris dataset...")
    iris = load_iris()

    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=0.2, random_state=42
    )

    logger.info("Training logistic regression model...")
    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)
    logger.info(f"Accuracy: {accuracy:.4f}")

    Path("models").mkdir(exist_ok=True)
    joblib.dump(model, "models/model.pkl")
    logger.info("Model saved to models/model.pkl")


if __name__ == "__main__":
    train()
