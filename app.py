from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

LANGUAGES = {
    "English": "en",
    "Urdu": "ur",
    "Arabic": "ar",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Italian": "it",
    "Chinese": "zh-CN",
    "Hindi": "hi",
    "Turkish": "tr"
}

API_URL = "https://api.mymemory.translated.net/get"

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", languages=LANGUAGES)

@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    source = data.get("source")
    target = data.get("target")

    if not text:
        return jsonify({"success": False, "error": "Please enter some text."}), 400

    if source not in LANGUAGES or target not in LANGUAGES:
        return jsonify({"success": False, "error": "Please select valid languages."}), 400

    if source == target:
        return jsonify({"success": True, "translation": text})

    try:
        params = {
            "q": text,
            "langpair": f"{LANGUAGES[source]}|{LANGUAGES[target]}"
        }
        response = requests.get(API_URL, params=params, timeout=15)
        response.raise_for_status()
        result = response.json()

        translated = result.get("responseData", {}).get("translatedText")
        if not translated:
            return jsonify({"success": False, "error": "Translation API returned no translation."}), 502

        return jsonify({"success": True, "translation": translated})
    except requests.RequestException as exc:
        return jsonify({
            "success": False,
            "error": f"Could not connect to the translation service: {exc}"
        }), 502

if __name__ == "__main__":
    app.run(debug=True)
