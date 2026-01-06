"""Plagiarism Detection Backend - Core Detection Logic"""
import math
import re
from collections import Counter
from difflib import SequenceMatcher

class DocumentParser:
    """Parse and extract text from documents"""
    @staticmethod
    def parse_text(text):
        return text.strip()

class TextPreprocessor:
    """Clean and preprocess text"""
    @staticmethod
    def clean_text(text):
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s.,!?;:\'-]', '', text)
        return text.strip()
    
    @staticmethod
    def tokenize(text):
        return re.findall(r'\b\w+\b', text.lower())
    
    @staticmethod
    def get_sentences(text):
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    @staticmethod
    def get_ngrams(tokens, n=3):
        return [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

class PlagiarismDetector:
    """Core plagiarism detection algorithms"""
    
    @staticmethod
    def cosine_similarity(text1, text2):
        tokens1 = TextPreprocessor.tokenize(text1)
        tokens2 = TextPreprocessor.tokenize(text2)
        
        vocab = set(tokens1 + tokens2)
        vec1 = [tokens1.count(word) for word in vocab]
        vec2 = [tokens2.count(word) for word in vocab]
        
        dot_product = sum(a*b for a, b in zip(vec1, vec2))
        mag1 = math.sqrt(sum(a*a for a in vec1))
        mag2 = math.sqrt(sum(b*b for b in vec2))
        
        if mag1 == 0 or mag2 == 0:
            return 0.0
        return dot_product / (mag1 * mag2)
    
    @staticmethod
    def jaccard_similarity(text1, text2):
        tokens1 = set(TextPreprocessor.tokenize(text1))
        tokens2 = set(TextPreprocessor.tokenize(text2))
        
        intersection = tokens1.intersection(tokens2)
        union = tokens1.union(tokens2)
        
        if len(union) == 0:
            return 0.0
        return len(intersection) / len(union)
    
    @staticmethod
    def sequence_similarity(text1, text2):
        return SequenceMatcher(None, text1, text2).ratio()
    
    @staticmethod
    def ngram_similarity(text1, text2, n=3):
        tokens1 = TextPreprocessor.tokenize(text1)
        tokens2 = TextPreprocessor.tokenize(text2)
        
        ngrams1 = set(TextPreprocessor.get_ngrams(tokens1, n))
        ngrams2 = set(TextPreprocessor.get_ngrams(tokens2, n))
        
        if len(ngrams1) == 0:
            return 0.0
        overlap = len(ngrams1.intersection(ngrams2))
        return overlap / len(ngrams1)
    
    @staticmethod
    def detect_plagiarism(original_text, submitted_text):
        """Comprehensive plagiarism detection"""
        cosine = PlagiarismDetector.cosine_similarity(original_text, submitted_text)
        jaccard = PlagiarismDetector.jaccard_similarity(original_text, submitted_text)
        sequence = PlagiarismDetector.sequence_similarity(original_text, submitted_text)
        ngram = PlagiarismDetector.ngram_similarity(original_text, submitted_text)
        
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

class AIContentDetector:
    """Detect AI-generated content"""
    
    @staticmethod
    def calculate_perplexity_score(text):
        sentences = TextPreprocessor.get_sentences(text)
        if not sentences:
            return 0.0
        
        word_counts = [len(TextPreprocessor.tokenize(s)) for s in sentences]
        if not word_counts:
            return 0.0
        
        avg = sum(word_counts) / len(word_counts)
        variance = sum((x - avg) ** 2 for x in word_counts) / len(word_counts)
        return variance ** 0.5
    
    @staticmethod
    def calculate_burstiness(text):
        sentences = TextPreprocessor.get_sentences(text)
        if len(sentences) < 2:
            return 0.0
        
        complexities = []
        for sentence in sentences:
            tokens = TextPreprocessor.tokenize(sentence)
            if tokens:
                unique_ratio = len(set(tokens)) / len(tokens)
                complexities.append(unique_ratio)
        
        if not complexities:
            return 0.0
        avg_complexity = sum(complexities) / len(complexities)
        return avg_complexity
    
    @staticmethod
    def detect_ai_content(text):
        """Detect AI-generated content"""
        perplexity = AIContentDetector.calculate_perplexity_score(text)
        burstiness = AIContentDetector.calculate_burstiness(text)
        
        # Scale to 0-100
        ai_probability = min(100, max(0, (perplexity * 20 + burstiness * 30)))
        
        return {
            'ai_probability': round(ai_probability, 1),
            'perplexity_score': round(perplexity, 2),
            'burstiness_score': round(burstiness, 2),
            'confidence_level': 'High' if ai_probability > 70 else 'Medium' if ai_probability > 40 else 'Low',
            'classification': 'AI-Generated' if ai_probability > 60 else 'Human-Written'
        }

def analyze_text(submitted_text, comparison_text=""):
    """Main analysis function"""
    try:
        if not comparison_text:
            comparison_text = submitted_text
        
        plagiarism_result = PlagiarismDetector.detect_plagiarism(comparison_text, submitted_text)
        ai_result = AIContentDetector.detect_ai_content(submitted_text)
        
        return {
            'success': True,
            'plagiarism_analysis': plagiarism_result,
            'ai_analysis': ai_result,
            'timestamp': pd.Timestamp.now().isoformat() if 'pd' in dir() else str(__import__('datetime').datetime.now().isoformat())
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
