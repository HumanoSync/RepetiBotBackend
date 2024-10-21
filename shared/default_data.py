from security.domain.model.user import User, Role
from security.domain.persistence.user_repository import UserRepository
from security.service.user_service import pwd_context

def defaultData(userRepository: UserRepository):
    if not userRepository.findByUsername("slayer32510"):
        userRepository.save(User(
            username="slayer32510", 
            password=pwd_context.hash("@rduino4141!"), 
            phone="995240514",
            role=Role.ADMIN))
