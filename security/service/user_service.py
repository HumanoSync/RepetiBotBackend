from fastapi import HTTPException, status
from security.domain.persistence.user_repository import UserRepository
from security.domain.model.user import User
from security.service.auth_service import pwd_context

class UserService:
    def __init__(self, userRepository: UserRepository):
        self.repository = userRepository
    
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
    
    def updateById(self, userId: int, fullName: str):
        userToUpdate = self.getById(userId)
        userToUpdate.full_name = fullName
        return self.repository.save(userToUpdate)
    
    def updatePasswordById(self, userId: int, password: str):
        userToUpdate = self.getById(userId)
        userToUpdate.hashed_password = pwd_context.hash(password)
        return self.repository.save(userToUpdate)
    
    def enableUserById(self, userId: int):
        userToUpdate = self.getById(userId)
        userToUpdate.enabled = True
        return self.repository.save(userToUpdate)
    
    def disableUserById(self, userId: int):
        userToUpdate = self.getById(userId)
        userToUpdate.enabled = False
        return self.repository.save(userToUpdate)

    def deleteById(self, userId: int):
        userToDelete = self.getById(userId)
        self.repository.deleteById(userToDelete.id)
        return True
