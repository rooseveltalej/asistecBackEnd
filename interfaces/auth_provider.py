from abc import ABC, abstractmethod
from controllers.users_controllers import login_user, create_user

class AuthProvider(ABC): 
    @abstractmethod
    def authenticate(self, email: str, password: str) -> bool:
        pass
    
    @abstractmethod
    def check_existance(self, email: str) -> bool:
        pass

    @abstractmethod
    def login(self, user_data, db):
        pass

    @abstractmethod
    def create_user(self, user_data, db):
        pass


class TecAuthProvider(AuthProvider):
    def authenticate(self, email: str, password: str) -> bool:
        # autenticación simulada
        return True

    def check_existance(self, email: str) -> bool:
        return True

    def login(self, user_data, db):
        return login_user(user_data, db)

    def create_user(self, user_data, db):
        return create_user(user_data, db)