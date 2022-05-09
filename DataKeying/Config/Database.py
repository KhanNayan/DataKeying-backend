from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

Server = 'GHIT-BPO-003\FARHANSERVER'
# port='8133'
User='sa'
Password ='farhan123'
Database = 'Datakeying'
Driver = 'ODBC Driver 17 for SQL Server'

Server2='10.0.0.9,8233'
# port2='8233'
User2='ghitwt'
Password2='Ghit@@wt135'
Database2='M21025'
Driver2='ODBC Driver 17 for SQL Server'

# SQLALCHAMY_DATABASE_URL = 'mysql+pymysql://root:''@127.0.0.1:3306/p19003'

SQLALCHAMY_DATABASE_URL = f'mssql://{User}:{Password}@{Server}/{Database}?driver={Driver}'

SQLALCHAMY_DATABASE_URL2 = f'mssql://{User2}:{Password2}@{Server2}/{Database2}?driver={Driver2}'

engine = create_engine(SQLALCHAMY_DATABASE_URL,deprecate_large_types=True)

engine2 = create_engine(SQLALCHAMY_DATABASE_URL2,deprecate_large_types=True)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)

SessionLocalEntry = sessionmaker(bind=engine2, autocommit=False, autoflush=False,)



Base = automap_base()
Base.prepare(engine, reflect=True)



BaseEntry= declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_entry():
    dbEntry = SessionLocalEntry()
    try:
        yield dbEntry
    finally:
        dbEntry.close()