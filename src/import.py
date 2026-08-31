from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import sqlite3
import requests
from src.Database import connect_db, create_table, save_movies, get_all_movies


app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/save-movie")
async def save_movie_route(movie: dict):
    tmdb_id = movie.get("id")
    title = movie.get("title")
    poster_url = movie.get("poster_path")

    if not tmdb_id or not title:
        raise HTTPException(status_code=400, detail="Missing movie data")

    poster_full_url = f"https://image.tmdb.org/t/p/w500{poster_url}" if poster_url else ""

    save_movies(tmdb_id, title, poster_full_url)
    return {"message": "Movie saved"}

@app.get('/movies')
async def get_movies_route():
    movies = get_all_movies()
    return {"movies": movies}