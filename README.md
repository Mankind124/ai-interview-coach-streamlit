# 🤖 AI Interview Coach

An intelligent mock interview application built with Streamlit that helps you practice job interviews using **GPT-4-powered** questions and feedback, with advanced speech recognition capabilities and comprehensive interview evaluation.

## ✨ Key Features

### 🧠 **AI-Powered Intelligence**
- **GPT-4 Integration**: Advanced question generation and feedback analysis
- **Job-Targeted Questions**: 10 customized questions based on specific job descriptions
- **Grammar Correction Agent**: Automatic grammar improvement for your responses
- **STAR Method Evaluation**: Comprehensive scoring using the STAR framework (Situation, Task, Action, Result)
- **Real-time Analysis**: Intelligent feedback on communication skills and content quality

### 🎤 **Advanced Speech Features**
- **Extended Speech Recognition**: 60-second recording with 2.5-second pause detection
- **Auto-Play Questions**: Questions automatically play in audio mode
- **Auto-Submit Responses**: Seamless voice workflow with automatic submission
- **Natural Conversation Flow**: No artificial question numbering for realistic experience
- **Microphone Testing**: Built-in microphone diagnostics and setup

### 📋 **Professional Interview Experience**
- **CV/Resume Analysis**: Upload PDF files for personalized question generation
- **Company-Specific Targeting**: Enter job title, company name, and description for relevant questions
- **Progress Tracking**: Visual progress indicators throughout the interview
- **Comprehensive Feedback**: Detailed analysis with strengths, improvements, and recommendations
- **Downloadable Reports**: Export your interview feedback for future reference

### 🌐 **Cloud & Local Deployment**
- **Cloud-Ready**: Automatic environment detection and graceful feature degradation
- **Local Development**: Full speech recognition support for Windows/Mac/Linux
- **Streamlit Cloud Compatible**: Seamless deployment without manual configuration

## 🔧 Prerequisites

- **Python 3.8+** (Tested with Python 3.12)
- **Windows/Mac/Linux** (Cross-platform support)
- **OpenAI API Key** (Required for GPT-4 functionality)
- **Microphone** (Optional - for speech recognition features)
- **Internet Connection** (For AI services and cloud deployment)

## 📋 Installation Guide

### Option 1: Local Development (Full Features)

#### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/ai-interview-coach-streamlit.git
cd ai-interview-coach-streamlit
```

#### Step 2: Set Up Python Virtual Environment

**On Windows:**
```cmd
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

#### Step 3: Install Dependencies

**For Local Development (with speech recognition):**
```bash
pip install -r requirements-local.txt
```

**For Cloud Deployment (text-only):**
```bash
pip install -r requirements.txt
```

#### Step 4: Install Speech Recognition Dependencies (Local Only)

**Windows:**
```cmd
pip install https://files.pythonhosted.org/packages/5a/5b/1bf7e5ef0c85c5c5c20c7b8e2c5f43ff76e23ce0c81eccc6b8f77e9f5a938/PyAudio-0.2.11-cp312-cp312-win_amd64.whl
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

### Option 2: Cloud Deployment (Streamlit Cloud)

1. **Fork this repository** on GitHub
2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select your forked repository
   - Set `main.py` as the main file
3. **Add environment variables** in Streamlit Cloud secrets:
   ```
   OPENAI_API_KEY = "your-openai-api-key-here"
   ```

> **Note:** Cloud deployment automatically uses text-only mode as speech recognition isn't available in cloud environments.
#### Step 5: Set Up OpenAI API Key

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

## 🚀 Running the Application

### Local Development

```bash
# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Start the application
streamlit run main.py
```

### Access the Application
Open your browser and navigate to: `http://localhost:8501`

## 📖 How to Use

### 1. Initial Setup
- **Enter Personal Details**: Full name for personalized experience
- **Upload CV/Resume**: PDF format supported for intelligent question generation
- **Job Information**: 
  - Job title you're applying for
  - Company name
  - Detailed job description for targeted questions
- **Choose Mode**: Enable Audio Mode for speech features (local only) or use Text Mode

### 2. Interview Experience

#### **Audio Mode (Local Development)**
- **🔊 Auto-Play**: Questions automatically play when generated
- **🎤 Voice Recording**: 60-second recording with smart pause detection
- **📝 Auto-Submit**: Responses automatically processed after recording
- **🔧 Microphone Test**: Built-in diagnostics for optimal setup

#### **Text Mode (Local & Cloud)**
- **💬 Text Input**: Type responses in the text area
- **🔊 Manual Audio**: Click to play question audio
- **✅ Manual Submit**: Click submit when ready for next question

### 3. Advanced Features

#### **Grammar Correction**
- **Auto-correction**: All responses automatically grammar-checked
- **Professional Polish**: Maintains your meaning while improving clarity
- **Real-time Processing**: Instant feedback integration

#### **STAR Method Evaluation**
Each response evaluated on:
- **Situation**: Context and background (0-10)
- **Task**: Responsibilities and objectives (0-10) 
- **Action**: Steps taken and decisions made (0-10)
- **Result**: Outcomes and achievements (0-10)

#### **10-Question Interview**
- **Job-Targeted**: Questions specifically tailored to your job description
- **Progressive Difficulty**: Questions build on previous responses
- **Natural Flow**: No artificial numbering for realistic conversation

### 4. Comprehensive Feedback
- **Detailed Analysis**: Strengths, areas for improvement, specific recommendations
- **STAR Scoring**: Individual scores for each framework component
- **Professional Insights**: Industry-specific advice and tips
- **Downloadable Report**: Export feedback for future reference

## 🔧 Troubleshooting

### Speech Recognition Issues (Local Only)

**Microphone Not Detected:**
1. Use the "🔧 Test Mic" button to verify detection
2. Check Windows microphone permissions:
   - Settings → Privacy & Security → Microphone
   - Enable "Microphone access" and "Desktop apps"
3. Set default microphone in Windows sound settings
4. Restart the application after changes

**Speech Not Recognized:**
- Speak clearly and at normal volume
- Reduce background noise
- Use a headset microphone for better quality
- Ensure 70-100% microphone volume in Windows
- Wait for the "Listening..." indicator before speaking

### OpenAI API Issues

**"Error generating question" messages:**
- Verify API key is correctly set in `.env` file
- Check internet connection stability
- Ensure OpenAI API credits are available
- Verify API key has GPT-4 access permissions

**Rate Limiting:**
- Wait a few minutes between requests
- Check your OpenAI usage limits
- Consider upgrading your OpenAI plan

### Installation Problems

**PyAudio Installation Fails (Windows):**
- Use the provided Windows wheel URL
- Install Visual C++ Build Tools if needed
- Try: `pip install pipwin && pipwin install pyaudio`

**Import Errors:**
- Ensure virtual environment is activated
- Reinstall: `pip install -r requirements-local.txt`
- Check Python version (3.8+ required)

### Cloud Deployment Issues

**Streamlit Cloud Deployment Fails:**
- Ensure you're using `requirements.txt` (not `requirements-local.txt`)
- Check that your GitHub repository is public or properly connected
- Verify environment variables are set correctly in Streamlit Cloud
- Wait for automatic redeployment after pushing fixes

## 🌐 Environment Compatibility

### Local Development
- ✅ **Full Features**: Speech recognition, voice recording, GPT-4 analysis
- ✅ **Platforms**: Windows, Mac, Linux
- ✅ **Audio Mode**: Complete hands-free experience
- ✅ **Text Mode**: Fallback option available

### Cloud Deployment (Streamlit Cloud)
- ✅ **Core Features**: GPT-4 questions, grammar correction, STAR evaluation
- ✅ **Text Mode**: Full functionality without speech recognition
- ✅ **Auto-Adaptation**: Graceful feature degradation
- ❌ **Audio Mode**: Speech recognition unavailable (Linux limitation)

## 📁 Project Structure

```
ai-interview-coach-streamlit/
├── main.py                 # Main Streamlit application
├── services.py            # GPT-4 service integration
├── models.py              # Data models and session management
├── requirements.txt       # Cloud deployment dependencies
├── requirements-local.txt # Local development dependencies (with speech)
├── requirements-cloud.txt # Backup cloud requirements
├── .env                   # Environment variables (create this)
├── DEPLOYMENT.md          # Cloud deployment guide
├── README.md              # This comprehensive guide
├── venv/                  # Virtual environment (created during setup)
├── uploads/               # Temporary file uploads (auto-created)
└── docs/                  # Additional documentation
```

## � Features Comparison

| Feature | Local Development | Cloud Deployment |
|---------|------------------|------------------|
| GPT-4 Questions | ✅ | ✅ |
| Grammar Correction | ✅ | ✅ |
| STAR Method Evaluation | ✅ | ✅ |
| Job-Targeted Questions | ✅ | ✅ |
| CV/PDF Upload | ✅ | ✅ |
| Text Input | ✅ | ✅ |
| Text-to-Speech | ✅ | ✅ |
| Speech Recognition | ✅ | ❌ |
| Audio Mode | ✅ | ❌ |
| Downloadable Feedback | ✅ | ✅ |

## 📝 Technical Requirements

### Local Development
```
Python Packages (requirements-local.txt):
- streamlit==1.48.1
- openai==1.100.2
- PyPDF2==3.0.1
- SpeechRecognition==3.14.3
- pyaudio==0.2.11
- gTTS==2.5.4
- python-dotenv==1.1.1
- pydub==0.25.1
+ 50+ additional dependencies
```

### Cloud Deployment
```
Python Packages (requirements.txt):
- streamlit==1.48.1
- openai==1.100.2
- PyPDF2==3.0.1
- gTTS==2.5.4
- python-dotenv==1.1.1
- pydub==0.25.1
+ 45+ additional dependencies (no speech libs)
```

### System Requirements
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 1GB for dependencies and models
- **Network**: Stable internet for GPT-4 API calls
- **Browser**: Modern browser (Chrome, Firefox, Safari, Edge)

## 🔒 Privacy & Security

### Data Handling
- **Local Processing**: CV text processed locally in memory only
- **API Communication**: Encrypted HTTPS communication with OpenAI
- **No Persistent Storage**: Interview data deleted after session ends
- **Session-Based**: All data cleared when browser is closed

### Security Best Practices
- **API Key Protection**: Store in `.env` file, never commit to version control
- **Environment Variables**: Use Streamlit Cloud secrets for production
- **Data Minimization**: Only necessary data sent to AI services
- **Temporary Files**: Uploaded CVs automatically deleted after processing

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository** on GitHub
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes** with clear, well-documented code
4. **Test thoroughly** in both local and cloud environments
5. **Update documentation** if necessary
6. **Submit a pull request** with a clear description of changes

### Development Guidelines
- Follow Python PEP 8 style guidelines
- Add docstrings for new functions
- Test speech recognition features on multiple platforms
- Ensure cloud compatibility for new features
- Update requirements files appropriately

## � Version History

### Latest Version (Current)
- **GPT-4 Integration**: Upgraded from GPT-3.5 for superior question quality
- **Grammar Correction Agent**: Automatic response polishing
- **STAR Method Evaluation**: Comprehensive behavioral interview scoring
- **10-Question Interviews**: Extended from 3 to 10 targeted questions
- **Job-Specific Targeting**: Questions tailored to job descriptions
- **Cloud Deployment Ready**: Automatic environment adaptation
- **Natural Conversation Flow**: Removed artificial question numbering
- **Auto-Play/Auto-Submit**: Seamless audio mode experience
- **Extended Speech Recognition**: 60-second recording with smart pause detection

### Previous Features
- Basic interview simulation with GPT-3.5
- 3-question interview sessions
- Simple speech recognition
- Basic feedback generation

## �📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License Summary
- ✅ **Commercial Use**: Use in commercial projects
- ✅ **Modification**: Modify and adapt the code
- ✅ **Distribution**: Share and distribute
- ✅ **Private Use**: Use privately
- ❌ **Liability**: No warranty or liability
- ❌ **Trademark Use**: No trademark rights included

## 🆘 Support & Help

### Getting Help
1. **Check this README** for comprehensive setup and troubleshooting
2. **Review DEPLOYMENT.md** for cloud-specific guidance
3. **Test microphone** using the built-in diagnostic feature
4. **Verify API key** setup and OpenAI account status
5. **Check Python version** and dependency compatibility

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Speech recognition not working | Check microphone permissions, test mic button |
| OpenAI API errors | Verify API key, check credits, ensure GPT-4 access |
| Cloud deployment fails | Use requirements.txt, check environment variables |
| Import errors | Activate virtual environment, reinstall requirements |
| Audio not playing | Enable audio permissions, check browser settings |

### Community Support
- **GitHub Issues**: Report bugs and request features
- **Discussions**: Ask questions and share experiences
- **Pull Requests**: Contribute improvements and fixes

## 🙏 Acknowledgments

- **OpenAI** for GPT-4 API and advanced language models
- **Streamlit** for the excellent web framework and cloud platform
- **SpeechRecognition** library maintainers for robust voice input
- **gTTS (Google Text-to-Speech)** for natural audio generation
- **PyAudio** community for cross-platform audio support
- **Contributors** who help improve this project

## 🌟 Special Features

### 🧠 **Advanced AI Analysis**
Our GPT-4 integration provides:
- **Contextual Understanding**: Questions that build on previous responses
- **Industry-Specific Insights**: Tailored advice for different job sectors
- **Behavioral Assessment**: STAR method evaluation with detailed scoring
- **Professional Communication**: Grammar correction maintaining your voice

### 🎯 **Interview Optimization**
- **Realistic Simulation**: Natural conversation flow without artificial constraints
- **Comprehensive Coverage**: 10 questions covering technical and behavioral aspects
- **Adaptive Questioning**: AI adjusts difficulty based on your responses
- **Professional Feedback**: Actionable insights for interview improvement

### 🔧 **Technical Excellence**
- **Cross-Platform Compatibility**: Works on Windows, Mac, and Linux
- **Cloud-Ready Architecture**: Seamless deployment on Streamlit Cloud
- **Graceful Degradation**: Features adapt to available environment capabilities
- **User-Friendly Interface**: Intuitive design for all skill levels

---

**🎯 Ready to ace your next interview?** 

Start practicing with AI-powered questions, get instant feedback, and build confidence for your dream job interview!

**🚀 [Deploy on Streamlit Cloud](https://share.streamlit.io) | 💻 [Run Locally](http://localhost:8501)**