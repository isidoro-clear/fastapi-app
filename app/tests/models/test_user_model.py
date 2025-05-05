import pytest
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from sqlalchemy.exc import IntegrityError

class TestUserModel:
    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.db = db_session
        self.user_data = UserCreate(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="password123"
        )

    def test_create_user(self):
        user = User.create(self.db, self.user_data)
        
        assert user.id is not None
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.email == "john.doe@example.com"
        assert user.password != "password123"  # Password should be hashed

    def test_create_duplicate_email(self):
        # Create first user
        User.create(self.db, self.user_data)
        
        # Try to create second user with same email
        with pytest.raises(ValueError, match="E-mail já registrado"):
            User.create(self.db, self.user_data)

    def test_find_user_by_email(self):
        created_user = User.create(self.db, self.user_data)
        found_user = User.find_by(self.db, email=self.user_data.email)
        
        assert found_user is not None
        assert found_user.id == created_user.id
        assert found_user.email == self.user_data.email

    def test_signin_success(self):
        User.create(self.db, self.user_data)
        login_data = UserLogin(
            username=self.user_data.email,
            password=self.user_data.password
        )
        token = User.signin(self.db, login_data)
        
        assert token is not None
        assert isinstance(token, str)

    def test_signin_wrong_password(self):
        User.create(self.db, self.user_data)
        
        wrong_password_data = UserLogin(
            username="john.doe@example.com",
            password="wrongpassword"
        )
        
        with pytest.raises(ValueError, match="E-mail or password is incorrect"):
            User.signin(self.db, wrong_password_data)

    def test_signin_nonexistent_user(self):
        nonexistent_user = UserLogin(
            username="nonexistent@example.com",
            password="password123"
        )
        
        with pytest.raises(ValueError, match="E-mail or password is incorrect"):
            User.signin(self.db, nonexistent_user) 