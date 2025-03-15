# main.py
import sys
import os
import json
import threading
import queue
import time
import pyaudio
from vosk import Model, KaldiRecognizer
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.clock import Clock
from interface import load_interface
from function import (
    clean_transcript,
    summarize_text,
    extract_keywords_spacy,
    highlight_keywords,
    get_wiki_summary
)

if hasattr(sys, '_MEIPASS'):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)

vosk_model_folder = os.path.join(base_path, "vosk-model-small-en-us-0.15")
iconpath = os.path.join(base_path, "noteTakingApp.png")

Window.size = (700, 900)

class MyNoteTakerApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vosk_model_path = vosk_model_folder
        if not os.path.exists(self.vosk_model_path):
            print("[Warning] Vosk model folder not found!")
        self.audio_queue = queue.Queue()
        self.transcript_queue = queue.Queue()
        self.stop_event = threading.Event()
        self.recording_thread = None
        self.full_transcript = ""
        self.partial_transcript = ""
        self.is_recording = False

    def build(self):
        self.icon = iconpath
        return load_interface()
    
    def toggle_recording(self):
        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording()

    def start_recording(self):
        self.stop_event.clear()
        self.full_transcript = ""
        self.partial_transcript = ""

        # Clear any old content
        self.root.ids.summary_label.text = ""
        self.root.ids.wiki_label.text = ""
        self.root.ids.transcript_label.text = "[Recording in progress...]"

        self.root.ids.record_button.text = "Stop Recording"

        self.recording_thread = threading.Thread(target=self.record_and_transcribe, daemon=True)
        self.recording_thread.start()

        Clock.schedule_interval(self.update_transcript_label, 2.5)
        self.is_recording = True

    def stop_recording(self):
        self.stop_event.set()
        if self.recording_thread:
            self.recording_thread.join()
            self.recording_thread = None

        self.root.ids.transcript_label.text = self.full_transcript
        Clock.unschedule(self.update_transcript_label)
        self.root.ids.record_button.text = "Start Recording"
        self.is_recording = False

    def record_and_transcribe(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        input=True,
                        frames_per_buffer=4096)

        model = Model(self.vosk_model_path)
        rec = KaldiRecognizer(model, 16000)

        try:
            while not self.stop_event.is_set():
                data = stream.read(4096, exception_on_overflow=False)
                if rec.AcceptWaveform(data):
                    result = rec.Result()
                    text = json.loads(result).get('text', '')
                    if text:
                        self.full_transcript += " " + text
                else:
                    partial = json.loads(rec.PartialResult()).get('partial', '')
                    self.partial_transcript = partial
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()

            # Handle final chunk of text
            final_result = json.loads(rec.FinalResult()).get('text', '')
            if final_result:
                self.full_transcript += " " + final_result

    def update_transcript_label(self, dt):
        combined = self.full_transcript + " " + self.partial_transcript
        self.root.ids.transcript_label.text = combined.strip()

    def summarize_transcript(self):
        cleaned = clean_transcript(self.full_transcript)
        
        if not cleaned.strip():
            self.root.ids.summary_label.text = "[No transcript to summarize]"
            return
        
        # Show "Summarizing the note..." message before summarization starts
        self.root.ids.summary_label.text = "[Summarizing the note...]"
        
        def process_summary(dt):
            summary_text = summarize_text(cleaned)
            keywords = extract_keywords_spacy(cleaned)
            highlighted_summary = highlight_keywords(summary_text, keywords, color="#0000FF")
            self.root.ids.summary_label.text = highlighted_summary

            wiki_texts = []
            for kw in keywords:
                info = get_wiki_summary(kw)
                if info:
                    wiki_texts.append(f"[b][color=#0000FF]{kw}[/color][/b]: {info}")
            self.root.ids.wiki_label.text = "\n\n".join(wiki_texts)


        Clock.schedule_once(process_summary, 0.5)


if __name__ == "__main__":
    MyNoteTakerApp().run()
