from sqlalchemy.orm import Session
from DataKeying.Models import Models, Schemas
from fastapi import HTTPException, status, Response
from ...Models.Models import ImageInfo,ImageDetails
from fastapi.encoders import jsonable_encoder
from ...Models.Models import *

def get_all(db: Session,userId:int):
    # imageData = db.execute(f'SELECT TOP 1 * FROM IMAGE_INFO where OPERATOR_ID = {userId}')
    IMAGE_INFO = ImageInfo()
    imageData = db.query(IMAGE_INFO).filter(IMAGE_INFO.OPERATOR_ID  == userId).all()

    imageData_as_dict = imageData
    return imageData_as_dict

def get_image_serise(db: Session,userId:int):
    #seriseData = db.execute(f'SELECT OPERATOR_ID,DIRECTORY,SERIES_NUMBER FROM IMAGE_INFO where OPERATOR_ID = {userId}')

    IMAGE_INFO = ImageInfo()
    seriseData = db.query(IMAGE_INFO).filter(IMAGE_INFO.OPERATOR_ID  == userId).all()

    seriseData_as_dict = seriseData
    return jsonable_encoder(seriseData_as_dict)


def get_image_index_tagging(db: Session,userId:int,seriseNumber:str):
    #indexTaggingData = db.execute(f"SELECT OPERATOR_ID,SERIES_NUMBER,IMAGE_NUMBER,IMAGE_NAME,CODE FROM IMAGE_DETAILS where OPERATOR_ID = {userId} and SERIES_NUMBER = '{seriseNumber}'")
    
    IMAGE_DETAILS = ImageDetails()
    #indexTaggingData = db.query(IMAGE_DETAILS).filter(IMAGE_DETAILS.OPERATOR_ID  == userId and IMAGE_DETAILS.SERIES_NUMBER == seriseNumber and IMAGE_DETAILS.COMMENTS == 0).all()
    indexTaggingData = db.query(IMAGE_DETAILS).filter(IMAGE_DETAILS.COMMENTS == 0).filter(IMAGE_DETAILS.OPERATOR_ID  == userId).filter(IMAGE_DETAILS.SERIES_NUMBER == seriseNumber).all()

    indexTaggingData_as_dict = indexTaggingData
    return indexTaggingData_as_dict


def get_image_index_entry(db: Session,userId:int,seriseNumber:str):
    IMAGE_DETAILS = ImageDetails()
    indexTaggingData = db.query(IMAGE_DETAILS).filter(IMAGE_DETAILS.COMMENTS == 2).filter(IMAGE_DETAILS.OPERATOR_ID  == userId).filter(IMAGE_DETAILS.SERIES_NUMBER == seriseNumber).all()
    indexTaggingData_as_dict = indexTaggingData
    return indexTaggingData_as_dict


def get_given_name(db: Session):

    # GivenName = Table('GIVENNAMES_Z', meta_data, autoload=True)
    # t = GivenName.insert().values(location='abc',iamge_name='def',x1_coordinate=1.2,y1_cordinate=1.3,tag_name="abc",ai_output="ghi",x2_coordinate=3.4,y2_coordinate=4.5)
    # db.execute(t)
    # db.commit()
    objects = db.query(Models.ImageInfo).with_entities(Models.ImageInfo.IMAGE_COUNT).first()
    return jsonable_encoder(objects)

def update_image_comment(db: Session,data):
    print("Image Number",data.IMAGE_NUMBER)
    IMAGE_DETAILS = Models.ImageDetails()
    objects = db.query(IMAGE_DETAILS).filter(IMAGE_DETAILS.IMAGE_NUMBER == data.IMAGE_NUMBER).first()
    print(objects)
    objects.COMMENTS = data.COMMENTS
    db.commit()
    return jsonable_encoder(objects)


