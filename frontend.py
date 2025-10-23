import streamlit as st 
st.set_page_config(page_title="LearnAuth", page_icon = "Ace.png", layout = "centered")
st.title("LearnAuth") 
st.info("LearnAuth takes Youtube link and gives the learning index of the video")
st.subheader("Enter the Video Details:")
st.text_input("Enter the Youtube link video", placeholder = "https://www.youtube.com/watch?........")
analyse_button = st.button("Analyse Video")
st.header("Analysis Details")
if analyse_button:
    with st.spinner("Processing...... Pls wait a moment........"):
        st.subheader("Learning Index Score:") 
        st.progress(0.90) 
        col1, col2 = st.columns(2) 
        with col1:
            st.metric(label = "Classification", value = "Highly Educational")
        with col2:
            st.metric(label = "Score", value = "90 / 100") 
        st.subheader("Explanation")
        st.write("The video was very educational which involves a deep understanding of concepts taught with examples and with low promotional content") 