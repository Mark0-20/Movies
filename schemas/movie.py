from pydantic import BaseModel, Field
from typing import Optional



class Movie(BaseModel):
    title: str = Field(default="Titulo de la pelicula", min_lenght=5, max_lenght=15)
    overview: str = Field(default="Descripción de la pelicula", min_lenght=5, max_lenght=100)
    year: int = Field(default="2000", le=2025)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_lenght=5, max_lenght=15)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Mi pelicula",
                "overview": "Descripcion de la pelicula",
                "year": 2025,
                "rating": 6.6,
                "category": "Accion"
            }
        }