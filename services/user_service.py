import uuid
import jwt
from datetime import datetime, timedelta
from dataclasses import asdict

class UserService:
    def __init__(self, userRepository, roleRepository):
        self.repository = userRepository
        self.roleRepository = roleRepository
        self.secret_key = "e6e5b0db-4fcc-449c-aa80-10b49b8a156c"

    def registerUser(self, username, password, role_name):
        if not username or not password or not role_name:
            return {"code": -32700, "message": "Username, password, and role are required"}
        
        if self.repository.findByName(username):
            return {"code": -32700, "message": "User with this name already exists"}

        role = self.roleRepository.findByName(role_name)
        if not role:
            return {"code": -32700, "message": "Invalid role"}

        self.repository.save(username, password, role.id)
        token = self.generateUserToken(username)
        auth_response = {
            "token": token,
            "user": asdict(self.validateUserToken(token))
        }
        return auth_response

    def loginUser(self, username, password):
        if not username or not password:
            return {"code": -32700, "message": "Username and password are required"}

        if self.repository.authenticate(username, password):
            token = self.generateUserToken(username)
            auth_response = {
                "token": token,
                "user": asdict(self.validateUserToken(token))
            }
            return auth_response
        else:
            return {"code": -32700, "message": "Invalid username or password"}

    def generateUserToken(self, username):
        payload = {
            'username': username,
            'exp': datetime.utcnow() + timedelta(hours=1)  # El token expira en 1 hora
        }
        token = jwt.encode(payload, self.secret_key, algorithm='HS256')
        return token

    def validateUserToken(self, token):
        try:
            decoded = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return self.repository.findByName(decoded['username'])
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")
        
    def getRoleById(self, roleId):
        return self.roleRepository.findById(roleId)
    
