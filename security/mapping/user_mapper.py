from security.domain.model.user import User
from security.resource.request.create_user_request import CreateUserRequest
from security.resource.request.register_user_request import RegisterUserRequest
from security.resource.request.update_user_request import UpdateUserRequest
from security.resource.response.auth_response import AuthResponse
from security.resource.response.user_response import UserResponse

class UserMapper:    
    # Metodos de auth controller
    @staticmethod
    def registerRequestToModel(request: RegisterUserRequest) -> User:
        return User(username=request.username, password=request.password, phone=request.phone)
    
    @staticmethod
    def ModelToResponseWithToken(user: User, access_token: str) -> AuthResponse:
        userResponse = UserMapper.modelToResponse(user)
        return AuthResponse(access_token=access_token, token_type="bearer", userResponse=userResponse)
    
    # Metodos de user controller
    @staticmethod
    def createRequestToModel(request: CreateUserRequest) -> User:
        return User(username=request.username, password=request.password, phone=request.phone, role=request.role)
    
    @staticmethod
    def updateRequestToModel(request: UpdateUserRequest) -> User:
        return User(username=request.username, password=request.password, phone=request.phone, role=request.role)
        
    @staticmethod
    def modelToResponse(user: User) -> UserResponse:
        return UserResponse(id=user.id, username=user.username, phone=user.phone, role=user.role.value)

