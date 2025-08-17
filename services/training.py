from sqlalchemy.orm import Session
from models.interactionModel import Interaccion
from models.productsModel import Product
from schemas.productSchemas import StatusProducto
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import pandas as pd

def entrenar_recomendaciones(db: Session, user_id: int):
    # 1. Obtener interacciones del usuario
    interacciones = db.query(Interaccion).filter(Interaccion.user_id == user_id).all()
    if not interacciones:
        return []

    # 2. Obtener productos con los que ha interactuado
    productos_ids = [i.product_id for i in interacciones]

    # 3. Obtener todos los productos DISPONIBLES y con stock > 0
    todos_productos = db.query(Product).filter(
        Product.status == StatusProducto.disponible.value,
        Product.quantity > 0
    ).all()

    if not todos_productos:
        return []

    # 4. Construir dataframe
    df = pd.DataFrame([{
        "id": p.id,
        "name": p.name,
        "category": p.category,
        "carbon_footprint": p.carbon_footprint,
        "recyclable_packaging": int(p.recyclable_packaging),
        "local_origin": int(p.local_origin),
        "price": p.price
    } for p in todos_productos])

    # 5. Combinar campos de texto para similitud
    df["text"] = (
        df["category"] + " " +
        df["recyclable_packaging"].astype(str) + " " +
        df["local_origin"].astype(str)
    )

    # 6. Vectorizar con TF-IDF
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(df["text"])

    # --- Clustering con K-Means ---
    n_clusters = min(5, len(df))  # evitar error si hay pocos productos
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(tfidf_matrix)
    df["cluster"] = clusters

    sil_score = silhouette_score(tfidf_matrix, clusters) if len(df) > 1 else 0.0

    # 7. Calcular similitud con productos que el usuario vio
    vistos_idx = df[df["id"].isin(productos_ids)].index
    if vistos_idx.empty:
        return []

    similarity_scores = cosine_similarity(tfidf_matrix[vistos_idx], tfidf_matrix)
    avg_scores = similarity_scores.mean(axis=0)

    # 8. Normalizar huella de carbono (menor = mejor)
    max_footprint = df["carbon_footprint"].max()
    min_footprint = df["carbon_footprint"].min()
    df["carbon_score"] = 1 - (df["carbon_footprint"] - min_footprint) / (max_footprint - min_footprint + 1e-6)

    # 9. Normalizar precio (más barato = mejor score relativo)
    max_price = df["price"].max()
    min_price = df["price"].min()
    df["price_score"] = 1 - (df["price"] - min_price) / (max_price - min_price + 1e-6)

    # 10. Score sustentabilidad
    df["sustentabilidad_score"] = (
        df["carbon_score"] + df["recyclable_packaging"] + df["local_origin"]
    ) / 3

    # 11. Score final (puedes tunear pesos según prefieras)
    df["score"] = (
        0.5 * avg_scores +           # similitud con lo que ya vio
        0.3 * df["sustentabilidad_score"] +  # conciencia ambiental
        0.2 * df["price_score"]      # accesibilidad en precio
    )

    # 12. Excluir productos ya vistos y ordenar
    recomendados = df[~df["id"].isin(productos_ids)].sort_values("score", ascending=False)

    return {
        "silhouette_score": sil_score,
        "clusters": df[["id", "name", "cluster"]].to_dict(orient="records"),
        "recomendaciones": recomendados[["id", "name", "category", "price", "score"]].head(5).to_dict(orient="records")
    }
