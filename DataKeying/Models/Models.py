from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey,DateTime,SmallInteger, column,Text
from DataKeying.Config.Database import Base
from sqlalchemy.orm import relationship
from DataKeying.Models.Schemas import ImageInfo


# class Blog(Base):
#     __tablename__ = 'blogs'

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String(100))
#     body = Column(String(100))
  

def Data():
    DATA = Base.classes.DATA
    print("data=",DATA)
    return DATA

def Operator():
    OPERATOR = Base.classes.Operators
    return OPERATOR

def ImageInfo():
    IMAGE_INFO = Base.classes.IMAGE_INFO
    return IMAGE_INFO

def ImageDetails():
    IMAGE_DETAILS = Base.classes.IMAGE_DETAILS
    return IMAGE_DETAILS