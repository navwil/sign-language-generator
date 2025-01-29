# SIGN LANGUAGE GENERATOR FROM SPEECH

This project converts audio speech to sign language animations. It uses Django for the web framework, NLTK for natural language processing, and OpenCV for video processing.

## Features

* Record audio speech from the user's microphone.
* Convert the speech to text using Google Speech Recognition.
* Preprocess the text using NLTK (tokenization, stemming, lemmatization, POS tagging).
* Detect the tense of the sentence.
* Remove stop words.
* Look up the corresponding sign language animations for each word.
* Play the animations in sequence.

## Requirements

* Python 3.7 or higher
* Django 3.0 or higher
* NLTK 3.5 or higher
* OpenCV 4.1.0 or higher
* PyAudio
* SpeechRecognition
* Graphviz

## Installation

1. Clone the repository:
2. Install the requirements:
3.  Download the NLTK data:
4. Create a superuser account:
5. Run the development server:
6. 6. Open your web browser and go to `http://127.0.0.1:8000/`.

## Usage

1. Click on the "Click to Start" button.
2. Allow the browser to access your microphone.
3. Speak into the microphone.
4. The recorded speech will be converted to text and displayed on the screen.
5. The corresponding sign language animations will be played in sequence.

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

## License

This project is licensed under the MIT License.
