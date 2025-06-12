from model.movie import Movie as MovieModel

class MovieService():
    def __init__(self, db_session):
        self.db = db_session

    def get_movies(self):
        return self.db.query(MovieModel).all()

    def get_movie_by_id(self, movie_id: int):
        return self.db.query(MovieModel).filter(MovieModel.id == movie_id).first()

    def get_movies_by_category(self, category: str):
        return self.db.query(MovieModel).filter(MovieModel.category == category).all()

    def create_movie(self, movie_data: dict):
        new_movie = MovieModel(**movie_data)
        self.db.add(new_movie)
        self.db.commit()
        return new_movie

    def update_movie(self, movie_id: int, movie_data: dict):
        movie = self.get_movie_by_id(movie_id)
        if not movie:
            return None
        for key, value in movie_data.items():
            setattr(movie, key, value)
        self.db.commit()
        return movie

    def delete_movie(self, movie_id: int):
        movie = self.get_movie_by_id(movie_id)
        if not movie:
            return None
        self.db.delete(movie)
        self.db.commit()
        return True