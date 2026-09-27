from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from passlib.context import CryptContext
import datetime

DATABASE_URL = "sqlite:///./store.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    category = Column(String)
    image = Column(String)

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    orders = relationship("OrderModel", back_populates="owner")

    def verify_password(self, password: str):
        return pwd_context.verify(password, self.hashed_password)

    @staticmethod
    def get_password_hash(password: str):
        return pwd_context.hash(password)

class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_amount = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    items_summary = Column(String)

    owner = relationship("UserModel", back_populates="orders")

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    if db.query(ProductModel).count() == 0:
        sample_products = [
            ProductModel(name="Floral Maxi Dress", price=99.00, category="Dresses", image="https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?auto=format&fit=crop&q=80&w=500"),
            ProductModel(name="Silky Slip Dress", price=85.00, category="Dresses", image="https://images.unsplash.com/photo-1595777457583-95e059d581b8?auto=format&fit=crop&q=80&w=500"),
            ProductModel(name="Elegant Gown", price=149.00, category="Evening", image="https://images.unsplash.com/photo-1566174053879-31528523f8ae?auto=format&fit=crop&q=80&w=500"),
            ProductModel(name="Ethereal Sundress", price=79.00, category="Casual", image="https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?auto=format&fit=crop&q=80&w=500"),
            ProductModel(name="Linen Dress", price=110.00, category="Summer", image="https://images.unsplash.com/photo-1539109136881-3be0616acf4b?auto=format&fit=crop&q=80&w=500"),
            ProductModel(name="Velvet Evening Dress", price=185.00, category="Evening", image="https://images.unsplash.com/photo-1583496661160-fb5886a0aaaa?auto=format&fit=crop&q=80&w=500")
        ]
        db.add_all(sample_products)
        db.commit()
    db.close()
  
