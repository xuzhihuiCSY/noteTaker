# noteTaker
make sure install requirement:
```
pip install vosk pyaudio kivy kivymd spacy transformers wikipedia

# Download and link the spaCy English model
python -m spacy download en_core_web_sm
```

Download vosk-model-small-en-us-0.15 to the root directory
https://alphacephei.com/vosk/models 

unzip the folder and also place it in the root directory
it should look like this:
```
.
├── main.py            # Entry point of the application (KivyMD App logic, audio recording, transcription)
├── function.py        # Functions for text processing (cleaning, summarizing, keyword extraction)
├── interface.py       # Kivy layout (GUI design)
├── vosk-model-small-en-us-0.15
│   └── ...            # Vosk model files (required to be in the same directory)
└── requirements.txt   # (Optional) If you provide or create a list of dependencies
```

lastly run the script:
```
python main.py
```

you can download the exe for windows demo:
https://drive.google.com/file/d/1DMjpb8vtG0tsCZqnJEAoCJr0B6aTPV0M/view?usp=sharing
