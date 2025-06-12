from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from fastapi.responses import JSONResponse
from typing import Dict
from jwt_manager import create_token
from config.database import Session, engine, Base
from model.movie import Movie as MovieModel
from model.computer import Computer as ComputerModel
from middlewares.error_handler import ErrorHandler
from middlewares.jwt_bearer import JWTBearer
from routers.movie import movie_router
from routers.user import user_router



app = FastAPI()
app.title="Mi primera aplicacion con FastAPI"
app.version = "0.0.1"


app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)


@app.get('/', tags=['home'])
def message():
    return "Hello World Ses"



# Computer Endpoints

class Computer(BaseModel):
    marca: str = Field(default="Marca de la computadora", min_length=3, max_length=20)
    modelo: str = Field(default="Modelo de la computadora", min_length=3, max_length=50)
    color: str = Field(default="Color de la computadora", min_length=3, max_length=20)
    ram: str = Field(default="Cantidad de RAM", min_length=3, max_length=10)
    almacenamiento: str = Field(default="Capacidad de almacenamiento", min_length=3, max_length=20)

    class Config:
        json_schema_extra = {
            "example": {
                "marca": "Dell",
                "modelo": "XPS 13",
                "color": "Silver",
                "ram": "16GB",
                "almacenamiento": "512GB SSD"
            }
        }
    
    
@app.get('/computers', tags=['Computers'], response_model=List[Computer], status_code=200, dependencies=[Depends(JWTBearer())])
def get_computers() -> List[Computer]:
    db = Session()
    result = db.query(ComputerModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.get('/computers/{computer_id}', tags=['Computers'], response_model=Computer, status_code=200, dependencies=[Depends(JWTBearer())])
def get_computer(computer_id: int = Path(ge=1, le=2000)) -> Computer:
    db = Session()
    result = db.query(ComputerModel).filter(ComputerModel.id == computer_id).first()
    if not result:
        return JSONResponse(status_code=404, content={"message": "No se ha encontrado la computadora"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.get('/computers/', tags=['Computers'], response_model=List[Computer], status_code=200, dependencies=[Depends(JWTBearer())])
def get_computer_by_marca(marca: str = Query(min_length=3, max_length=20)) -> List[Computer]:
    db = Session()
    result = db.query(ComputerModel).filter(ComputerModel.marca == marca).all()
    if not result:
        return JSONResponse(status_code=404, content={"message": "No se ha encontrado ninguna computadora con esa marca"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.post('/computers', tags=['Computers'], response_model=dict, status_code=201, dependencies=[Depends(JWTBearer())])
def create_computer(computer: Computer) -> dict:
    db = Session()
    new_computer = ComputerModel(**computer.model_dump())
    db.add(new_computer)
    db.commit()
    db.refresh(new_computer)
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la computadora correctamente"})

@app.put('/computers/{computer_id}', tags=['Computers'], response_model=dict, status_code=200, dependencies=[Depends(JWTBearer())])
def update_computer(computer_id: int, computer: Computer) -> dict:
    db = Session()
    result = db.query(ComputerModel).filter(ComputerModel.id == computer_id).first()
    if not result:
        return JSONResponse(status_code=404, content={"message": "No se ha encontrado la computadora"})
    result.marca = computer.marca
    result.modelo = computer.modelo
    result.color = computer.color
    result.ram = computer.ram
    result.almacenamiento = computer.almacenamiento
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Computadora actualizada correctamente"})

@app.delete('/computers/{computer_id}', tags=['Computers'], response_model=dict, status_code=200, dependencies=[Depends(JWTBearer())])
def delete_computer(computer_id: int) -> dict:
    db = Session()
    result = db.query(ComputerModel).filter(ComputerModel.id == computer_id).first()
    if not result:
        return JSONResponse(status_code=404, content={"message": "No se ha encontrado la computadora"})
    db.delete(result)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Computadora eliminada correctamente"})


