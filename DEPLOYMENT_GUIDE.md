# Streamlit Cloud Deployment Guide

## Overview
This guide will walk you through deploying the AI Plagiarism Detector to Streamlit Cloud in less than 5 minutes.

## Prerequisites
- GitHub account
- Streamlit Cloud account (free)
- This repository code

## Step-by-Step Deployment

### 1. Ensure Code is on GitHub
✅ Your code is already pushed to GitHub at:
```
https://github.com/Arpan-234/AI-Plagiarism-Detector
```

### 2. Visit Streamlit Cloud
1. Go to https://streamlit.io/cloud
2. Click "Launch app"
3. Sign in with your GitHub account

### 3. Deploy Your App
1. Click "New app" button
2. Select repository: `Arpan-234/AI-Plagiarism-Detector`
3. Select branch: `main`
4. Set main file path: `app.py`
5. Click "Deploy"

### 4. Wait for Deployment
Streamlit Cloud will:
- Install dependencies from `requirements.txt`
- Build and launch your Streamlit app
- Provide you with a unique URL like: `https://your-app-name.streamlit.app`

## After Deployment

### Configure Backend Connection
By default, the app uses `http://localhost:5000` for the backend.

To use a remote backend:
1. Open the app
2. In the sidebar, change "Backend URL" to your backend server URL
3. The setting is saved in the session

### Environment Variables
To use environment variables for sensitive data:
1. In Streamlit Cloud dashboard, go to "Settings"
2. Add secrets under "Secrets" section
3. Access in your app via `st.secrets["key_name"]`

## Troubleshooting

### App Not Loading
- Check if all dependencies in `requirements.txt` are compatible
- View logs in Streamlit Cloud dashboard
- Ensure `app.py` exists in root directory

### Backend Connection Error
- Verify backend server is running and accessible
- Check the backend URL in the app sidebar
- Ensure CORS is enabled on backend

### Missing Dependencies
- Add to `requirements.txt` and push to GitHub
- Streamlit Cloud will automatically redeploy

## Customization

### Change App Name
Edit `.streamlit/config.toml`:
```toml
[client]
tooltipFont = "sans serif"
```

### Change Colors/Theme
Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#0f1419"
secondaryBackgroundColor = "#262730"
textColor = "#fafafa"
```

### Increase File Upload Size
Edit `.streamlit/config.toml`:
```toml
[server]
maxUploadSize = 100
```

## Sharing Your App
Your app URL is automatically shareable:
- Share directly: `https://your-app-name.streamlit.app`
- Works on desktop and mobile
- Real-time updates when you push to GitHub

## Scaling

For free tier:
- Up to 3 apps per account
- Dormant app goes to sleep after 7 days of inactivity
- Wake up automatically on new traffic

For Pro/Business:
- Unlimited apps
- Always-on apps
- Custom domain
- Priority support

## Common URLs

| Resource | URL |
|----------|-----|
| App | https://your-app-name.streamlit.app |
| Code | https://github.com/Arpan-234/AI-Plagiarism-Detector |
| Streamlit Docs | https://docs.streamlit.io |
| Streamlit Cloud | https://streamlit.io/cloud |

## Next Steps

1. **Monitor Performance**: Check Streamlit Cloud dashboard for app statistics
2. **Set Up Backend**: Deploy a Flask/FastAPI backend for full functionality
3. **Add Features**: Use the Claude prompts from README.md to extend functionality
4. **Customize Theme**: Edit `.streamlit/config.toml` for your branding

## Support

- GitHub Issues: https://github.com/Arpan-234/AI-Plagiarism-Detector/issues
- Streamlit Community: https://discuss.streamlit.io
- Documentation: https://docs.streamlit.io

---

**Last Updated**: January 2026
**Maintained by**: Arpan Choudhury
