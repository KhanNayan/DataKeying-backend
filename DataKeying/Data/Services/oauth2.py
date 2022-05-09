from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from DataKeying.Config import Database
from DataKeying.Data.Services import token
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

get_db = Database.get_db

def get_current_user(data: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    return token.verify_token(data, credentials_exception,db)
