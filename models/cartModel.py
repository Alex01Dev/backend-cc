from sqlalchemy import Column, Integer, ForeignKey
from config.db import Base

class Cart(Base):
    __tablename__ = "tbd_cart"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("tbb_users.id"))  # depende de tu tabla users
    product_id = Column(Integer, ForeignKey("tbb_products.id"))
    quantity = Column(Integer, nullable=False, default=1)
