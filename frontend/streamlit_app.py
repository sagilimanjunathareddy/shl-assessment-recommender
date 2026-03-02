import streamlit as st
import requests

st.title("SHL Assessment Recommendation")

query = st.text_area("Enter Job Description or Query")

if st.button("Recommend"):
    response = requests.post(
        "http://localhost:8000/recommend",
        json={"query": query}
    )

    data = response.json()

    for item in data["recommended_assessments"]:
        st.subheader(item["name"])
        st.write(item["description"])
        st.write(item["url"])