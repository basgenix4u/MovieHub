from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text
from sqlalchemy.orm import relationship
from core.database import Base

# Association table for Many-to-Many relationship between Users and Movies (Favorites)
favorites = Table(
    'favorites',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('movie_id', Integer, primary_key=True)
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
    favorite_movies = relationship("Movie", secondary=favorites, back_populates="favorited_by")

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True) # TMDB Movie ID
    title = Column(String)
    overview = Column(Text)
    poster_path = Column(String)
    backdrop_path = Column(String)
    release_date = Column(String)
    vote_average = Column(String)
    source_url = Column(String) # Store the Thenkiri/Source URL
    
    favorited_by = relationship("User", secondary=favorites, back_populates="favorite_movies")
