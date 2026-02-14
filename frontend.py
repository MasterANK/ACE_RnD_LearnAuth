import streamlit as st 
import backend 

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
        
        
st.set_page_config(page_title="LearnAuth", page_icon = "Ace.png", layout = "centered")
st.title("LearnAuth") 
st.info("LearnAuth takes Youtube link and gives the learning index of the video")
st.subheader("Enter the Video Details:")
st.text_input("Enter the Youtube link video", placeholder = "https://www.youtube.com/watch?........")

col1, col2 = st.columns([1, 4])
with col1: 
    analyse_button = st.button("Analyse Video", type = "primary")
with col2: 
    popup()  
    
if analyse_button:
    filters = st.session_state.get("selected_filters", [])
    backend.options(filters)
    
st.header("Analysis Details:")

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