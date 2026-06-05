from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from models.models import User, Movie
from sqlalchemy import String

router = APIRouter(prefix="/favorites", tags=["Favorites"])

@router.post("/{movie_id}")
async def add_to_favorites(movie_id: int, user_id: str, db: Session = Depends(get_db)):
    # Updated to accept user_id as string (UUID from Supabase)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        # Create a dummy user if not exists for the demo
        # Note: In a real app, User.id would be a String/UUID column in the DB
        user = User(id=user_id, username=f"user_{user_id[:8]}", email=f"{user_id[:8]}@example.com")
        db.add(user)
        db.commit()
        db.refresh(user)
    
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        movie = Movie(id=movie_id, title="Unknown Movie")
        db.add(movie)
        db.commit()
    
    if movie not in user.favorite_movies:
        user.favorite_movies.append(movie)
        db.commit()
    
    return {"message": "Added to favorites"}

@router.get("/{user_id}")
async def get_favorites(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return []
    return user.favorite_movies
