import customtkinter as ctk
import speech_recognition as sr
import pyttsx3
from youtube_search import YoutubeSearch
import webbrowser

# Initialiser la reconnaissance vocale
recognizer = sr.Recognizer()

# Initialiser la synthèse vocale avec gestion des erreurs
try:
    engine = pyttsx3.init('sapi5')  # Pour Windows
    voices = engine.getProperty('voices')
    
    # Chercher une voix française
    french_voice_found = False
    for voice in voices:
        # Recherche des identifiants de voix françaises
        if any(lang in voice.name.lower() for lang in ['french', 'français', 'fr']):
            engine.setProperty('voice', voice.id)
            french_voice_found = True
            print(f"Voix française sélectionnée : {voice.name}")
            break
    
    # Si aucune voix française n'est trouvée, installer et utiliser une voix française
    if not french_voice_found:
        print("Aucune voix française trouvée. Veuillez installer une voix française dans Windows :")
        print("1. Allez dans Paramètres Windows")
        print("2. Temps et langue > Langue")
        print("3. Ajoutez le français et téléchargez le pack de voix")

except:
    try:
        engine = pyttsx3.init('nsss')  # Pour macOS
        # Pour macOS, définir une voix française
        engine.setProperty('voice', 'com.apple.speech.synthesis.voice.thomas.premium')  # Voix française de macOS
    except:
        engine = pyttsx3.init('espeak')  # Pour Linux
        # Pour Linux/espeak, définir explicitement la voix française
        engine.setProperty('voice', 'fr')

# Configuration du moteur de synthèse vocale
engine.setProperty('rate', 150)    # Vitesse de parole
engine.setProperty('volume', 1.0)  # Volume

def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Erreur de synthèse vocale : {e}")

def recognize_speech():
    with sr.Microphone() as source:
        print("Ajustement au bruit ambiant...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Parlez maintenant...")
        
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            print("Traitement de la voix...")
            command = recognizer.recognize_google(audio, language="fr-FR")
            print(f"Vous avez dit : {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Je n'ai pas compris")
            speak("Je n'ai pas compris")
            return ""
        except sr.RequestError:
            print("Erreur de connexion")
            speak("Erreur de connexion")
            return ""
        except Exception as e:
            print(f"Erreur : {e}")
            speak("Une erreur s'est produite")
            return ""

def execute_command():
    try:
        command = recognize_speech()
        if not command:
            return
        
        if "jarvis" in command:
            speak("Heureux de vous revoir monsieur")
            return

        if "joue" in command:
            song_name = command.replace("joue", "").strip()
            speak(f"Je recherche {song_name} sur Youtube")

            try:
                results = YoutubeSearch(song_name, max_results=1).to_dict()
                if results:
                    video_url = f"https://www.youtube.com/watch?v={results[0]['id']}"
                    speak(f"Je lance la lecture de {results[0]['title']}")
                    webbrowser.open(video_url)
                else:
                    speak("Je n'ai pas trouvé ce titre sur Youtube")
            except Exception as e:
                print(f"Erreur lors de la recherche YouTube : {e}")
                speak("Erreur lors de la recherche sur YouTube")

        elif "ouvre youtube" in command:
            speak("J'ouvre Youtube")
            webbrowser.open("https://www.youtube.com")

        elif "ouvre google" in command:
            speak("J'ouvre Google")
            webbrowser.open("https://www.google.com")
        
        elif "ferme" in command or "quitter" in command:
            speak("Je ferme l'application")
            app.quit()

        else:
            speak("Je n'ai pas reconnu cette commande")
            
    except Exception as e:
        print(f"Erreur lors de l'exécution de la commande : {e}")
        speak("Une erreur s'est produite")

# Configuration de l'interface
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Création de la fenêtre principale
app = ctk.CTk()
app.title("Assistant Jarvis")
app.geometry("500x400")
app.resizable(False, False)

# Création des widgets
label = ctk.CTkLabel(
    app, 
    text="Cliquez sur le bouton pour parler",
    font=("Helvetica", 16)
)
label.pack(pady=30)

ecoute_bouton = ctk.CTkButton(
    app,
    text="Parler",
    command=execute_command,
    font=("Helvetica", 14),
    height=50,
    width=200
)
ecoute_bouton.pack(pady=20)

quitter_bouton = ctk.CTkButton(
    app,
    text="Quitter",
    command=app.quit,
    font=("Helvetica", 14),
    height=50,
    width=200,
    fg_color="red",
    hover_color="#c92a2a"
)
quitter_bouton.pack(pady=20)

# Démarrage de l'application
app.mainloop()