"""AI Plagiarism & AI Content Detector - Streamlit App"""
import streamlit as st
import re
import math
from collections import Counter
from difflib import SequenceMatcher
from datetime import datetime

# ============== PLAGIARISM DETECTION FUNCTIONS ==============

def tokenize_text(text):
    """Tokenize text into words"""
    return re.findall(r'\b\w+\b', text.lower())

def get_sentences(text):
    """Split text into sentences"""
    sentences = re.split(r'[.!?]+', text)
    return [s.strip() for s in sentences if s.strip()]

def get_ngrams(tokens, n=3):
    """Generate n-grams from tokens"""
    return [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

def cosine_similarity(text1, text2):
    """Calculate cosine similarity"""
    tokens1 = tokenize_text(text1)
    tokens2 = tokenize_text(text2)
    
    vocab = set(tokens1 + tokens2)
    vec1 = [tokens1.count(word) for word in vocab]
    vec2 = [tokens2.count(word) for word in vocab]
    
    dot_product = sum(a*b for a, b in zip(vec1, vec2))
    mag1 = math.sqrt(sum(a*a for a in vec1))
    mag2 = math.sqrt(sum(b*b for b in vec2))
    
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot_product / (mag1 * mag2)

def jaccard_similarity(text1, text2):
    """Calculate Jaccard similarity"""
    tokens1 = set(tokenize_text(text1))
    tokens2 = set(tokenize_text(text2))
    
    intersection = tokens1.intersection(tokens2)
    union = tokens1.union(tokens2)
    
    if len(union) == 0:
        return 0.0
    return len(intersection) / len(union)

def sequence_similarity(text1, text2):
    """Calculate sequence similarity"""
    return SequenceMatcher(None, text1, text2).ratio()

def ngram_similarity(text1, text2, n=3):
    """Calculate n-gram similarity"""
    tokens1 = tokenize_text(text1)
    tokens2 = tokenize_text(text2)
    
    ngrams1 = set(get_ngrams(tokens1, n))
    ngrams2 = set(get_ngrams(tokens2, n))
    
    if len(ngrams1) == 0:
        return 0.0
    overlap = len(ngrams1.intersection(ngrams2))
    return overlap / len(ngrams1)

def detect_plagiarism(original_text, submitted_text):
    """Detect plagiarism with multiple algorithms"""
    cosine = cosine_similarity(original_text, submitted_text)
    jaccard = jaccard_similarity(original_text, submitted_text)
    sequence = sequence_similarity(original_text, submitted_text)
    ngram = ngram_similarity(original_text, submitted_text)
    
    overall = (cosine * 0.3 + jaccard * 0.2 + sequence * 0.3 + ngram * 0.2) * 100
    
    return {
        'overall_similarity': round(overall, 2),
        'cosine_similarity': round(cosine * 100, 2),
        'jaccard_similarity': round(jaccard * 100, 2),
        'sequence_similarity': round(sequence * 100, 2),
        'ngram_similarity': round(ngram * 100, 2),
        'is_plagiarized': overall > 50,
        'severity': 'critical' if overall > 75 else 'high' if overall > 60 else 'moderate' if overall > 40 else 'low'
    }

def detect_ai_content(text):
    """Detect AI-generated content"""
    sentences = get_sentences(text)
    if len(sentences) < 2:
        ai_prob = 25.0
    else:
        word_counts = [len(tokenize_text(s)) for s in sentences]
        avg = sum(word_counts) / len(word_counts) if word_counts else 0
        variance = sum((x - avg) ** 2 for x in word_counts) / len(word_counts) if word_counts else 0
        perplexity = variance ** 0.5 if variance > 0 else 0
        
        complexities = []
        for sentence in sentences:
            tokens = tokenize_text(sentence)
            if tokens:
                unique_ratio = len(set(tokens)) / len(tokens)
                complexities.append(unique_ratio)
        
        burstiness = sum(complexities) / len(complexities) if complexities else 0
        ai_prob = min(100, max(0, (perplexity * 15 + burstiness * 35)))
    
    return {
        'ai_probability': round(ai_prob, 1),
        'confidence_level': 'High' if ai_prob > 70 else 'Medium' if ai_prob > 40 else 'Low',
        'classification': 'AI-Generated' if ai_prob > 60 else 'Human-Written'
    }

# ============== STREAMLIT APP ==============

st.set_page_config(
    page_title="AI Plagiarism Detector",
    page_icon="🔍",
    layout="wide"
)

st.markdown("""
<style>
.main { padding: 2rem; }
.header-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}
.metric-box {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1.5rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-card">
    <h1>🎓 AI Plagiarism & Content Detector</h1>
    <p>Detect plagiarism and AI-generated content with advanced algorithms</p>
</div>
""", unsafe_allow_html=True)

# Input section
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Your Content")
    submitted_text = st.text_area(
        "Paste text to analyze",
        height=200,
        placeholder="Enter the text you want to check for plagiarism and AI content..."
    )

with col2:
    st.subheader("📚 Source/Comparison")
    comparison_text = st.text_area(
        "Paste source/original text (optional)",
        height=200,
        placeholder="Enter source text to compare against..."
    )

# Analysis button
if st.button("🔍 Analyze Now", use_container_width=True):
    if not submitted_text:
        st.error("Please enter text to analyze")
    else:
        with st.spinner("Analyzing..."):
            compare_text = comparison_text if comparison_text else submitted_text
            
            # Run analysis
            plag_results = detect_plagiarism(compare_text, submitted_text)
            ai_results = detect_ai_content(submitted_text)
            
            # Display results in tabs
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Results", "📈 Metrics", "💭 Suggestions", "📥 Download"])
            
            with tab1:
                st.subheader("Analysis Results")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Plagiarism Severity", plag_results['severity'].upper())
                with col2:
                    st.metric("Similarity %", f"{plag_results['overall_similarity']}%")
                with col3:
                    status = "🚨 PLAGIARIZED" if plag_results['is_plagiarized'] else "✅ ORIGINAL"
                    st.markdown(f"<div class='metric-box'>{status}</div>", unsafe_allow_html=True)
                
                st.markdown("---")
                st.subheader("🤖 AI Content Detection")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("AI Probability", f"{ai_results['ai_probability']}%")
                with col2:
                    st.metric("Confidence", ai_results['confidence_level'])
                with col3:
                    st.metric("Classification", ai_results['classification'])
            
            with tab2:
                st.subheader("Similarity Metrics")
                st.write(f"**Cosine Similarity:** {plag_results['cosine_similarity']}%")
                st.write(f"**Jaccard Similarity:** {plag_results['jaccard_similarity']}%")
                st.write(f"**Sequence Similarity:** {plag_results['sequence_similarity']}%")
                st.write(f"**N-gram Similarity:** {plag_results['ngram_similarity']}%")
            
            with tab3:
                st.subheader("💡 Improvement Suggestions")
                if plag_results['overall_similarity'] > 50:
                    st.warning("⚠️ High plagiarism detected. Consider rewriting the content.")
                if ai_results['ai_probability'] > 60:
                    st.info("🤖 AI-generated content detected. Add more personal insights.")
                st.markdown("""
                **Best Practices:**
                1. Use original content and write in your own words
                2. Cite sources properly with quotation marks
                3. Paraphrase and add your own analysis
                4. If using AI, disclose and add human perspective
                5. Review and proofread before submission
                """)
            
            with tab4:
                st.subheader("📥 Download Results")
                import json
                results = {
                    'timestamp': datetime.now().isoformat(),
                    'plagiarism': plag_results,
                    'ai_detection': ai_results
                }
                json_str = json.dumps(results, indent=2)
                st.download_button(
                    "Download JSON Report",
                    data=json_str,
                    file_name=f"plagiarism_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>© 2024 AI Plagiarism Detector | Powered by Streamlit</p>", unsafe_allow_html=True)
