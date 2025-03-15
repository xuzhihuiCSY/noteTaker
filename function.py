import re
import en_core_web_sm
from transformers import pipeline
import wikipedia

nlp = en_core_web_sm.load()
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)

def clean_transcript(text: str) -> str:
    text_no_fillers = re.sub(r"\b(um|uh|er|like)\b", "", text, flags=re.IGNORECASE)
    text_no_fillers = re.sub(r"\s+", " ", text_no_fillers).strip()
    return text_no_fillers

def chunk_text(text: str, max_tokens: int = 500):
    """Splits long text into chunks within the model's token limit."""
    words = text.split()
    chunks = []
    while words:
        chunk = words[:max_tokens]
        chunks.append(" ".join(chunk))
        words = words[max_tokens:]
    return chunks

def summarize_text(text: str, max_length=130, min_length=30) -> str:
    if not text.strip():
        return "[No text to summarize]"

    chunks = chunk_text(text)
    first_level_summaries = []

    for chunk in chunks:
        summary = summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)
        first_level_summaries.append(summary[0]["summary_text"])

    combined_summary = " ".join(first_level_summaries)
    final_summary = summarizer(combined_summary, max_length=max_length, min_length=min_length, do_sample=False)[0]["summary_text"]

    return final_summary

def extract_keywords_spacy(text: str, top_n: int = 10) -> list:
    doc = nlp(text)
    raw_chunks = [chunk.text.strip() for chunk in doc.noun_chunks]
    filtered = []
    for ch in raw_chunks:
        if len(ch) < 3:
            continue
        ch_doc = nlp(ch)
        if all(token.is_stop or token.pos_ == "PRON" for token in ch_doc):
            continue
        filtered.append(ch)

    freq = {}
    for kw in filtered:
        freq[kw] = freq.get(kw, 0) + 1

    sorted_kws = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [kw for kw, _ in sorted_kws[:top_n]]

def highlight_keywords(text: str, keywords: list, color="#0000FF") -> str:
    for kw in keywords:
        pattern = re.compile(r"\b({})\b".format(re.escape(kw)), re.IGNORECASE)
        text = pattern.sub(rf"[color={color}]\1[/color]", text)
    return text

def get_wiki_summary(keyword: str) -> str:
    try:
        summary = wikipedia.summary(keyword, sentences=1)
        return summary
    except Exception:
        return ""
