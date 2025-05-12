import pyttsx3
import os

def text_to_speech(text, filename="output.mp3"):
    """Converts text to speech and saves as an MP3 file."""
    if not text.strip():
        return None

    engine = pyttsx3.init()
    
    # Optional: Change voice properties
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 1.0)  # Volume level (0.0 to 1.0)

    # Save speech to file
    engine.save_to_file(text, filename)
    engine.runAndWait()
    
    return filename  # Return the generated file name

# Example Usage:
if __name__ == "__main__":
    sample_text = "Hello! This is a text-to-speech test using Python."
    audio_file = text_to_speech(sample_text, "speech.mp3")
    if audio_file:
        print(f"Speech saved as {audio_file}")
    else:
        print("No text provided.")
