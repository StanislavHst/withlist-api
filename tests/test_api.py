from uuid import uuid4

from fastapi.testclient import TestClient
from database import Base, SessionLocal, engine
from main import app
from models import User, WishList

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["redis"] == "healthy"


def test_get_wishlist():
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        user = User(email=f"{uuid4()}@example.com", hashed_password="unused")
        db.add(user)
        db.flush()
        wishlist = WishList(title="Lab 4", user_id=user.id)
        db.add(wishlist)
        db.commit()
        try:
            response = client.get(f"/wishlists/{wishlist.id}")
            assert response.status_code == 200
            assert response.json()["id"] == wishlist.id
            assert response.json()["title"] == "Lab 4"
        finally:
            db.delete(wishlist)
            db.delete(user)
            db.commit()
