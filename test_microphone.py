import speech_recognition as sr
import pyaudio

def test_microphone():
    """Test microphone and speech recognition setup"""
    print("Testing microphone setup...")
    
    # Test PyAudio
    try:
        p = pyaudio.PyAudio()
        print("✅ PyAudio initialized successfully")
        
        # List available audio devices
        print("\n📱 Available audio devices:")
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:  # Input devices only
                print(f"  {i}: {info['name']} (Channels: {info['maxInputChannels']})")
        
        p.terminate()
    except Exception as e:
        print(f"❌ PyAudio error: {e}")
        return False
    
    # Test Speech Recognition
    try:
        r = sr.Recognizer()
        print("\n🎤 Testing microphone...")
        
        with sr.Microphone() as source:
            print("📊 Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=1)
            
            print("🔴 Say something now! (5 seconds)")
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            
            print("🔄 Processing...")
            text = r.recognize_google(audio)
            print(f"✅ Heard: '{text}'")
            return True
            
    except sr.WaitTimeoutError:
        print("❌ No speech detected - timeout")
        return False
    except sr.UnknownValueError:
        print("❌ Could not understand audio")
        return False
    except sr.RequestError as e:
        print(f"❌ Google Speech Recognition error: {e}")
        return False
    except Exception as e:
        print(f"❌ General error: {e}")
        return False

if __name__ == "__main__":
    test_microphone()
