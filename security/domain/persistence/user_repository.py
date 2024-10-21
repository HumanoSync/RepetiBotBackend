from sqlmodel import Session, select
from security.domain.model.user import User
from shared.database import getSession

class UserRepository:
    def __init__(self):
        pass  # No necesitas inyectar la sesión directamente

    def findByUsername(self, username: str) -> User:
        with getSession() as session:
            query = select(User).where(User.username == username)
            return session.exec(query).first()

    def findById(self, userId: int) -> User:
        with getSession() as session:
            query = select(User).where(User.id == userId)
            return session.exec(query).first()

    def findAll(self) -> list[User]:
        with getSession() as session:
            query = select(User)
            return session.exec(query).all()

    def save(self, user: User):
        with getSession() as session:
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        
    def delete(self, userId: int):
        with getSession() as session:
            user = session.get(User, userId)
            if user:
                session.delete(user)
                session.commit()
