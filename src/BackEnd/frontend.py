import streamlit as st
from learn_auth_engine import recommend_videos

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
            st.session_state.language = st.selectbox("", ["English", "Hindi"], key = "language_select")
        col3, col4 = st.columns([4, 5])
        with col3:
            st.markdown("**Choose your mode of learning:**")
        with col4:
            st.session_state.mode = st.selectbox("", ["Practical", "Theoretical with notes", "A mix of both"], key = "mode_select")
        col5, col6 = st.columns([3, 4])
        with col5:
            st.markdown("**Your current knowledge level:**")
        with col6:
            st.session_state.knowledge_level = st.selectbox("", ["Beginner", "Intermediate", "Advanced"], key = "knowledge")    
        col7, col8 = st.columns([2, 4])
        with col7:
            st.markdown("**Learning Goal:**")
        with col8:
            st.session_state.learning = st.selectbox("", ["Exam Preparation", "Concept Understanding", "Project Building", "Interview Preparation"], key = "learning_goal")   
        col9, col10 = st.columns([2, 6])
        with col9:
            st.markdown("**Ideal video length:**")
        with col10:
            st.session_state.video = st.selectbox("", ["less then 20 minutes","less then 1 Hour", ], key = "video_length")
        if st.button("Apply", type = "primary"):
            st.session_state.selected_filters = [st.session_state.language, st.session_state.mode, st.session_state.knowledge_level, st.session_state.learning, st.session_state.video]   
# LEFT SIDE 
with left_col:
    st.title("LearnAuth")
    st.info("LearnAuth takes YouTube link and gives the learning index of the video")

    st.subheader("Enter the Video Details:")
    video_url = st.text_input(
        "Enter the YouTube video link",
        placeholder="https://www.youtube.com/watch?........"
    )

    col1, col2 = st.columns([2, 10])
    with col1:
        analyse_button_left = st.button("Analyse Video")
    with col2: 
        popup()

    st.header("Analysis Details")

    if analyse_button_left and video_url:
        with st.spinner("Processing... Please wait..."):

            try:
                from learn_auth_engine import (
                    get_transcript_with_pytube,
                    analyze_transcript_with_gemini
                )

                # 1. Extract transcript
                transcript = get_transcript_with_pytube(video_url)

                # 2. Analyze using Gemini
                result = analyze_transcript_with_gemini(transcript)

                # 3. Convert rating (1–10 → 0–100)
                overall_score = int(result["overall_rating"]) * 10

                # 4. Classification logic
                if overall_score >= 80:
                    classification = "Highly Educational"
                elif overall_score >= 50:
                    classification = "Moderately Educational"
                else:
                    classification = "Low Educational Value"

                # 5. Display Results
                st.subheader("Learning Index Score:")

                # Correct dynamic progress bar (0–100)
                progress_bar = st.progress(0)
                progress_bar.progress(overall_score)

                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label="Classification", value=classification)
                with col2:
                    st.metric(label="Score", value=f"{overall_score} / 100")

                st.subheader("Explanation")
                st.write(result.get("summary", "No summary available."))

            except Exception as e:
                st.error(f"Error occurred: {str(e)}")
# RIGHT SIDE  WORKING BACKEND SEARCH + OUTPUT
with right_col:
    st.subheader("Search for recommended videos by Topic")
    topic = st.text_input( "Enter the Youtube topic",
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
                # Save dataframe in session so it persists across reruns
                st.session_state.ranked_df = ranked_df
    # DISPLAY RESULTS    
    if "ranked_df" in st.session_state:
        ranked_df = st.session_state.ranked_df
        st.markdown("### Recommended Videos")
        for idx, row in ranked_df.iterrows():
            col1, col2 = st.columns([1, 6])
            with col1:
                st.markdown(f"**{row['Rank']}**")
            with col2:
                if st.button(row["Video Title"], key=f"video_{idx}"):
                    st.session_state.selected_video = idx 
        # OPEN DIALOG IF VIDEO SELECTED
        if "selected_video" in st.session_state:
            video_details = ranked_df.iloc[st.session_state.selected_video]
            @st.dialog("Video Details")
            def show_details():
                st.markdown(f"### {video_details['Video Title']}")
                st.markdown(f"**Channel:** {video_details['Channel']}")
                st.markdown(f"**Link:** {video_details['Link']}")
                st.markdown("---")
                st.markdown("### Scoring Metrics")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Clarity", video_details["clarity"])
                    st.metric("Engagement", video_details["engagement"])
                with col2:
                    st.metric("Concept Depth", video_details["concept_depth"])
                    st.metric("Promotion", video_details["promotion"])
                st.markdown("---")
                st.metric("Personal Score", video_details["personal_score"])
                if "summary" in video_details:
                    st.markdown("### Summary")
                    st.write(video_details["summary"])
                if st.button("Close"):
                    del st.session_state.selected_video
            show_details()