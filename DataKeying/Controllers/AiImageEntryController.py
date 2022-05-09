from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from DataKeying.Models import Schemas,Models
from DataKeying.Config import Database
from DataKeying.Data.Services import oauth2
from DataKeying.Config import Database
from sqlalchemy.orm import Session
from DataKeying.Data.Services import AiImageEntry

router = APIRouter(
    prefix="/ImgaeAI",
    tags=['ImageAI']
)

get_db = Database.get_db
get_db_entry = Database.get_db_entry


@router.get('/AiImage')
def allAiImage(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
   return AiImageEntry.get_ai_images_data(db)

@router.post('/AiCoordinate')
def ai_coordinate_insert(request: Schemas.AiImageCoordinate,db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    return AiImageEntry.insert_ai_image_coordinate(request,db);
