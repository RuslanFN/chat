from pydantic import BaseModel, Field, model_validator
from re import fullmatch
class UserCreate(BaseModel):
    username: str = Field(min_length=5, max_length=20)
    first_name: str = Field(max_length=50)
    second_name: str = Field(max_length=50)
    email: str = Field(max_length=50)
    password: str 
    password_again: str

    @model_validator(mode='after')
    def valid_password(self):
        if self.password == self.password_again:
            return self
        raise ValueError('Пароли не совпадают')

    @model_validator(mode='after')
    def email_validator(self):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'   
        if fullmatch(email_pattern, self.email):
            return self
        raise ValueError('Некорректный email')

class UserInfo(BaseModel):
    username: str = Field(min_length=5, max_length=20)
    first_name: str = Field(max_length=50)
    second_name: str = Field(max_length=50)
    email: str = Field(max_length=50)
