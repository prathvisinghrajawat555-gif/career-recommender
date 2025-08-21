import streamlit as st
from logic.rules import recommend

st.set_page_config(page_title="Career Recommender", page_icon="🎯", layout="centered")

st.title("Career Recommender 🎯")

skills = st.text_input("Your skills (comma separated)")
interests = st.text_input("Your interests (comma separated)")
style = st.text_input("Your work style (comma separated)")

user_text = st.text_area("Describe yourself", help="Add a short description about your background and goals.")

if st.button("Get Recommendations"):
    profile = {
        'skills': skills,
        'interests': interests,
        'style': style
    }
    results = recommend(user_text, profile)
    if not results:
        st.warning("No strong matches. Try adding more details or keywords.")
    for r in results:
        with st.container():
            st.subheader(f"{r['role']} (score: {r['score']})")
            st.write(r['description'])
            if r['reasons']:
                st.caption("Why this role: " + " • ".join(r['reasons']))
            if r['resources']:
                st.write("Resources:", r['resources'])
            if r.get('roadmap'):
                st.write("Roadmap:", r['roadmap'])
