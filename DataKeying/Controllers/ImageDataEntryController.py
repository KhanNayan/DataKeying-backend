from typing import List
from datetime import datetime,date
from fastapi import APIRouter, Depends, status, HTTPException, Response
from DataKeying.Models import Schemas,Models
from DataKeying.Models.Models import Data
from DataKeying.Config import Database
from DataKeying.Data.Services import oauth2
from DataKeying.Config import Database
from sqlalchemy.orm import Session
from DataKeying.Data.Services import ImageDataEntry

router = APIRouter(
    prefix="/Image",
    tags=['ImageInfo']
)

get_db = Database.get_db
get_db_entry = Database.get_db_entry


@router.get('/')
def all(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
   return ImageDataEntry.get_all(db,current_user.OperatorID)

@router.get('/GetSeries')
def get_image_serise(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
   return ImageDataEntry.get_image_serise(db,current_user.OperatorID)


@router.get('/GetIndexTagging/{request}')
def get_image_index_tagging(request:str,db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
   return ImageDataEntry.get_image_index_tagging(db,current_user.OperatorID,request);

@router.get('/GetIndexEntry/{request}')
def get_image_index_entry(request:str,db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
   return ImageDataEntry.get_image_index_entry(db,current_user.OperatorID,request);


@router.get('/GetGivenName')
def get_given_name(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
   return ImageDataEntry.get_given_name(db)

@router.put('/UpdateComment')
def update_image_comment(data:Schemas.UpdateComment,db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
   return ImageDataEntry.update_image_comment(db,data)

@router.get('/GetGivenName')
def get_given_name(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
   return ImageDataEntry.get_given_name(db)


@router.post('/DataInsert', response_model=List[Schemas.Image_detail], status_code=201)
def data_insert(requests: List[Schemas.Image_detail],response:Response,db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    
    DATA = Data()
    columns = [m.key for m in DATA.__table__.columns] 
    res = requests
    
    try:
        for request in requests:
            fieldname = str(request.fieldName)+"_POS"
            if request.fieldName in columns:
                data = db.query(DATA).filter(DATA.LINE == request.line, DATA.IMAGE_NAME == request.imageName).first()
        
                if data!=None:
                    setattr(data,fieldname,f"{requests[0].coordinateX};{requests[0].coordinateY}")
                else:
                
                    data = DATA()
                    setattr(data,fieldname,f"{request.coordinateX};{request.coordinateY}")
                    data.OPERATOR_ID = current_user.OperatorID
                    data.ENTRY_TIME = datetime.now().time()
                    data.ENTRY_DATE = str(date.today())
                    data.SERIES_NUMBER=request.seriesNumber
                    data.LINE = request.line
                    data.IMAGE_NUMBER=request.imageId
                    data.IMAGE_NAME = request.imageName
                    db.add(data)
                db.commit()
                db.refresh(data)
            else:
                res = "No field name exist in database"
    except:
        response.status_code= 400

    return res



@router.get('/DataGet/{imagenumber}', status_code=201)
def data_get(imagenumber:str,response:Response,db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):

    DATA = Data()
    list = []

    try:  
        image = db.query(DATA).filter(DATA.IMAGE_NUMBER == imagenumber).all()

        for i in image:
        
            if i.DEPARTEMENT_POS:

                image_detail={}

                image_detail["fieldName"]="DEPARTMENT"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.DEPARTEMENT_POS.split(";")
                list.append(image_detail)

            if i.ARRONDISSEMENT_POS:

                image_detail={}

                image_detail["fieldName"]="ARRONDISSEMEN"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.ARRONDISSEMENT_POS.split(";")
                list.append(image_detail)
            
            if i.HEADER_COMMUNE_POS:

                image_detail={}

                image_detail["fieldName"]="HEADER_COMMUNE"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.HEADER_COMMUNE_POS.split(";")
                list.append(image_detail)

            if i.HEADER_YEAR_POS:

                image_detail={}

                image_detail["fieldName"]="HEADER_YEAR"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.HEADER_YEAR_POS.split(";")
                list.append(image_detail)

            if i.TITLE_POS:

                image_detail={}

                image_detail["fieldName"]="TITLE"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.TITLE_POS.split(";")
                list.append(image_detail)

            if i.ITEM_NO_POS:

                image_detail={} 

                image_detail["fieldName"]="ITEM_NO"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.ITEM_NO_POS.split(";")
                list.append(image_detail)

            if i.EVENT_TYPE_POS:
                
                image_detail={} 

                image_detail["fieldName"]="EVENT_TYPE"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.EVENT_TYPE_POS.split(";")
                list.append(image_detail)

            if i.ENTRY_NO_POS:
                
                image_detail={} 

                image_detail["fieldName"]="ENTRY_NO"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.ENTRY_NO_POS.split(";")
                list.append(image_detail)

            if i.EVENT_COMMUNE_POS:
                
                image_detail={} 

                image_detail["fieldName"]="EVENT_COMMUNE"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.EVENT_COMMUNE_POS.split(";")
                list.append(image_detail)

            if i.BAPTISM_DATE_POS:
                
                image_detail={} 

                image_detail["fieldName"]="BAPTISM_DATE"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.BAPTISM_DATE_POS.split(";")
                list.append(image_detail)

            if i.R_BAPTISM_DATE_POS:
                
                image_detail={} 

                image_detail["fieldName"]="BAPTISM_DATE"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.R_BAPTISM_DATE_POS.split(";")
                list.append(image_detail)

            if i.MARRIAGE_DATE_POS:
                
                image_detail={} 

                image_detail["fieldName"]="MARRIAGE_DATE"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.MARRIAGE_DATE_POS.split(";")
                list.append(image_detail)
            
            if i.R_MARRIAGE_DATE_POS:
                
                image_detail={} 

                image_detail["fieldName"]="R_MARRIAGE_DATE"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.R_MARRIAGE_DATE_POS.split(";")
                list.append(image_detail)

            if i.BANNS_DATE_POS:
                
                image_detail={} 

                image_detail["fieldName"]="BANNS_DATE"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.BANNS_DATE_POS.split(";")
                list.append(image_detail)

            if i.R_BANNS_DATE_POS:
                
                image_detail={} 

                image_detail["fieldName"]="R_BANNS_DATE"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.R_BANNS_DATE_POS.split(";")
                list.append(image_detail)

            if i.BURIAL_DATE_POS:
                
                image_detail={} 

                image_detail["fieldName"]="BURIAL_DATE"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.BURIAL_DATE_POS.split(";")
                list.append(image_detail)

            if i.R_BURIAL_DATE_POS:
                
                image_detail={} 

                image_detail["fieldName"]="R_BURIAL_DATE"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.R_BURIAL_DATE_POS.split(";")
                list.append(image_detail)

            if i.REGISTER_DATE_POS:
                
                image_detail={} 

                image_detail["fieldName"]="REGISTER_DATE"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.REGISTER_DATE_POS.split(";")
                list.append(image_detail)

            if i.R_REGISTER_DATE_POS:
                
                image_detail={} 

                image_detail["fieldName"]="R_REGISTER_DATE"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.R_REGISTER_DATE_POS.split(";")
                list.append(image_detail)

            if i.GIVENNAME_POS:
                
                image_detail={} 

                image_detail["fieldName"]="GIVENNAME"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.GIVENNAME_POS.split(";")
                list.append(image_detail)

            if i.SURNAME_POS:
                
                image_detail={} 

                image_detail["fieldName"]="SURNAME"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.SURNAME_POS.split(";")
                list.append(image_detail)

            if i.MAIDEN_NAME_POS:
                
                image_detail={} 

                image_detail["fieldName"]="MAIDEN_NAME"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.MAIDEN_NAME_POS.split(";")
                list.append(image_detail)

            if i.ALIAS_GIVENNAME_POS:
                
                image_detail={} 

                image_detail["fieldName"]="ALIAS_GIVENNAME"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.ALIAS_GIVENNAME_POS.split(";")
                list.append(image_detail)

            if i.ALIAS_SURNAME_POS:
                
                image_detail={} 

                image_detail["fieldName"]="ALIAS_SURNAME"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.ALIAS_SURNAME_POS.split(";")
                list.append(image_detail)

            if i.GENDER_POS:
                
                image_detail={} 

                image_detail["fieldName"]="GENDER"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.GENDER_POS.split(";")
                list.append(image_detail)

            if i.AGE_POS:
                
                image_detail={} 

                image_detail["fieldName"]="AGE"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.AGE_POS.split(";")
                list.append(image_detail)

            if i.BIRTH_DATE_POS:
                
                image_detail={} 

                image_detail["fieldName"]="BIRTH_DATE"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.BIRTH_DATE_POS.split(";")
                list.append(image_detail)

            if i.R_BIRTH_DATE_POS:
                
                image_detail={} 

                image_detail["fieldName"]="R_BIRTH_DATE"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.R_BIRTH_DATE_POS.split(";")
                list.append(image_detail)

            if i.BIRTH_PLACE_POS:
                
                image_detail={} 

                image_detail["fieldName"]="BIRTH_PLACE"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.BIRTH_PLACE_POS.split(";")
                list.append(image_detail)

            if i.DEATH_DATE_POS:
                
                image_detail={} 

                image_detail["fieldName"]="DEATH_DATE"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.DEATH_DATE_POS.split(";")
                list.append(image_detail)

            if i.R_DEATH_DATE_POS:
                
                image_detail={} 

                image_detail["fieldName"]="R_DEATH_DATE"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.R_DEATH_DATE_POS.split(";")
                list.append(image_detail)

            if i.FATHER_GIVENNAME_POS:
                
                image_detail={} 

                image_detail["fieldName"]="FATHER_GIVENNAME"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.FATHER_GIVENNAME_POS.split(";")
                list.append(image_detail)

            if i.FATHER_SURNAME_POS:
                
                image_detail={} 

                image_detail["fieldName"]="FATHER_SURNAME"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.FATHER_SURNAME_POS.split(";")
                list.append(image_detail)

            if i.FATHER_AGE_POS:
                
                image_detail={} 

                image_detail["fieldName"]="FATHER_AGE"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.FATHER_AGE_POS.split(";")
                list.append(image_detail)

            if i.FATHER_BIRTH_PLACE_POS:
                
                image_detail={} 

                image_detail["fieldName"]="FATHER_BIRTH_PLACE"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.FATHER_BIRTH_PLACE_POS.split(";")
                list.append(image_detail)
            
            if i.MOTHER_GIVENNAME_POS:
                
                image_detail={} 

                image_detail["fieldName"]="MOTHER_GIVENNAME"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.MOTHER_GIVENNAME_POS.split(";")
                list.append(image_detail)

            if i.MOTHER_SURNAME_POS:
                
                image_detail={} 

                image_detail["fieldName"]="MOTHER_SURNAME"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.MOTHER_SURNAME_POS.split(";")
                list.append(image_detail)

            if i.MOTHER_MAIDEN_NAME_POS:
                
                image_detail={} 

                image_detail["fieldName"]="MOTHER_MAIDEN_NAME"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.MOTHER_MAIDEN_NAME_POS.split(";")
                list.append(image_detail)

            if i.MOTHER_AGE_POS:
                
                image_detail={} 

                image_detail["fieldName"]="MOTHER_AGE"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.MOTHER_AGE_POS.split(";")
                list.append(image_detail)

            if i.MOTHER_BIRTH_PLACE_POS:
                
                image_detail={} 

                image_detail["fieldName"]="MOTHER_BIRTH_PLACE"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.MOTHER_BIRTH_PLACE_POS.split(";")
                list.append(image_detail)

            if i.SPOUSE_GIVENNAME_POS:
                
                image_detail={} 

                image_detail["fieldName"]="SPOUSE_GIVENNAME"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.SPOUSE_GIVENNAME_POS.split(";")
                list.append(image_detail)

            if i.SPOUSE_SURNAME_POS:
                
                image_detail={} 

                image_detail["fieldName"]="SPOUSE_SURNAME"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.SPOUSE_SURNAME_POS.split(";")
                list.append(image_detail)

            if i.SPOUSE_MAIDEN_NAME_POS:
                
                image_detail={} 

                image_detail["fieldName"]="SPOUSE_MAIDEN_NAME"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.SPOUSE_MAIDEN_NAME_POS.split(";")
                list.append(image_detail)

            if i.SPOUSE_ALIAS_GIVENNAME_POS:
                
                image_detail={} 

                image_detail["fieldName"]="SPOUSE_ALIAS_GIVENNAME"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.SPOUSE_ALIAS_GIVENNAME_POS.split(";")
                list.append(image_detail)

            if i.SPOUSE_ALIAS_SURNAME_POS:
                
                image_detail={} 

                image_detail["fieldName"]="SPOUSE_ALIAS_SURNAME"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.SPOUSE_ALIAS_SURNAME_POS.split(";")
                list.append(image_detail)

            if i.SPOUSE_AGE_POS:
                
                image_detail={} 

                image_detail["fieldName"]="SPOUSE_AGE"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.SPOUSE_AGE_POS.split(";")
                list.append(image_detail)

            if i.SPOUSE_BIRTH_DATE_POS:
                
                image_detail={} 

                image_detail["fieldName"]="SPOUSE_BIRTH_DATE"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.SPOUSE_BIRTH_DATE_POS.split(";")
                list.append(image_detail)

            if i.SPOUSE_R_BIRTH_DATE_POS:
                
                image_detail={} 

                image_detail["fieldName"]="SPOUSE_R_BIRTH_DATE"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.SPOUSE_R_BIRTH_DATE_POS.split(";")
                list.append(image_detail)

            if i.SPOUSE_BIRTH_PLACE_POS:
                
                image_detail={} 

                image_detail["fieldName"]="SPOUSE_BIRTH_PLACE"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.SPOUSE_BIRTH_PLACE_POS.split(";")
                list.append(image_detail)

            if i.SPOUSE_GENDER_POS:
                
                image_detail={} 

                image_detail["fieldName"]="SPOUSE_GENDER"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.SPOUSE_GENDER_POS.split(";")
                list.append(image_detail)

            if i.SPOUSE_FATHER_GIVENNAME_POS:
                
                image_detail={} 

                image_detail["fieldName"]="SPOUSE_FATHER_GIVENNA"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.SPOUSE_FATHER_GIVENNAME_POS.split(";")
                list.append(image_detail)

            if i.SPOUSE_FATHER_SURNAME_POS:
                
                image_detail={} 

                image_detail["fieldName"]="SPOUSE_FATHER_SURNAME"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.SPOUSE_FATHER_SURNAME_POS.split(";")
                list.append(image_detail)

            if i.SPOUSE_FATHER_BIRTH_PLACE_POS:
                
                image_detail={} 

                image_detail["fieldName"]="SPOUSE_FATHER_BIRTH_PLACE"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.SPOUSE_FATHER_BIRTH_PLACE_POS.split(";")
                list.append(image_detail)

            if i.SPOUSE_MOTHER_GIVENNAME_POS:
                
                image_detail={} 

                image_detail["fieldName"]="SPOUSE_MOTHER_GIVENNAME"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.SPOUSE_MOTHER_GIVENNAME_POS.split(";")
                list.append(image_detail)

            if i.SPOUSE_MOTHER_SURNAME_POS:
                
                image_detail={} 

                image_detail["fieldName"]="SPOUSE_MOTHER_SURNAME"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.SPOUSE_MOTHER_SURNAME_POS.split(";")
                list.append(image_detail)

            if i.SPOUSE_MOTHER_MAIDEN_NAME_POS:
                
                image_detail={} 

                image_detail["fieldName"]="SPOUSE_MOTHER_MAIDEN_NAME"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.SPOUSE_MOTHER_MAIDEN_NAME_POS.split(";")
                list.append(image_detail)

            if i.SPOUSE_MOTHER_BIRTH_PLACE_POS:
                
                image_detail={} 

                image_detail["fieldName"]="SPOUSE_MOTHER_BIRTH_PLACE"
                image_detail["line"] = i.LINE
                image_detail["imageName"] = i.IMAGE_NAME
                image_detail["imageId"] = i.IMAGE_NUMBER
                image_detail["coordinateX"],image_detail["coordinateY"] = i.SPOUSE_MOTHER_BIRTH_PLACE_POS.split(";")
                list.append(image_detail)

            
    except:
        response.status_code= 400

    
    return list
    