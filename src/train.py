import logging
import csv
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from src.utils import save_model
from src.preprocess import FEATURES, PROCESSED_DATA_PATH

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def train():
    logger.info(f"Loading processed data from {PROCESSED_DATA_PATH}...")
    X, y = [], []
    with open(PROCESSED_DATA_PATH) as f:
        reader = csv.DictReader(f)
        for row in reader:
            X.append([float(row[feature]) for feature in FEATURES])
            y.append(int(row["rained_tomorrow"]))

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    logger.info("Training logistic regression model...")
    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)
    logger.info(f"Accuracy: {accuracy:.4f}")

    save_model(model)


if __name__ == "__main__":
    train()
