import re
from sqlalchemy.orm import Session
from DataKeying.Models import Models, Schemas
from fastapi import HTTPException, status



def get_all(db: Session,userId:int):
    imageData = db.execute(f'SELECT TOP 1 * FROM IMAGE_INFO where OPERATOR_ID = {userId}')
    imageData_as_dict = imageData.mappings().all()
    return imageData_as_dict

def get_ai_images_data(db: Session):
    aiImageData = db.execute(f'SELECT * FROM Tag')
    imageData_as_dict = aiImageData.mappings().all()
    return imageData_as_dict


def insert_ai_image_coordinate(request: Schemas.AiImageCoordinate,db: Session):
    aiCoordinate = db.execute(f"update Tag SET x1_coordinate ='{request.x1_coordinate}' , y1_cordinate ='{request.y2_coordinate}',tag_name='{request.tag_name}', ai_output='{request.ai_output}',x2_coordinate='{request.x2_coordinate}',y2_coordinate='{request.y2_coordinate}'  where id = {request.id}")
    return "upadate"