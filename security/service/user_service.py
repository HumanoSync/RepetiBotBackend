from fastapi import HTTPException, status
from security.domain.persistence.user_repository import UserRepository
from security.domain.model.user import User
from passlib.context import CryptContext 

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

class UserService:
    def __init__(self, userRepository: UserRepository):
        self.repository = userRepository
    
    def hashPassword(self, password: str):
        return pwd_context.hash(password)

    def verifyPassword(self, plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)
    
    def authenticate(self, username: str, password: str):
        authenticatedUser = self.repository.findByUsername(username)
        
        if not authenticatedUser or not self.verifyPassword(password, authenticatedUser.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        
        return authenticatedUser
    
    def create(self, user: User):
        if self.repository.findByUsername(user.username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
        
        user.password = self.hashPassword(user.password)
        return self.repository.save(user)
    
    def getByUsername(self, username: str):
        user = self.repository.findByUsername(username)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    
    def getById(self, userId: int):
        user = self.repository.findById(userId)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    
    def getAll(self):
        users = self.repository.findAll()
        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
        return users
    
    def updateById(self, userId: int, user: User):
        userToUpdate = self.getById(userId)
        
        # Actualiza los campos del usuario existente
        userToUpdate.username = user.username or userToUpdate.username
        userToUpdate.password = self.hashPassword(user.password) or userToUpdate.password    
        userToUpdate.phone = user.phone or userToUpdate.phone
        userToUpdate.role = user.role or userToUpdate.role

        return self.repository.save(userToUpdate)

    def deleteById(self, userId: int):
        userToDelete = self.getById(userId)
        self.repository.delete(userToDelete.id)
        return True
