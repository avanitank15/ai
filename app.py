from flask import Flask, render_template, request, jsonify
from chatbot_engine import EcoBot
import uuid

app = Flask(__name__)
bot = EcoBot()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    user_id = request.json.get("user_id")
    
    # Generate a temporary ID if none exists
    if not user_id:
        user_id = str(uuid.uuid4())

    response_text = bot.process_message(user_id, user_input)
    
    return jsonify({"response": response_text, "user_id": user_id})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
