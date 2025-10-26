import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import numpy as np
import time

# --- Global Variables for Model and Vectorizer ---
# These will be trained/fitted once when the application starts
MODEL = None
VECTORIZER = None
MOCK_DATASET_SIZE = 500

def create_mock_dataset():
    """
    Creates a small, reproducible mock dataset for demonstration purposes.
    In a real project, this is where you would load your large CSV file.
    """
    print(f"[{time.strftime('%H:%M:%S')}] Generating mock dataset of {MOCK_DATASET_SIZE} entries...")

    # Seeds for reproducible fake content
    fake_headlines = [
        "Exclusive: Secret Mars Colony Discovered by Local Teenager",
        "Breaking: Doctors Recommend Eating Chocolate to Cure All Colds",
        "Urgent: Government Announces Plan to Ban Weekends Starting Next Month",
        "Celebrity Spotted Walking Dog on Water, Says Gravity is a Lie",
        "New Study: Sleeping Upside Down Increases IQ by 50 Points Instantly",
        "Shocking: Cats Found to Be Running a Global Financial Conspiracy"
    ]

    real_headlines = [
        "S&P 500 Closes Lower as Tech Stocks Dip Amidst Inflation Concerns",
        "Local Council Votes to Approve New Pedestrian Bridge Project",
        "The Science of Climate Change: Understanding the Greenhouse Effect",
        "Interview with the Director of the New Documentary on Renewable Energy",
        "Traffic Delays Expected on Highway 101 due to Ongoing Roadwork",
        "Health Officials Advise on New Vaccination Guidelines for Flu Season"
    ]

    # Create the dataset
    data = []
    # Create the headlines, ensuring an approximate 50/50 split
    for i in range(MOCK_DATASET_SIZE // 2):
        data.append({'text': f"Title: {np.random.choice(real_headlines)}. Article body: The details are confirmed. {i}", 'label': 0}) # 0 = Real
        data.append({'text': f"Title: {np.random.choice(fake_headlines)}. Article body: Sources confirm this is true. {i}", 'label': 1}) # 1 = Fake

    # Shuffle the data
    df = pd.DataFrame(data).sample(frac=1).reset_index(drop=True)
    return df

def train_model(df):
    """
    Trains the Logistic Regression model using TF-IDF features.

    Args:
        df (pd.DataFrame): The dataset containing 'text' and 'label' columns.

    Returns:
        tuple: (fitted_model, fitted_vectorizer)
    """
    print(f"[{time.strftime('%H:%M:%S')}] Starting model training...")

    # 1. Feature and Target Split
    X = df['text']
    y = df['label']

    # 2. Train-Test Split (Optional, but good practice to check model performance)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 3. TF-IDF Vectorization
    # Using TfidfVectorizer to convert text data into numerical feature vectors.
    # We limit features to the top 5000 to keep it lightweight.
    tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7, max_features=5000)
    tfidf_train = tfidf_vectorizer.fit_transform(X_train)
    tfidf_test = tfidf_vectorizer.transform(X_test)

    # 4. Logistic Regression Model Training
    # Logistic Regression is a strong baseline for binary classification like this.
    log_reg = LogisticRegression(random_state=42)
    log_reg.fit(tfidf_train, y_train)

    # 5. Evaluation
    y_pred = log_reg.predict(tfidf_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"[{time.strftime('%H:%M:%S')}] Model training complete.")
    print(f"[{time.strftime('%H:%M:%S')}] Validation Accuracy: {accuracy:.4f}")

    return log_reg, tfidf_vectorizer

def classify_news(text):
    """
    Takes a string of news text and returns the classification result.
    """
    global MODEL, VECTORIZER
    if MODEL is None or VECTORIZER is None:
        return "Error: Model or Vectorizer is not initialized."

    # 1. Vectorize the input text using the fitted vectorizer
    input_features = VECTORIZER.transform([text])

    # 2. Get the prediction
    prediction = MODEL.predict(input_features)[0]
    
    # 3. Get the prediction probability (confidence)
    # The output is [[Prob_Real, Prob_Fake]]
    probabilities = MODEL.predict_proba(input_features)[0]

    result = "FAKE" if prediction == 1 else "REAL"
    confidence = probabilities[prediction] * 100

    return result, confidence

def main():
    """
    Main application logic: initializes the model and runs the CLI loop.
    """
    global MODEL, VECTORIZER

    print("=========================================")
    print("  Fake News Detector (TF-IDF + LogReg)   ")
    print("=========================================")

    # 1. Load Data and Train Model
    try:
        data_frame = create_mock_dataset()
        MODEL, VECTORIZER = train_model(data_frame)
    except Exception as e:
        print(f"\n[ERROR] Failed to initialize model: {e}")
        return

    # 2. Start Interactive CLI Loop
    print("\n--- Interactive Testing CLI ---")
    print("Enter a news article/headline to classify (Type 'quit' to exit):")
    print("-------------------------------------")

    while True:
        try:
            user_input = input(">> News Input: ")

            if user_input.lower() in ('quit', 'exit'):
                print("Exiting application. Goodbye!")
                break

            if not user_input.strip():
                print("Please enter some text.")
                continue

            # Classify the input
            classification, confidence = classify_news(user_input)

            # Display results
            if classification == "REAL":
                color_code = "\033[92m" # Green
            else:
                color_code = "\033[91m" # Red
            reset_code = "\033[0m"

            print(f"  {color_code}CLASSIFICATION:{reset_code} {classification}")
            print(f"  {color_code}CONFIDENCE:{reset_code} {confidence:.2f}%")
            print("-------------------------------------")

        except Exception as e:
            print(f"\n[AN ERROR OCCURRED] {e}")
            time.sleep(1)

# Execute the main function
if __name__ == "__main__":
    main()
