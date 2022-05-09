from sqlalchemy.orm import Session
from DataKeying.Models import Schemas
from fastapi import HTTPException, status
from DataKeying.Models.Models import Operator
from fastapi.encoders import jsonable_encoder


def  get_operator(id: str,db: Session):

    operator = Operator()
    operator = db.query(operator).filter(operator.OperatorID  == id).first()

    # operator = db.execute(f'SELECT TOP 1 OperatorID,PASSWD,Name FROM Operators where OperatorID = {id}');
    operator_as_dict = operator

    if not operator_as_dict:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Operate with the id {id} is not available")
    return operator_as_dict