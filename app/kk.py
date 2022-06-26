"""
FastAPI app called 'Bookipedia' that serves information about emails and their categories. A simple example of a
"many-to-many" relationship *with* extra data. This solution uses SQLAlchemy Association Proxies
"""

from .db import engine
from .marketplace.models.models import Email, Category, User, EmailCategory

# Insert data
from sqlalchemy.orm import Session
with Session(bind=engine) as session:
    user1 = User(username="user@mail.com", hashed_password="asdsa")

    book1 = Email(message_id="Dead People Who'd Be Influencers Today")
    book2 = Email(message_id="How To Make Friends In Your 30s")

    author1 = Category(name="Blu Renolds")
    author2 = Category(name="Chip Egan")
    author3 = Category(name="Alyssa Wyatt")

    session.add_all([user1, book1, book2, author1, author2, author3])
    session.commit()

    book_author1 = EmailCategory(email_id=book1.id, category_id=author1.id, user_id=1)
    book_author2 = EmailCategory(email_id=book1.id, category_id=author2.id, user_id=1)
    book_author3 = EmailCategory(email_id=book2.id, category_id=author1.id, user_id=1)
    book_author4 = EmailCategory(email_id=book2.id, category_id=author3.id, user_id=1)

    session.add_all([book_author1, book_author2, book_author3, book_author4])
    session.commit()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic

from .marketplace.routes import categories_route, emails_route, users_route

app = FastAPI(message_id="Bookipedia")
security = HTTPBasic()

app.include_router(emails_route.router, prefix="/emails")
app.include_router(categories_route.router, prefix="/categories")
app.include_router(users_route.router, prefix="/users")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()

import uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)