from flask import Flask, render_template, redirect, url_for 
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import os
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)


api_key = os.getenv("API_KEY")
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movie.db"
Bootstrap5(app)

MOVIE_DB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
MOVIE_DB_INFO_URL = "https://api.themoviedb.org/3/movie"
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

# CREATE DB
class Base(DeclarativeBase):
    pass

# INITIALIZE DB
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(250), nullable=True)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context(): 
    db.create_all()

class addMovies(FlaskForm):
    movie_title = StringField("Movie Title",[DataRequired()])
    add = SubmitField("Add Movie")
    
class updateMovies(FlaskForm):
    new_rating = StringField("Rating")
    new_review = StringField("Review")
    submit = SubmitField("Done")
    
@app.route("/")
def home():
    results = db.session.execute(db.select(Movie).order_by(Movie.rating))
    all_movies = results.scalars().all()
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()
    return render_template("index.html", movies = all_movies)

@app.route("/update/<int:index>", methods=["GET","POST"])
def update(index):
    form = updateMovies()
    to_update = db.session.execute(db.select(Movie).where(Movie.id == index)).scalar() 
    if form.validate_on_submit():
        updated_rating = form.new_rating.data
        updated_review = form.new_review.data
        
        if updated_rating: 
            to_update.rating = form.new_rating.data

        if updated_review:
            to_update.review = form.new_review.data

        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", form=form, movie=to_update)

@app.route('/delete/<int:index>')
def delete(index):
    to_delete = db.session.execute(db.select(Movie).where(Movie.id == index)).scalar()
    db.session.delete(to_delete)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/add",methods=["GET","POST"])
def add_movies():
    form =  addMovies()
    if form.validate_on_submit():
        movie_title = form.movie_title.data

        response = requests.get(MOVIE_DB_SEARCH_URL, params={"api_key": api_key, "query": movie_title})
        data = response.json()["results"]
        return render_template("select.html", options=data)
    return render_template('add.html', form=form)

@app.route("/find_movie/<int:id>") 
def find_movie(id):
    if id:
        movie_api_url = f"{MOVIE_DB_INFO_URL}/{id}" 
        response = requests.get(movie_api_url, params={"api_key":api_key, "language":"en-US"})
        data = response.json()
        new_movie = Movie(
            title=data["title"],
            year=data["release_date"].split("-")[0],
            img_url=f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}",
            description=data["overview"]
        )
        db.session.add(new_movie)
        db.session.commit()

        return redirect(url_for("update",index=new_movie.id))


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
