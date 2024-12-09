from flask import Flask, request, jsonify
import google.generativeai as genai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
genai.configure(api_key="AIzaSyChLjkBs-o6xYRPkfShcYZ1e6UNM_oc2EM")

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-8b",
    system_instruction="You are Youssef, a virtual culinary assistant specializing in moroccan recipe recommendations. Your mission is to help users find recipes based on the ingredients they have available. When a user provides a list of ingredients, analyze them and suggest up to three recipes that match, considering possible ingredient combinations. For each recipe, provide: the recipe name, a brief description, and a short list of preparation steps. If no exact match is found, offer creative ideas using similar or complementary ingredients. Always respond in a friendly and engaging manner. Your goal is to make the user experience simple, helpful, and enjoyable."
)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = model.generate_content(contents=user_input)
    return jsonify({'response': response.text})

if __name__ == '__main__':
    app.run(debug=True)
