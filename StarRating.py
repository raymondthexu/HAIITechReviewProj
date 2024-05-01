import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
import nltk
nltk.download('vader_lexicon')

def load_data(filepath, is_training_data=False):
    data = pd.read_csv(filepath)
    required_columns = ['text', 'stars'] if is_training_data else ['Review']
    missing_cols = [col for col in required_columns if col not in data.columns]
    if missing_cols:
        raise ValueError(f"CSV {filepath} is missing required columns: {missing_cols}")
    data.dropna(subset=required_columns, inplace=True)
    return data

def train_model(X_train, y_train):
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english')),
        ('regressor', LinearRegression())
    ])
    pipeline.fit(X_train, y_train)
    return pipeline

def predict_ratings(model, X_test):
    predictions = model.predict(X_test)
    return np.clip(predictions, 1, 5)  # Restricts range to 1-5 stars

def aggregate_ratings(predictions):
    return np.round(np.mean(predictions), 1) if predictions.size > 0 else 0

def compare_ratings(actual, predicted):
    print(f"Actual Rating: {actual} Stars")
    print(f"Predicted Rating: {predicted} Stars")
    difference = actual - predicted
    print(f"Difference: {difference} Stars")
    return difference

def adjust_model_based_on_feedback(model, X_train, y_train, additional_data, weight=10):
    """ Adjust the model based on user feedback with weighted average. """

    print(f"Weight used to adjust prediction: {10}")
    # Create dataframe with weights for new data
    new_X = pd.Series([additional_data['text']] * weight)
    new_y = pd.Series([additional_data['stars']] * weight)
    
    # Add new data to original training set
    X_train_augmented = pd.concat([X_train, new_X])
    y_train_augmented = pd.concat([y_train, new_y])
    
    # Retrain the model with the augmented dataset
    model.fit(X_train_augmented, y_train_augmented)
    return model

if __name__ == "__main__":
    train_data = load_data('techreviewstrain.csv', is_training_data=True)
    X_train, y_train = train_data['text'], train_data['stars']

    model = train_model(X_train, y_train)

    test_data = load_data('SingleProductReview.csv', is_training_data=False)
    X_test = test_data['Review']
    predicted_ratings = predict_ratings(model, X_test)
    overall_rating = aggregate_ratings(predicted_ratings)
    print(f"Overall Predicted Star Rating: {overall_rating} Stars")

    actual_rating = float(input("Please enter the actual Amazon star rating: "))
    difference = compare_ratings(actual_rating, overall_rating)

    if input("Would you like to adjust the model based on this result? (yes/no) ").lower() == 'yes':
        additional_data = {'text': test_data['Review'].iloc[0], 'stars': actual_rating}
        model = adjust_model_based_on_feedback(model, X_train, y_train, additional_data)
        print("Model has been adjusted based on the new data.")

        # Adjusted model output
        new_predictions = predict_ratings(model, X_test)
        new_overall_rating = aggregate_ratings(new_predictions)
        print(f"New Overall Predicted Star Rating: {new_overall_rating} Stars")
