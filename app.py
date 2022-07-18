#Importing libraries----------------------------------------------------------------------------------------------------
from urllib import response
import streamlit as st
import pandas as pd
import pickle
import requests
from itertools import cycle
from PIL import Image
from io import BytesIO

#Functions--------------------------------------------------------------------------------------------------------------
@st.cache()
def load_movies():
    url = 'https://drive.google.com/file/d/12-2w5tB7cS7ZgXAF_yAMFrKe2n6xHHbl/view?usp=sharing'
    path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
    df = pd.read_csv(path, usecols=['original_title'])
    return df

@st.cache()
def load_data():
    url = 'https://drive.google.com/file/d/12-2w5tB7cS7ZgXAF_yAMFrKe2n6xHHbl/view?usp=sharing'
    path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
    df = pd.read_csv(path)
    return df


@st.cache
def load_embeddings():
    url2 = 'https://drive.google.com/file/d/1Rp3Ay3oyQzEj1IUwZm0kTD8AmbjMCvwA/view?usp=sharing'
    path2 = 'https://drive.google.com/uc?export=download&id='+url2.split('/')[-2]
    df2 = pd.read_csv(path2, compression='gzip')
    return df2


def fetch_poster(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=a984a10e30d9db72dac2c18a4b9f79f3")
    data = response.json()
    return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"


def recommender(movies, top_n):
  movies_index = movies_data[movies_data['original_title']==movies].index[0]
  distances = similarity[movies_index]
  movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:top_n]
  recommeded_movie = []
  recommended_poster = []
  for i in movies_list:
    movie_id = movies_data.iloc[i[0]].id
    recommeded_movie.append(movies_data.iloc[i[0]].original_title)
    recommended_poster.append(fetch_poster(movie_id))
  return recommeded_movie, recommended_poster

#Loading data-----------------------------------------------------------------------------------------------------------
movies_name = load_movies()
movies_data = load_data()
similarity = load_embeddings().values

#Page Layout------------------------------------------------------------------------------------------------------------
st.title('Movie Recommender System')
selected_movie = st.selectbox('Please select your favourite movie:',movies_name)
top_n = st.number_input('Number of recommendation to be extracted:',10,50)

if st.button('Recommend'):
    st.write('''---''')
    st.subheader('Recommended Movies:')
    recommendation, posters = recommender(selected_movie, top_n=top_n+1)

    cols = cycle(st.columns(4))
    
    for i,j in zip(recommendation, posters):
        cc = next(cols)
        r = requests.get(j)
        img = Image.open(BytesIO(r.content))
        resizedImg = img.resize((250, 325), Image.ANTIALIAS)
        cc.image(resizedImg, caption=i)
#------------------------------------------------------------------------------------------------------------------------
    

