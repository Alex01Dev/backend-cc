import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import os

def cargar_datos_interacciones():   
    current_dir = os.path.dirname(__file__)
    path = os.path.join(current_dir, "simulated_interactions.csv")
    return pd.read_csv(path)
def generar_recomendaciones(user_id: int, top_n: int = 3):
    df = cargar_datos_interacciones()

    # Pivot table: users × products
    pivot = df.pivot_table(index='user_id', columns='product_id', values='interaction', fill_value=0)

    if user_id not in pivot.index:
        return []  # Usuario sin interacciones

    # Calcular similitud entre usuarios
    similarity_matrix = cosine_similarity(pivot)
    similarity_df = pd.DataFrame(similarity_matrix, index=pivot.index, columns=pivot.index)

    # Obtener usuarios similares
    similares = similarity_df[user_id].sort_values(ascending=False).drop(user_id)

    # Obtener productos recomendados
    productos_vistos = set(df[df['user_id'] == user_id]['product_id'])
    recomendaciones = {}

    for similar_user in similares.index:
        productos_similar = df[df['user_id'] == similar_user]['product_id']
        for producto in productos_similar:
            if producto not in productos_vistos:
                recomendaciones[producto] = recomendaciones.get(producto, 0) + 1

    # Devolver los top_n productos más recomendados
    recomendaciones_ordenadas = sorted(recomendaciones.items(), key=lambda x: x[1], reverse=True)
    return [prod_id for prod_id, _ in recomendaciones_ordenadas[:top_n]]
