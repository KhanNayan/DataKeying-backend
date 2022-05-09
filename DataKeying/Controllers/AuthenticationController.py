from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from DataKeying.Config import  Database 
from DataKeying.Models import Schemas,Models
from DataKeying.Data.Services import token
from DataKeying.Data.Services import oauth2
from sqlalchemy.orm import Session


router = APIRouter(tags=['Authentication'])

get_db = Database.get_db
get_db_entry = Database.get_db_entry


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(Database.get_db)):
    # user = db.query(models.Operator).filter(
    #     models.Operator.OPERATOR_ID == request.username).first()

    user = db.execute(f'SELECT TOP 1 OperatorID,PASSWD,Name FROM Operators where OperatorID = {request.username}');
    user_as_dict = user.mappings().all()
   
    # print(users_as_dict[0])

    if not user_as_dict:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    if not user_as_dict[0].PASSWD == request.password:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")

    access_token = token.create_access_token(data={"sub": str(user_as_dict[0].OperatorID)})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get('/current-user')
def current_user_details(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Invalid Credentials")
    return current_user