from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from implicit.als import AlternatingLeastSquares
import numpy as np

def train_test_split_recommendation(df):
    # Divisez les données en ensembles d'entraînement et de test
    train_data, test_data = train_test_split(df, test_size=0.2, random_state=42)
    return train_data, test_data

def collaborative_filtering(train_data, test_data):
    # Modèle Alternating Least Squares (ALS)
    als_model = AlternatingLeastSquares(factors=50, regularization=0.01, iterations=50)
    item_user_matrix = (train_data[['user_id', 'item_id']].values).T
    als_model.fit(item_user_matrix)
    # Prédiction pour l'ensemble de test
    als_predictions = [als_model.predict(user, item) for user, item in test_data[['user_id', 'item_id']].values]
    # Ajout des prédictions à l'ensemble de test
    test_data['als_predictions'] = als_predictions
    return test_data

def content_based_recommendation(train_data, test_data,input_img):
    # Modèles basés sur le Contenu : Arbres de Décision, Random Forests, Gradient Boosting Machines
    X_train, y_train = train_data[input_img], train_data['Class']
    X_test, y_test = test_data[input_img], test_data['Class']
    # Arbres de Décision
    decision_tree_model = DecisionTreeRegressor()
    decision_tree_model.fit(X_train, y_train)
    dt_predictions = decision_tree_model.predict(X_test)
    # Random Forests
    random_forest_model = RandomForestRegressor()
    random_forest_model.fit(X_train, y_train)
    rf_predictions = random_forest_model.predict(X_test)
    # Gradient Boosting Machines
    gradient_boosting_model = GradientBoostingRegressor()
    gradient_boosting_model.fit(X_train, y_train)
    gb_predictions = gradient_boosting_model.predict(X_test)
    return dt_predictions, rf_predictions, gb_predictions
