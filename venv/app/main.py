
from pydoc import ModuleScanner
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Response, status, Depends
from pydantic import BaseModel

import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models,schemas,utils
from .database import engine,SessionLocal
from .routers import posts,users,auth
from .database import get_db


models.Base.metadata.create_all(bind=engine)




app = FastAPI()





while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database='fastapi',user='postgres', password='moyin',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection was sucessful')
        break
    except Exception as error:
        print('database connection was not sucessful!!')
        print('error:', error)
        time.sleep(2)


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)







