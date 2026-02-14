import streamlit as st
from learn_auth_engine import recommend_videos
import backend 

st.set_page_config(page_title="LearnAuth",page_icon="Ace.png",layout="wide")
left_col, right_col = st.columns([2, 1])

#PERSONALISATION 
def popup():
    popover = st.popover("Personalised Search")
    with popover:
        col1, col2 = st.columns([5, 3])
        with col1:
            st.markdown("**Choose your preferred language:**")
        with col2:
            st.session_state.language = st.selectbox("", ["English", "Hindi", "Marathi", "Tamil", "Spanish", "German"], key = "language_select")
        col3, col4 = st.columns([4, 5])
        with col3:
            st.markdown("**Choose your mode of learning:**")
        with col4:
            st.session_state.mode = st.selectbox("", ["Practical", "Theoretical with notes", "A mix of both"], key = "mode_select")
        if st.button("Apply", type = "primary"):
            st.session_state.selected_filters = [st.session_state.language, st.session_state.mode]

# LEFT SIDE 
with left_col:
    st.title("LearnAuth")
    st.info("LearnAuth takes Youtube link and gives the learning index of the video")
    st.subheader("Enter the Video Details:")
    st.text_input(
        "Enter the Youtube link video",
        placeholder="https://www.youtube.com/watch?........" )
    analyse_button_left = st.button("Analyse Video")
    st.header("Analysis Details")
    if analyse_button_left:
        with st.spinner("Processing...... Pls wait a moment........"):
            st.subheader("Learning Index Score:")
            st.progress(0.90)
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Classification", value="Highly Educational")
            with col2:
                st.metric(label="Score", value="90 / 100")
            st.subheader("Explanation")
            st.write(
                "The video was very educational which involves a deep understanding "
                "of concepts taught with examples and with low promotional content"
            )

# RIGHT SIDE  WORKING BACKEND SEARCH + OUTPUT
with right_col:
    st.subheader("Search for reccomended videos by Topic")
    topic = st.text_input(
        "Enter the Youtube topic",
        placeholder="Machine Learning, Python, Data Structures...",
        key="right_search")
    analyse_button_right = st.button("Analyse Video", key="right_button")
    if analyse_button_right and topic:
        with st.spinner("Running backend analysis..."):
            ranked_df = recommend_videos(topic)
            if ranked_df is None:
                st.error("No suitable videos found.")
            else:
                st.success("Backend Output Generated")
                st.dataframe(ranked_df, use_container_width=True)
