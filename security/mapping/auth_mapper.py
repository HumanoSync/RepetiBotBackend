from security.domain.model.user import User
from security.mapping.user_mapper import UserMapper
from security.resource.request.create_user_request import CreateUserRequest
from security.resource.request.register_user_request import RegisterUserRequest
from security.resource.request.update_user_request import UpdateUserRequest
from security.resource.response.auth_response import AuthResponse 
from security.resource.response.user_response import UserResponse
from security.service.auth_service import pwd_context

class AuthMapper:    
    @staticmethod
    def registerRequestToModel(request: RegisterUserRequest) -> User:
        return User(username=request.username, 
                    email=request.email, 
                    full_name=request.full_name, 
                    hashed_password=pwd_context.hash(request.password))
    
    @staticmethod
    def ModelToResponseWithToken(user: User, accessToken: str) -> AuthResponse:
        userResponse = UserMapper.modelToResponse(user)
        return AuthResponse(access_token=accessToken, 
                            token_type="bearer", 
                            userResponse=userResponse)

