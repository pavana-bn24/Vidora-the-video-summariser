from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from collections import Counter
from urllib.parse import urlparse, parse_qs
import yt_dlp
import re

app = Flask(__name__)
CORS(app)

def clean_url(url):
    if "youtu.be" in url:
        return url.split("?")[0]
    elif "youtube.com" in url:
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        video_id = query.get("v", [None])[0]
        if video_id:
            return f"https://www.youtube.com/watch?v={video_id}"
    return url

def get_video_info(video_url):
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        return {
            'title': info.get('title'),
            'channel': info.get('uploader'),
            'publish_date': info.get('upload_date'),
            'views': info.get('view_count'),
            'length_sec': info.get('duration'),
            'description': info.get('description')
        }

def get_transcript(video_url):
    video_id = video_url.split("v=")[-1] if "v=" in video_url else video_url.split("/")[-1]
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([t['text'] for t in transcript])
    except TranscriptsDisabled:
        return None

def basic_summary(text, num_keywords=10, num_sentences=5):
    if not text:
        return {
            'keywords': [],
            'summary_sentences': ["Transcript not available."]
        }
    words = re.findall(r'\w+', text.lower())
    word_freq = Counter(words)
    common_words = [word for word, _ in word_freq.most_common(num_keywords)]
    sentences = re.split(r'(?<=[.!?]) +', text)
    selected_sentences = []
    for sentence in sentences:
        if any(keyword in sentence.lower() for keyword in common_words):
            selected_sentences.append(sentence.strip())
        if len(selected_sentences) >= num_sentences:
            break
    return {
        'keywords': common_words,
        'summary_sentences': selected_sentences
    }

@app.route('/api/summary', methods=['POST'])
def summarize():
    data = request.get_json()
    video_url = clean_url(data.get('url'))
    try:
        transcript = get_transcript(video_url)
        summary = basic_summary(transcript)
        return jsonify({
            'summary': "<ul>" + ''.join(f"<li>{s}</li>" for s in summary['summary_sentences']) + "</ul>",
            'keywords': summary['keywords']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
