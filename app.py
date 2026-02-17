import streamlit as st
import requests
import random
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

st.set_page_config(page_title="Smart Movie Recommender", layout="wide")

st.markdown("""
<style>
.stApp {background-color: #0F172A;}
.title {text-align:center; font-size:40px; color:#22C55E; font-weight:bold;}
.movie-title {color:white; font-size:14px; font-weight:bold;}
.rating {color:#FACC15; font-size:13px;}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🎬 Smart Movie Recommendation System</div>", unsafe_allow_html=True)

# 🎬 Updated Categories
category_dict = {

    # 🔥 Bollywood
    "🔥 Bollywood Action": {"with_genres": "28", "with_original_language": "hi"},
    "😂 Bollywood Comedy": {"with_genres": "35", "with_original_language": "hi"},
    "❤️ Bollywood Love": {"with_genres": "10749", "with_original_language": "hi"},
    "👻 Bollywood Horror": {"with_genres": "27", "with_original_language": "hi"},
    "🎭 Bollywood Drama": {"with_genres": "18", "with_original_language": "hi"},

    # 🌍 Hollywood
    "💣 Hollywood Action": {"with_genres": "28", "with_original_language": "en"},
    "🤣 Hollywood Comedy": {"with_genres": "35", "with_original_language": "en"},
    "💕 Hollywood Love": {"with_genres": "10749", "with_original_language": "en"},
    "🧟 Hollywood Horror": {"with_genres": "27", "with_original_language": "en"},

    # 🎭 Mood Based
    "😊 Feel Good": {"with_genres": "35,10749"},
    "😢 Emotional": {"with_genres": "18"},
    "🤯 Thriller Mood": {"with_genres": "53"},
    "🚀 Sci-Fi": {"with_genres": "878"},
    "🎬 Cartoon / Animation": {"with_genres": "16"},
}

def get_movies(params):
    url = "https://api.themoviedb.org/3/discover/movie"

    params.update({
        "api_key": API_KEY,
        "sort_by": "popularity.desc",
        "vote_count.gte": 200
    })

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        movies = data.get("results", [])
        random.shuffle(movies)
        return movies[:10]
    except:
        st.error("API Error - Check API Key or Internet")
        return []

def search_movie(query):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {"api_key": API_KEY, "query": query}
    response = requests.get(url, params=params)
    data = response.json()
    return data.get("results", [])

if "movies" not in st.session_state:
    st.session_state.movies = []

if "favorites" not in st.session_state:
    st.session_state.favorites = []

st.subheader("🔍 Search Movie")
search_query = st.text_input("Enter movie name")

if st.button("Search Movie"):
    if search_query:
        results = search_movie(search_query)
        cols = st.columns(5)
        for index, movie in enumerate(results[:10]):
            with cols[index % 5]:
                poster = movie.get("poster_path")
                title = movie.get("title")
                rating = movie.get("vote_average")
                movie_id = movie.get("id")
                if poster:
                    st.image(f"https://image.tmdb.org/t/p/w300{poster}", use_container_width=True)
                st.markdown(f"<div class='movie-title'>{title}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='rating'>⭐ {rating}</div>", unsafe_allow_html=True)
                trailer_url = f"https://www.youtube.com/results?search_query={title}+trailer"
                st.markdown(f"[▶ Watch Trailer]({trailer_url})")
                if st.button("❤️ Add", key=f"search{movie_id}"):
                    if title not in st.session_state.favorites:
                        st.session_state.favorites.append(title)

st.divider()

choice = st.selectbox("Select Category:", list(category_dict.keys()))

if st.button("🚀 Generate 10 Movies"):
    st.session_state.movies = get_movies(category_dict[choice])

movies = st.session_state.movies

if movies:
    cols = st.columns(5)
    for index, movie in enumerate(movies):
        with cols[index % 5]:
            poster = movie.get("poster_path")
            title = movie.get("title")
            rating = movie.get("vote_average")
            movie_id = movie.get("id")
            if poster:
                st.image(f"https://image.tmdb.org/t/p/w300{poster}", use_container_width=True)
            st.markdown(f"<div class='movie-title'>{title}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='rating'>⭐ {rating}</div>", unsafe_allow_html=True)
            trailer_url = f"https://www.youtube.com/results?search_query={title}+trailer"
            st.markdown(f"[▶ Watch Trailer]({trailer_url})")
            if st.button("❤️ Add", key=f"cat{movie_id}"):
                if title not in st.session_state.favorites:
                    st.session_state.favorites.append(title)

st.divider()
st.subheader("❤️ Your Favorites")

if st.session_state.favorites:
    for fav in st.session_state.favorites:
        st.write("•", fav)
else:
    st.write("No favorites added yet.")
