# 🤖 AI Interview Coach

An intelligent mock interview application built with Streamlit that helps you practice job interviews using AI-powered questions and feedback, with speech recognition capabilities.

## ✨ Features

- **AI-Powered Questions**: Dynamic interview questions based on your CV/resume
- **Speech Recognition**: Voice input for natural interview simulation
- **Text-to-Speech**: Audio playback of interview questions
- **Real-time Feedback**: AI-generated feedback on your responses
- **CV Analysis**: Upload PDF or text resumes for personalized questions
- **Audio Mode**: Complete hands-free interview experience
- **Progress Tracking**: Multi-question interview sessions

## 🔧 Prerequisites

- **Python 3.8+** (Tested with Python 3.12)
- **Windows/Mac/Linux** (Instructions below are for Windows)
- **OpenAI API Key** (Required for AI functionality)
- **Microphone** (For speech recognition features)
- **Internet Connection** (For AI services)

## 📋 Installation Guide

### Step 1: Clone or Download the Project

```bash
git clone <your-repository-url>
cd ai-interview-coach-streamlit
```

Or download the ZIP file and extract it to your desired location.

### Step 2: Set Up Python Virtual Environment

**On Windows:**
```cmd
# Navigate to project directory
cd ai-interview-coach-streamlit

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

**On Mac/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

You should see `(venv)` at the beginning of your command prompt when activated.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install Speech Recognition Dependencies

**Windows (Usually works automatically):**
```cmd
pip install https://github.com/intxcc/pyaudio_portaudio/releases/download/v0.2.11/PyAudio-0.2.11-cp312-cp312-win_amd64.whl
```

**Mac:**
```bash
brew install portaudio
pip install pyaudio
```

**Linux (Ubuntu):**
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

### Step 5: Set Up OpenAI API Key

1. **Get an OpenAI API Key:**
   - Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
   - Create an account or log in
   - Click "Create new secret key"
   - Copy the key (starts with `sk-`)

2. **Create Environment File:**
   Create a `.env` file in the project root directory:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```
   
   Replace `your_openai_api_key_here` with your actual API key.

**⚠️ Important:** Never share your API key publicly or commit it to version control.

### Step 6: Configure Windows Microphone (If Using Speech Features)

1. **Check Microphone Permissions:**
   - Go to **Settings → Privacy & Security → Microphone**
   - Ensure "Microphone access" is **ON**
   - Allow **Desktop apps** to access microphone

2. **Set Default Microphone:**
   - Right-click speaker icon in system tray
   - Select "Open Sound settings"
   - Choose your preferred microphone as default input device
   - Test microphone and adjust volume (recommended: 70-100%)

## 🚀 Running the Application

### Step 1: Activate Virtual Environment
```cmd
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Step 2: Start the Application
```bash
streamlit run main.py
```

### Step 3: Open in Browser
The application will automatically open in your default web browser at:
```
http://localhost:8501
```

If it doesn't open automatically, manually navigate to the URL above.

## 📖 How to Use

### 1. Initial Setup
- Enter your full name
- Upload your CV/Resume (PDF or TXT format)
- Enable "Audio Mode" if you want to use speech features
- Click "🚀 Start Mock Interview"

### 2. During the Interview
- **Read/Listen** to the AI-generated questions
- **Respond** using voice recording or text input
- **Submit** your response to get the next question
- Continue for 3 questions (default setting)

### 3. Speech Features
- **🔊 Play Question**: Listen to questions read aloud
- **🎤 Record Response**: Voice input for your answers
- **🔧 Test Mic**: Check if your microphone is working
- **Voice Tips**: Speak continuously with minimal pauses (1.5 seconds max pause)

### 4. Get Feedback
- After completing all questions, receive detailed AI feedback
- Review strengths, areas for improvement, and recommendations
- Start a new interview session if desired

## 🔧 Troubleshooting

### Speech Recognition Not Working

**Check Microphone Setup:**
1. Use the "🔧 Test Mic" button to verify microphone detection
2. Ensure microphone permissions are enabled
3. Try different microphone if available
4. Check Windows sound settings

**Common Solutions:**
- Speak louder and closer to microphone
- Reduce background noise
- Use a headset microphone for better quality
- Disable other applications using the microphone

### OpenAI API Errors

**"Error generating question" messages:**
1. Verify API key is correct in `.env` file
2. Check internet connection
3. Ensure you have OpenAI API credits available
4. Check OpenAI service status

### Installation Issues

**PyAudio Installation Fails:**
- Use the Windows wheel provided in installation steps
- Try installing Visual C++ Build Tools
- Consider using `pipwin` package manager

**Module Import Errors:**
- Ensure virtual environment is activated
- Reinstall requirements: `pip install -r requirements.txt`
- Check Python version compatibility

## 📁 Project Structure

```
ai-interview-coach-streamlit/
├── main.py              # Main Streamlit application
├── services.py          # AI service integration
├── models.py           # Data models and classes
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create this)
├── README.md          # This file
├── venv/              # Virtual environment (created during setup)
├── uploads/           # Temporary file uploads
└── docs/              # Documentation
```

## 🔒 Privacy & Security

- **Local Processing**: CV text is processed locally and in memory only
- **API Usage**: Questions and responses are sent to OpenAI for processing
- **No Data Storage**: No interview data is permanently stored
- **Session-Based**: All data is cleared when you close the browser

## 📝 Requirements

### Python Packages
- streamlit==1.48.1
- openai==1.100.2
- PyPDF2==3.0.1
- SpeechRecognition==3.14.3
- pyaudio==0.2.11
- gTTS==2.5.4
- python-dotenv==1.1.1
- pydub==0.25.1

### System Requirements
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 500MB for dependencies
- **Network**: Stable internet connection for AI services

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter issues:

1. **Check this README** for common solutions
2. **Test microphone** using built-in test feature
3. **Verify API key** setup and OpenAI account status
4. **Check Python version** compatibility
5. **Review error messages** in the Streamlit interface

## 🙏 Acknowledgments

- **OpenAI** for GPT-3.5 API
- **Streamlit** for the web framework
- **SpeechRecognition** library for voice input
- **gTTS** for text-to-speech functionality

---

**Happy interviewing! 🎯** Practice makes perfect, and this AI coach is here to help you succeed in your job interviews.