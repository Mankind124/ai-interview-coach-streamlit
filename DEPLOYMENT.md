# Cloud Deployment Guide

## Streamlit Cloud Deployment

The application has been made cloud-compatible by making speech recognition optional. When deployed to Streamlit Cloud:

### What Works:
✅ All core interview functionality  
✅ Text-to-speech for questions  
✅ Text input for responses  
✅ Grammar correction with GPT-4  
✅ STAR method evaluation  
✅ Job-targeted questions  
✅ Comprehensive feedback  
✅ PDF CV upload and parsing  

### What's Different in Cloud:
⚠️ Speech recognition is disabled (PyAudio not available)  
⚠️ Audio mode automatically switches to text mode  
⚠️ Users type responses instead of speaking  

### Deployment Steps:

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Cloud-compatible version"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to https://share.streamlit.io
   - Connect your GitHub repository
   - Select `main.py` as the main file
   - The app will automatically use the cloud-compatible requirements.txt

3. **Set Environment Variables:**
   - Add your `OPENAI_API_KEY` in the Streamlit Cloud secrets management
   - Format: `OPENAI_API_KEY = "your-api-key-here"`

### Local Development vs Cloud:

**Local (Windows):**
- Full speech recognition support
- PyAudio + SpeechRecognition enabled
- Audio mode available

**Cloud (Linux):**
- Text-only mode
- Speech recognition gracefully disabled
- All other features fully functional

### Requirements Files:

- `requirements.txt` - Cloud-compatible (no PyAudio/SpeechRecognition)
- `requirements-cloud.txt` - Backup cloud requirements
- Use `pip install -r requirements-local.txt` for local development with speech

The application automatically detects the environment and adapts accordingly!
