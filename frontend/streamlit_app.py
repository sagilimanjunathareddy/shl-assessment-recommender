import streamlit as st
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from retrieval.retriever import retrieve


st.set_page_config(
    page_title="SHL Assessment Recommender",
    page_icon="🔍",
    layout="wide"
)


st.markdown("""
<style>
.main-title {
    font-size: 40px;
    font-weight: 700;
    color: #1f4e79;
}
.subtitle {
    font-size: 18px;
    color: #555;
}
.result-card {
    padding: 20px;
    border-radius: 12px;
    background-color: #f9f9f9;
    margin-bottom: 15px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🔍 SHL Assessment Recommendation Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">GenAI-powered RAG system for intelligent SHL assessment recommendations</div>', unsafe_allow_html=True)
st.divider()


st.sidebar.title("📌 About")
st.sidebar.write("""
This system uses:

- SentenceTransformers embeddings  
- FAISS vector search  
- CrossEncoder neural reranking  
- Hybrid keyword boosting  

Built using a two-stage RAG architecture.
""")

st.sidebar.markdown("### 📊 Model Performance")
st.sidebar.write("Mean Recall@10 ≈ 0.30")

query = st.text_area(
    "Enter Job Requirement",
    placeholder="Example: Looking to hire a Java developer with collaboration and analytical reasoning skills..."
)

col1, col2 = st.columns([1,1])

with col1:
    top_k = st.slider("Number of Recommendations", 5, 15, 10)

with col2:
    search_button = st.button("🚀 Generate Recommendations")


if search_button:

    if not query.strip():
        st.warning("Please enter a job requirement.")
    else:
        with st.spinner("Analyzing and retrieving best assessments..."):
            results = retrieve(query, top_k=top_k)

        st.success(f"Top {len(results)} Recommended Assessments")

        for i, item in enumerate(results, 1):

            st.markdown(f"""
            <div class="result-card">
                <h3>{i}. {item['name']}</h3>
                <p>{item['description']}</p>
                <p><b>Duration:</b> {item.get('duration', 'N/A')} minutes</p>
                <p><b>Test Type:</b> {', '.join(item.get('test_type', []))}</p>
                <a href="{item['url']}" target="_blank">🔗 View Assessment</a>
            </div>
            """, unsafe_allow_html=True)