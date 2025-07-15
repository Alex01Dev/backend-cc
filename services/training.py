from sqlalchemy.orm import Session
from models.interactionModel import Interaccion
from models.productsModel import Product
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def entrenar_recomendaciones(db: Session, user_id: int):
    # 1. Obtener interacciones del usuario
    interacciones = db.query(Interaccion).filter(Interaccion.user_id == user_id).all()
    if not interacciones:
        return []

    # 2. Obtener productos con los que ha interactuado
    productos_ids = [i.product_id for i in interacciones]
    productos_vistos = db.query(Product).filter(Product.id.in_(productos_ids)).all()

    # 3. Obtener todos los productos (para recomendar los no vistos)
    todos_productos = db.query(Product).all()
    df = pd.DataFrame([{
        "id": p.id,
        "name": p.name,
        "category": p.category,
        "carbon_footprint": p.carbon_footprint,
        "recyclable_packaging": int(p.recyclable_packaging),
        "local_origin": int(p.local_origin)
    } for p in todos_productos])

    # 4. Combinar campos para similitud (simplificado para demo)
    df["text"] = df["category"] + " " + df["recyclable_packaging"].astype(str) + " " + df["local_origin"].astype(str)

    # 5. Vectorizar con TF-IDF
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(df["text"])

    # 6. Identificar productos que el usuario ya vio
    vistos_idx = df[df["id"].isin(productos_ids)].index
    if vistos_idx.empty:
        return []

    # 7. Calcular similitud entre productos vistos y todos
    similarity_scores = cosine_similarity(tfidf_matrix[vistos_idx], tfidf_matrix)
    avg_scores = similarity_scores.mean(axis=0)

    # 8. Excluir productos ya vistos y ordenar
    df["score"] = avg_scores
    recomendados = df[~df["id"].isin(productos_ids)].sort_values("score", ascending=False)

    # 9. Retornar los mejores N productos recomendados
    return recomendados[["id", "name", "category", "score"]].head(5).to_dict(orient="records")
