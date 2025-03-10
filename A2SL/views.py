from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
from nltk import pos_tag
from django.contrib.staticfiles import finders
from django.contrib.auth.decorators import login_required
from nltk.stem import PorterStemmer

import cv2
import pyaudio
import wave
import threading
import os
import speech_recognition as sr

# Ensure NLTK data is downloaded
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')

def home_view(request):
    return render(request, 'home.html')

def about_view(request):
    return render(request, 'about.html')

def contact_view(request):
    return render(request, 'contact.html')

def record_video_audio(request):
    if request.method == 'POST':
        video_filename = 'output.avi'
        audio_filename = 'output.wav'
        chunk = 1024
        sample_format = pyaudio.paInt16
        channels = 2
        fs = 44100

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return JsonResponse({'error': 'Could not open video.'})

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(video_filename, fourcc, 20.0, (640, 480))

        p = pyaudio.PyAudio()
        try:
            stream = p.open(format=sample_format, channels=channels, rate=fs, output=False, input=True, frames_per_buffer=chunk)
        except Exception as e:
            return JsonResponse({'error': f'Error opening audio stream: {e}'})

        frames = []

        def record_audio():
            while recording:
                data = stream.read(chunk)
                frames.append(data)

        recording = True
        audio_thread = threading.Thread(target=record_audio)
        audio_thread.start()

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                out.write(frame)
                cv2.imshow('Video Feed', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        except Exception as e:
            return JsonResponse({'error': f'Error during recording: {e}'})
        finally:
            recording = False
            audio_thread.join()
            stream.stop_stream()
            stream.close()
            p.terminate()
            cap.release()
            out.release()
            cv2.destroyAllWindows()

        with wave.open(audio_filename, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(sample_format))
            wf.setframerate(fs)
            wf.writeframes(b''.join(frames))

        if os.path.exists(video_filename):
            os.remove(video_filename)

        text = process_audio(audio_filename)
        if text:
            final_converted_text = process_text(text)
            if os.path.exists(audio_filename):
                os.remove(audio_filename)
            return JsonResponse({'text': final_converted_text})
        else:
            return JsonResponse({'error': 'No text extracted from audio.'})
    return render(request, 'record.html')

def process_audio(audio_filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_filename) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            return None

def remove_consecutive_repeats(words):
    if not words:
        return words
    result = [words[0]]
    for i in range(1, len(words)):
        if words[i] != words[i - 1]:
            result.append(words[i])
    return result

def process_text(text):
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    stemmer = PorterStemmer()
    words = text.split()
    processed_text = []
    for word in words:
        if word.lower() not in stop_words:
            lemmatized_word = lemmatizer.lemmatize(word)
            stemmed_word = stemmer.stem(lemmatized_word)
            processed_text.append(stemmed_word)
    
    # Remove consecutive repeated words
    processed_text = remove_consecutive_repeats(processed_text)
    
    final_text = ' '.join(processed_text)
    sentences = final_text.split('. ')
    converted_sentences = [convert_to_verb_subject(sentence) for sentence in sentences]
    final_converted_text = '. '.join(converted_sentences)
    return final_converted_text

def convert_to_verb_subject(sentence):
    words = word_tokenize(sentence)
    tagged = pos_tag(words)
    converted_sentence = []
    i = 0
    while i < len(tagged):
        word, tag = tagged[i]
        if i < len(tagged) - 1 and tag.startswith('NN') and tagged[i+1][1].startswith('VB'):
            converted_sentence.append(tagged[i+1][0])
            converted_sentence.append(word)
            i += 2
        else:
            converted_sentence.append(word)
            i += 1
    return ' '.join(converted_sentence)

def animation_view(request):
    if request.method == 'POST':
        text = request.POST.get('sen')
        text = text.lower()
        words = word_tokenize(text)
        ps = PorterStemmer()
        lr = WordNetLemmatizer()
        stemmed_words = [ps.stem(word) for word in words]
        lemmatized_words = [lr.lemmatize(word) for word in words]
        tagged = nltk.pos_tag(lemmatized_words)
        tense = {
            "future": len([word for word in tagged if word[1] == "MD"]),
            "present": len([word for word in tagged if word[1] in ["VBP", "VBZ", "VBG"]]),
            "past": len([word for word in tagged if word[1] in ["VBD", "VBN"]]),
            "present_continuous": len([word for word in tagged if word[1] in ["VBG"]])
        }
        stop_words = set(["mightn't", 're', 'wasn', 'wouldn', 'be', 'has', 'that', 'does', 'shouldn', 'do', "you've", 'off', 'for', "didn't", 'm', 'ain', 'haven', "weren't", 'are', "she's", "wasn't", 'its', "haven't", "wouldn't", 'don', 'weren', 's', "you'd", "don't", 'doesn', "hadn't", 'is', 'was', "that'll", "should've", 'a', 'then', 'the', 'mustn', 'i', 'nor', 'as', "it's", "needn't", 'd', 'am', 'have', 'hasn', 'o', "aren't", "you'll", "couldn't", "you're", "mustn't", 'didn', "doesn't", 'll', 'an', 'hadn', 'whom', 'y', "hasn't", 'itself', 'couldn', 'needn', "shan't", 'isn', 'been', 'such', 'shan', "shouldn't", 'aren', 'being', 'were', 'did', 'ma', 't', 'having', 'mightn', 've', "isn't", "won't"])
        filtered_text = []
        for w, p in zip(lemmatized_words, tagged):
            if w not in stop_words:
                if p[1] in ['VBG', 'VBD', 'VBZ', 'VBN', 'NN']:
                    filtered_text.append(lr.lemmatize(w, pos='v'))
                elif p[1] in ['JJ', 'JJR', 'JJS', 'RBR', 'RBS']:
                    filtered_text.append(lr.lemmatize(w, pos='a'))
                else:
                    filtered_text.append(lr.lemmatize(w))
        words = filtered_text
        temp = []
        for w in words:
            if w == 'i':
                temp.append('me')
            else:
                temp.append(w)
        words = temp
        probable_tense = max(tense, key=tense.get)
        if probable_tense == "past" and tense["past"] >= 1:
            temp = ["before"]
            temp = temp + words
            words = temp
        elif probable_tense == "future" and tense["future"] >= 1:
            if "will" not in words:
                temp = ["will"]
                temp = temp + words
                words = temp
        elif probable_tense == "present":
            if tense["present_continuous"] >= 1:
                temp = ["now"]
                temp = temp + words
                words = temp
                
        # Apply the remove_consecutive_repeats function to the words in animation_view as well
        words = remove_consecutive_repeats(words)
        
        filtered_text = []
        for w in words:
            path = w + ".mp4"
            f = finders.find(path)
            if not f:
                for c in w:
                    filtered_text.append(c)
            else:
                filtered_text.append(w)
        words = filtered_text
        return render(request, 'animation.html', {'words': words, 'text': text})
    else:
        return render(request, 'animation.html')

def logout_view(request):
    logout(request)
    return redirect("home")