import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
# def clean_price(price):
#     cleaned_price = price.replace("\xa0", " ").replace(" ", "").replace("$", "").replace(",", "")
#     return float(cleaned_price)
# df['Prix_CA'] = df['Prix_CA'].apply(clean_price)
# df['Prix_US'] = df['Prix_US'].apply(clean_price)
data = '../get_data/donnees/donnees_total.csv'
df = pd.read_csv(data)
def visualize_data(df):
    # Visualisation de la distribution des classes
    sns.countplot(x='Class', data=df)
    plt.title('Distribution des classes')
    plt.show()

    # Visualisation de la relation entre les caractéristiques numériques et la variable cible
    num_features = df.select_dtypes(include=['float64', 'int64']).columns
    for feature in num_features:
        plt.figure(figsize=(8, 6))
        sns.boxplot(x='Class', y=feature, data=df)
        plt.title(f'Relation entre {feature} et la classe')
        plt.show()

    # Visualisation de la distribution des caractéristiques catégorielles
    cat_features = df.select_dtypes(include=['object']).columns
    for feature in cat_features:
        plt.figure(figsize=(12, 8))
        sns.countplot(x=feature, hue='Class', data=df)
        plt.title(f'Distribution de {feature} par classe')
        plt.xticks(rotation=45)
        plt.show()
    
visualize_data(df)
def encode_categorical(df):
    df_encoded = pd.get_dummies(df, columns=['Nom', 'Compagne_Model', 'Livraison'])
    return df_encoded

# Utilisez la fonction dans votre code
df_encoded = encode_categorical(df)
print(df_encoded.head())
def prepare_data(df):
    X = df.drop('Class', axis=1)  
    y = df['Class']  
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test


