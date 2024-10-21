from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
from security.domain.model.user import Role, User
from dependency_injector.wiring import Provide
from shared.container import Container

security = HTTPBearer()

# Configuramos el contenedor
container = Container()
jwtService = container.jwtService()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    user = jwtService.validateJWToken(token=credentials.credentials)
    return user

def authorize_roles(roles: list[Role]):
    def wrapper(current_user: User = Depends(get_current_user)):
        jwtService.authorizeRoles(current_user, roles)
        return current_user
    return wrapper
