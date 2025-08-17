import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, classification_report

# Simulamos cargar datos (debes reemplazarlo por tus datos reales)
data = pd.DataFrame({
    'carbon_footprint': [1.2, 3.5, 0.8, 4.1, 2.0],
    'recyclable_packaging': [True, False, True, False, True],
    'local_origin': [True, True, False, False, True],
    'category': ['Alimentos', 'Ropa', 'Alimentos', 'Tecnología', 'Ropa'],
    'sustainability_level': [2, 0, 2, 0, 1]  # Etiquetas: 0=baja,1=media,2=alta
})

# Preprocesamiento
data['recyclable_packaging'] = data['recyclable_packaging'].astype(int)
data['local_origin'] = data['local_origin'].astype(int)

# Encoding categoría
data = pd.get_dummies(data, columns=['category'])

# Separar features y target
X = data.drop('sustainability_level', axis=1)
y = data['sustainability_level']

# Dividir en train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modelo
clf = RandomForestClassifier(random_state=42)
clf.fit(X_train, y_train)

# Predicciones
y_pred = clf.predict(X_test)

# Métricas
print("Accuracy:", accuracy_score(y_test, y_pred))
print("F1-score:", f1_score(y_test, y_pred, average='weighted'))
print("Reporte de clasificación:\n", classification_report(y_test, y_pred))
