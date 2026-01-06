# AI-Plagiarism-Detector
An AI-powered assignment plagiarism detection system that analyzes documents for plagiarism and AI-generated content. Features detailed reports with highlighted sections, confidence scores, and suggestions for improvement.

## 🌟 Features

- **Advanced Plagiarism Detection**: Multiple similarity algorithms (Cosine, Jaccard, Sequence Matching, N-gram)
- **AI Content Detection**: Identifies AI-generated content with statistical analysis
- **Document Support**: Analyzes PDF, DOCX, and TXT files
- **Beautiful UI**: Responsive Streamlit interface with dark mode
- **Real-time Analysis**: Fast document processing and analysis
- **Detailed Reports**: Downloadable JSON and CSV reports
- **Session History**: Track previous analyses

## 🚀 Quick Start (Local)

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/Arpan-234/AI-Plagiarism-Detector.git
cd AI-Plagiarism-Detector

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 🌐 Deploy to Streamlit Cloud

### Step 1: Push Code to GitHub
Your code is already in the repository.

### Step 2: Create Streamlit Cloud Account
1. Visit https://streamlit.io/cloud
2. Sign in with your GitHub account
3. Click "New app"

### Step 3: Connect Repository
1. Select your GitHub repository: `AI-Plagiarism-Detector`
2. Select branch: `main`
3. Set main file path: `app.py`
4. Click "Deploy"

### Step 4: Configure Backend
Update the `backend_url` in the app to point to your backend server. By default, it uses `http://localhost:5000`.

## 📝 Project Structure

```
AI-Plagiarism-Detector/
├── app.py                 # Streamlit frontend application
├── requirements.txt       # Python dependencies
├── .streamlit/
│   └── config.toml       # Streamlit configuration
├── README.md             # This file
└── LICENSE               # MIT License
```

## 🔧 Configuration

Modify `.streamlit/config.toml` to customize:
- Theme colors
- Page layout
- Server settings
- Browser preferences

## 📚 Available Prompts for Claude

Use these excellent prompts with Claude.ai to extend the project:

1. **Backend Development**: Create Flask/FastAPI backend with document parsing
2. **Frontend Enhancement**: Build React/Vue interface with modern design
3. **Database Setup**: Design SQLAlchemy models for data persistence
4. **API Integration**: Create REST endpoints for all analysis features
5. **Advanced AI Detection**: Implement ML models for content classification
6. **Report Generation**: Build PDF reports with visualizations
7. **Performance Optimization**: Cache and async processing setup
8. **Testing Suite**: Comprehensive pytest test coverage
9. **Docker Deployment**: Containerize for production use
10. **Documentation**: Generate API docs and developer guides

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please feel free to submit pull requests.

## 📧 Support

For issues and questions, please open an issue on GitHub.

---

**Last Updated**: January 2026
**Created by**: Arpan Choudhury
