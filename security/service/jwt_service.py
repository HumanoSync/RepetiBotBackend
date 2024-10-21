from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
import jwt
import os
from security.domain.model.user import Role, User
from security.service.user_service import UserService

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

class JwtService:
    def __init__(self, userService: UserService):
        self.userService = userService

    def createJWToken(self, username: str):
        payload = {
            "username": username,
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        return jwt.encode(payload=payload, key=SECRET_KEY, algorithm=ALGORITHM)

    def validateJWToken(self, token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("username")
            print(f"Decoded username: {username}")
            if username is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
            return self.userService.getByUsername(username)
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    def authorizeRoles(self, user: User, roles: list[Role]):
        if user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
        return True

# 2. Decorador para autorización dinámica por roles
# def authorize_roles(roles: list[str]):
#     def decorator(func):
#         async def wrapper(*args, current_user: User = Depends(get_current_user), **kwargs):
#             auth_service = JwtService(userService=None)  # Inyectar la dependencia de JwtService si es necesario
#             auth_service.authorizeRoles(current_user, roles)
#             return await func(*args, current_user=current_user, **kwargs)
#         return wrapper
#     return decorator