"""Streamlit AI Plagiarism Detector Application"""
import streamlit as st
import requests
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from io import BytesIO
import base64

# Page Configuration
st.set_page_config(
    page_title="AI Plagiarism Detector",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session State Initialization
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []
if 'current_report' not in st.session_state:
    st.session_state.current_report = None
if 'backend_url' not in st.session_state:
    st.session_state.backend_url = "http://localhost:5000"

# Custom CSS Styling
st.markdown("""
    <style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .warning-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .success-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.title("🔍 AI Plagiarism Detector")
    st.markdown("---")
    st.markdown("### How to Use")
    st.info("1. Upload a document (PDF, DOCX, TXT)\n2. Enter comparison text\n3. Click Analyze\n4. View detailed results")
    st.markdown("---")
    
    backend_url = st.text_input(
        "Backend URL",
        value=st.session_state.backend_url,
        help="Enter the backend server URL"
    )
    st.session_state.backend_url = backend_url

# Main Header
st.markdown("""
    <div class="metric-card">
        <h1>🎓 AI Plagiarism & Content Detector</h1>
        <p>Detect plagiarism and AI-generated content with advanced algorithms</p>
    </div>
""", unsafe_allow_html=True)

# Main Content Area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📤 Upload Document")
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "docx", "txt"],
        help="Upload PDF, DOCX, or TXT files"
    )

with col2:
    st.subheader("📝 Comparison Text")
    comparison_text = st.text_area(
        "Enter original text to compare",
        height=150,
        placeholder="Paste the original text here..."
    )

# Analysis Button and Results
if st.button("🔍 Analyze Document", use_container_width=True):
    if uploaded_file and comparison_text:
        with st.spinner("Analyzing... Please wait..."):
            try:
                files = {'file': uploaded_file}
                data = {'comparison_text': comparison_text}
                
                response = requests.post(
                    f"{st.session_state.backend_url}/api/analyze",
                    files=files,
                    data=data,
                    timeout=30
                )
                
                if response.status_code == 200:
                    report = response.json()
                    st.session_state.current_report = report
                    st.session_state.analysis_history.append({
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'file': uploaded_file.name,
                        'report': report
                    })
                    st.success("✅ Analysis complete!")
                else:
                    st.error(f"❌ Error: {response.text}")
            except Exception as e:
                st.error(f"❌ Connection error: {str(e)}")
    else:
        st.warning("⚠️ Please upload a file and enter comparison text")

# Display Results
if st.session_state.current_report:
    report = st.session_state.current_report
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Results", "📈 Metrics", "📋 Details", "📥 Download"])
    
    with tab1:
        st.subheader("Analysis Results")
        
        # Display Plagiarism Detection
        if 'plagiarism_analysis' in report:
            plag = report['plagiarism_analysis']
            col1, col2, col3 = st.columns(3)
            
            with col1:
                severity = plag.get('severity', 'unknown')
                st.metric("Severity", severity.upper())
            
            with col2:
                similarity = plag.get('overall_similarity', 0)
                st.metric("Overall Similarity", f"{similarity}%")
            
            with col3:
                is_plagiarized = "🚨 Yes" if plag.get('is_plagiarized') else "✅ No"
                st.metric("Plagiarized", is_plagiarized)
        
        # Display AI Detection
        if 'ai_analysis' in report:
            ai = report['ai_analysis']
            st.markdown("""<div class="warning-card">
                <h3>🤖 AI-Generated Content Detection</h3>
            </div>""", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("AI Probability", f"{ai.get('ai_probability', 0)}%")
            with col2:
                st.metric("Confidence", ai.get('confidence_level', 'N/A'))
            with col3:
                st.metric("Classification", ai.get('classification', 'N/A'))
    
    with tab2:
        st.subheader("Similarity Metrics")
        
        if 'plagiarism_analysis' in report:
            plag = report['plagiarism_analysis']
            metrics = {
                'Overall': plag.get('overall_similarity', 0),
                'Cosine': plag.get('cosine_similarity', 0),
                'Jaccard': plag.get('jaccard_similarity', 0),
                'Sequence': plag.get('sequence_similarity', 0),
                'N-gram': plag.get('ngram_similarity', 0)
            }
            
            df = pd.DataFrame(list(metrics.items()), columns=['Metric', 'Similarity (%)'])
            fig = px.bar(df, x='Metric', y='Similarity (%)',
                        color='Similarity (%)',
                        color_continuous_scale=['#4caf50', '#ff9800', '#f44336'],
                        text='Similarity (%)')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Detailed Analysis")
        st.json(report)
    
    with tab4:
        st.subheader("Download Results")
        
        # Download as JSON
        json_str = json.dumps(report, indent=2)
        st.download_button(
            label="📥 Download as JSON",
            data=json_str,
            file_name="analysis_report.json",
            mime="application/json"
        )
        
        # Download as CSV
        if 'plagiarism_analysis' in report:
            plag = report['plagiarism_analysis']
            csv_data = pd.DataFrame([plag]).to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv_data,
                file_name="analysis_report.csv",
                mime="text/csv"
            )

# Display Analysis History
if st.session_state.analysis_history:
    with st.expander("📜 Analysis History"):
        for i, item in enumerate(st.session_state.analysis_history, 1):
            st.write(f"{i}. **{item['file']}** - {item['timestamp']}")

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>© 2024 AI Plagiarism Detector | Powered by Streamlit</p>", unsafe_allow_html=True)
