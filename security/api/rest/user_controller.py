from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from security.domain.model.user import Role, User
from security.resource.request.update_user_request import UpdateUserRequest
from security.service.authorize import authorize_roles, get_current_user
from security.resource.request.create_user_request import CreateUserRequest
from security.resource.response.user_response import UserResponse
from security.mapping.user_mapper import UserMapper
from security.service.user_service import UserService
from shared.container import Container

# Inyectar el contenedor
# container = Container()
# userService = container.userService()

# Definir el router con prefijo y etiqueta
router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"]
)

# Crear usuario (solo accesible por ADMIN)
@router.post("/create", response_model=UserResponse, dependencies=[Depends(authorize_roles([Role.ADMIN]))])
@inject
async def createUser(request: CreateUserRequest, 
                     userService: UserService = Depends(Provide[Container.userService])):
    user = userService.create(UserMapper.createRequestToModel(request))
    return UserMapper.modelToResponse(user)

# Obtener usuario por nombre de usuario (solo accesible por ADMIN)
@router.get("/by-username/{username}", response_model=UserResponse, dependencies=[Depends(authorize_roles([Role.ADMIN]))])
@inject
async def getUserByUsername(username: str, 
                            userService: UserService = Depends(Provide[Container.userService])):
    user = userService.getByUsername(username)
    return UserMapper.modelToResponse(user)

# Obtener usuario por ID (solo accesible por ADMIN)
@router.get("/by-id/{userId}", response_model=UserResponse, dependencies=[Depends(authorize_roles([Role.ADMIN]))])
@inject
async def getUserById(userId: int, 
                      userService: UserService = Depends(Provide[Container.userService])):
    user = userService.getById(userId)
    return UserMapper.modelToResponse(user)

# Obtener todos los usuarios (solo accesible por ADMIN)
@router.get("/all", response_model=list[UserResponse], dependencies=[Depends(authorize_roles([Role.ADMIN]))])
@inject
async def getAllUsers(userService: UserService = Depends(Provide[Container.userService])):
    users = userService.getAll()
    return [UserMapper.modelToResponse(user) for user in users]

# Actualizar usuario por ID (solo accesible por ADMIN)
@router.put("/update/{userId}", response_model=UserResponse, dependencies=[Depends(authorize_roles([Role.ADMIN]))])
@inject
async def updateUserById(userId: int, 
                         request: UpdateUserRequest, 
                         userService: UserService = Depends(Provide[Container.userService])):
    user = userService.updateById(userId, UserMapper.updateRequestToModel(request))
    return UserMapper.modelToResponse(user)

# Eliminar usuario por ID (solo accesible por ADMIN)
@router.delete("/delete/{userId}", response_model=dict, dependencies=[Depends(authorize_roles([Role.ADMIN]))])
@inject
async def deleteUserById(userId: int, 
                         userService: UserService = Depends(Provide[Container.userService])):
    is_deleted = userService.deleteById(userId)
    return {"is_deleted": is_deleted}

# Obtener información del usuario actual (accesible por USER y ADMIN)
@router.get("/me", response_model=UserResponse, dependencies=[Depends(authorize_roles([Role.USER, Role.ADMIN]))])
@inject
async def getMyUser(currentUser: User = Depends(get_current_user)):
    return UserMapper.modelToResponse(currentUser)

# Actualizar información del usuario actual (accesible por USER y ADMIN)
@router.put("/me", response_model=UserResponse, dependencies=[Depends(authorize_roles([Role.USER, Role.ADMIN]))])
@inject
async def updateMyUser(request: UpdateUserRequest, 
                       currentUser: User = Depends(get_current_user), 
                       userService: UserService = Depends(Provide[Container.userService])):
    user = userService.updateById(currentUser.id, UserMapper.updateRequestToModel(request))
    return UserMapper.modelToResponse(user)

# Eliminar usuario actual (accesible por USER y ADMIN)
@router.delete("/me", response_model=dict, dependencies=[Depends(authorize_roles([Role.USER, Role.ADMIN]))])
@inject
async def deleteMyUser(currentUser: User = Depends(get_current_user), 
                       userService: UserService = Depends(Provide[Container.userService])):
    is_deleted = userService.deleteById(currentUser.id)
    return {"is_deleted": is_deleted}
