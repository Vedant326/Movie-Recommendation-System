import streamlit as st
import pickle
import pandas as pd
import requests

# Fetching posters
def fetching_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=eab4681e65474567445fffb6eef8f5a1')
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']

# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]  # distances using similarity above
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_list = []
    recommended_movie_list = []

    for i in movie_list:
        # For fetching posters
        movie_id = movies.iloc[i[0]].movie_id
        recommended_list.append(movies.iloc[i[0]].title) 

        # Fetching poster from API key (TMDB)
        recommended_movie_list.append(fetching_poster(movie_id))

    return recommended_list, recommended_movie_list

# Load data
try:
    movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('recommend.pkl', 'rb'))
    st.write("Data loaded successfully.")
except Exception as e:
    st.error(f"Error loading data: {e}")

# Streamlit UI
st.title('Movie Recommendation System')

# Select box
select_movie_name = st.selectbox(
    "Select the movies",
    movies['title'].values
)

# Recommend movies
if st.button("Recommend"):
    try:
        names, posters = recommend(select_movie_name)
        
        # Check if we actually have 5 names and posters
        if len(names) == 5 and len(posters) == 5:
            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.text(names[0])
                st.image(posters[0])
            with col2:
                st.text(names[1])
                st.image(posters[1])
            with col3:
                st.text(names[2])
                st.image(posters[2])
            with col4:
                st.text(names[3])
                st.image(posters[3])
            with col5:
                st.text(names[4])
                st.image(posters[4])
        else:
            st.error("There was an issue with the recommendations. Please try again.")
    except Exception as e:
        st.error(f"An error occurred during recommendation: {e}")
