import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import joblib
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')

def load_data(filepath):
    data = pd.read_csv(filepath)
    data.replace('n/a', np.nan, inplace=True)
    data.fillna(0, inplace=True)
    return data

def preprocess_data(data):
    if 'Review' in data.columns:
        data['combined_text'] = data['Review'].astype(str)
    elif 'text' in data.columns and 'title' in data.columns:
        data['combined_text'] = data['title'].astype(str) + " " + data['text'].astype(str)
    else:
        raise ValueError("wrong columns")
    return data['combined_text']

def feature_extraction(text_data):
    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000, sublinear_tf=True)
    features = vectorizer.fit_transform(text_data)
    return vectorizer, features

def augmentFeaturesWithSentimentAnalysis(text_data, features):
    sia = SentimentIntensityAnalyzer()
    sentiment_scores = []

    for text in text_data:
        score = sia.polarity_scores(text)['compound']
        sentiment_scores.append(score) 
    sentiment_scores = np.array(sentiment_scores)

    return np.hstack((features.toarray(), sentiment_scores[:, np.newaxis]))

def train_models(features, data, feature_columns):
    models = {}
    for feature in feature_columns:
        if not np.all(np.isfinite(data[feature])):
            print(f"Non-finite values found in {feature}, skipping...")
            continue
        X_train, X_test, y_train, y_test = train_test_split(features, data[feature], test_size=0.2, random_state=42)
        model = LinearRegression()
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        print(f"Feature: {feature}, MSE: {mse}")
        models[feature] = model
    return models

def predict_sentiments(models, features):
    results = {}
    scaled_results = {}
    for feature, model in models.items():
        predictions = model.predict(features)
        scaled_predictions = scale_scores(predictions)
        results[feature] = predictions 
        scaled_results[feature] = scaled_predictions
    return scaled_results

def aggregate_scores(scores):
    scores_df = pd.DataFrame(scores)
    aggregated_scores = scores_df.mean(axis=0)
    return aggregated_scores

def scale_scores(scores):
    """ Scale scores based on min and max values to 0 to 10. """
    min_val = np.min(scores)
    max_val = np.max(scores)
    if max_val == min_val:
        return np.full(scores.shape, 5.0)  # Neutral score if no variation
    return 10 * (scores - min_val) / (max_val - min_val)

feature_columns = ['Price (value)', 'Quality', 'Aesthetics', 'Customer service', 'Functionality', 'Enjoyable', 'Ease of use']
train_data = load_data('techreviewstrain.csv')
train_texts = preprocess_data(train_data)
vectorizer, train_features = feature_extraction(train_texts)
train_augmented_features = augmentFeaturesWithSentimentAnalysis(train_texts, train_features)
models = train_models(train_augmented_features, train_data, feature_columns)

joblib.dump(models, 'feature_models.pkl')
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')

new_data = load_data('SingleProductReview.csv')
new_texts = preprocess_data(new_data)
new_features = vectorizer.transform(new_texts)  # Use the fitted vectorizer
new_augmented_features = augmentFeaturesWithSentimentAnalysis(new_texts, new_features)

# After prediction
sentiment_scores = predict_sentiments(models, new_augmented_features)
final_scores = aggregate_scores(sentiment_scores)

print("Aggregated sentiment scores for each category:")
for category, score in final_scores.items():
    print(f"{category}: {score:.2f}")
