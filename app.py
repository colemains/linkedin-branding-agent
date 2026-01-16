import gradio as gr  # pyright: ignore[reportMissingImports]
import joblib  # pyright: ignore[reportMissingImports]
import re
from urllib.parse import urlparse

model = joblib.load('url_model.pkl')

def extract_features(url):
    # Add scheme if missing for proper parsing
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    features = {}
    features['length'] = len(url)
    features['dots'] = url.count('.')
    features['https'] = 1 if url.startswith('https') else 0
    try:
        parsed = urlparse(url)
        features['ip'] = 1 if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', parsed.netloc) else 0
    except:
        features['ip'] = 0
    features['at'] = 1 if '@' in url else 0
    features['hyphens'] = url.count('-')
    return [list(features.values())]

def predict(url):
    feats = extract_features(url)
    pred = model.predict(feats)[0]
    return "Phishing Detected! 🚨" if pred == 1 else "Safe URL ✅"

iface = gr.Interface(fn=predict, inputs="text", outputs="text", title="AI Phishing URL Detector")
iface.launch(share=False, server_name="127.0.0.1", server_port=7860)