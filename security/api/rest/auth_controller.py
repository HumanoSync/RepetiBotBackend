from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from security.resource.request.register_user_request import RegisterUserRequest
from security.resource.request.login_user_request import LoginUserRequest
from security.resource.response.auth_response import AuthResponse
from security.mapping.user_mapper import UserMapper
from security.service.jwt_service import JwtService
from security.service.user_service import UserService
from shared.container import Container

# Definir el router con prefijo y etiqueta
router = APIRouter(
    prefix="/api/v1/auth",  # Prefijo para todas las rutas de autenticación
    tags=["auth"]  # Etiqueta que agrupa las rutas bajo "auth"
)

# Registro de usuario
@router.post("/register", response_model=AuthResponse)
@inject
async def registerUser(request: RegisterUserRequest,
                        userService: UserService = Depends(Provide[Container.userService]),
                        jwtService: JwtService = Depends(Provide[Container.jwtService])):
    user = userService.create(UserMapper.registerRequestToModel(request))
    token = jwtService.createJWToken(user.username)
    return UserMapper.ModelToResponseWithToken(user, token)

# Inicio de sesión
@router.post("/login", response_model=AuthResponse)
@inject
async def loginUser(request: LoginUserRequest,
                    userService: UserService = Depends(Provide[Container.userService]),
                    jwtService: JwtService = Depends(Provide[Container.jwtService])):
    user = userService.authenticate(request.username, request.password)
    token = jwtService.createJWToken(user.username)
    return UserMapper.ModelToResponseWithToken(user, token)

