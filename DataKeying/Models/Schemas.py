from typing import List,Text,Optional
from pydantic import BaseModel
from datetime import datetime

class BlogBase(BaseModel):
    title: str
    body: str

class Blog(BlogBase):
    class Config():
        orm_mode = True

class User(BaseModel):
    name:str
    email:str
    password:str

class ShowUser(BaseModel):
    name:str
    email:str
    class Config():
        orm_mode = True

class ShowBlog(BaseModel):
    title: str
    body:str

    class Config():
        orm_mode = True


class Login(BaseModel):
    username: str
    password:str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    OPERATOR_ID: Optional[int] = None


class ShowOperator(BaseModel):
    SHIFT: Optional[str] = None
    OPERATOR_NAME:str
    STATUS: int

    class Config():
        orm_mode = True

class Surname(BaseModel):
     Surname:str

     class Config():
        orm_mode = True                                                                                            

class ImageInfo(BaseModel):
     OPERATOR_ID: int
     START_DATE:datetime
     DIRECTORY:str
     FOLDER_NAME:Optional[str] = None
     SERIES_NUMBER:str
     IMAGE_COUNT:int
     STATUS:int
     YEAR_RANGE:Optional[str] = None
     ENTRY_POS:Optional[int] = None
     TOTAL_FIELD:int

     class Config():
        orm_mode = True

class Project(BaseModel):
    id: int
    projectName: str
    startDate: datetime
    endDate:datetime
    language:int
    country:int
    description:Text
    status:int


class Country(BaseModel):
    id:int
    countryName: str
    description:Text
    status: int


class AiImageCoordinate(BaseModel):
    id:int
    x1_coordinate:Optional[float] = None
    y1_cordinate:Optional[float] = None
    tag_name:Optional[str] = None
    ai_output:Optional[str] = None
    x2_coordinate:Optional[float] = None
    y2_coordinate:Optional[float] = None


class UpdateComment(BaseModel):
   COMMENTS:int
   IMAGE_NUMBER:str 


class Image_detail(BaseModel):
    fieldName:str
    coordinateX:float
    coordinateY:float
    imageName:str
    imageId:str
    line:int
    seriesNumber:str