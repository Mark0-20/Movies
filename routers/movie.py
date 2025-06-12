from fastapi import Path, Query, Depends, APIRouter
from pydantic import BaseModel, Field
from typing import Optional, List
from fastapi.responses import JSONResponse
from typing import Dict
from jwt_manager import create_token, validate_token
from config.database import Session
from model.movie import Movie as MovieModel
from middlewares.error_handler import ErrorHandler
from middlewares.jwt_bearer import JWTBearer
from fastapi.encoders import jsonable_encoder
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()


@movie_router.get('/movies', tags=['Movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=200, content= jsonable_encoder(result))   

@movie_router.get('/movies/{movie_id}', tags=['Movies'], response_model=Movie, dependencies=[Depends(JWTBearer())])
def get_movie(movie_id: int= Path(ge=1, le=200)) -> Movie:
    db = Session()
    result = MovieService(db).get_movie_by_id(movie_id)
    if not result:
        return JSONResponse(status_code=200, content= {"message" : "Pelicula no encontrada"})
    return JSONResponse(status_code=404,content= jsonable_encoder(result))

@movie_router.get('/movies/', tags=['Movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movie_by_category(category: str  = Query(min_length=5, max_length=25)) -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies_by_category(category)
    if not result:
        return JSONResponse(status_code=404, content={"message": "No se encontraron peliculas de esa categoria"})
    return JSONResponse(content= jsonable_encoder(result))

@movie_router.post('/movies', tags=['Movies'], response_model= dict, status_code=201, dependencies=[Depends(JWTBearer())])
def create_movie(movie: Movie) -> dict:
    db = Session()
    MovieService(db).create_movie(movie.model_dump())
    return JSONResponse(status_code=201 ,content= {"message": "Se ha registrado correctamente"})

@movie_router.put('/movies/{movie_id}', tags=['Movies'], response_model= dict, status_code=200, dependencies=[Depends(JWTBearer())])
def update_movie(movie_id: int, movie: Movie) -> dict:
    db = Session()
    result = MovieService(db).get_movie_by_id(movie_id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "Pelicula no encontrada"})
    MovieService(db).update_movie(movie_id, movie.model_dump())
    return JSONResponse(status_code=200,content= {"message": "Se ha actualizado la pelicula correctamente"})

@movie_router.delete('/movies/{movie_id}', tags=['Movies'], response_model= dict, status_code=200, dependencies=[Depends(JWTBearer())])
def delete_movie(movie_id: int) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not result:
        return JSONResponse(status_code=404, content={"message": "Pelicula no encontrada"})
    MovieService(db).delete_movie(movie_id)
    return JSONResponse(status_code=200,content= {"message": "Se ha eliminado la pelicula correctamente"})
