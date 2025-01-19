from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv
import markdown2

load_dotenv()

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

TOPICS = {
    'python': ['Basic Syntax', 'Data Types', 'Functions', 'OOP'],
    'javascript': ['Variables', 'Functions', 'DOM', 'Async Programming'],
    'machine_learning': ['Supervised Learning', 'Unsupervised Learning', 'Neural Networks']
}

@app.route('/')
def index():
    return render_template('index.html', topics=TOPICS)

@app.route('/learn/<topic>/<subtopic>')
def learn(topic, subtopic):
    # Generate content using Gemini
    prompt = f"Explain {subtopic} in {topic} with simple examples. Use markdown formatting."
    response = model.generate_content(prompt)
    content = markdown2.markdown(response.text)

    # Generate quiz questions
    quiz_prompt = f"Generate 2 multiple choice questions about {subtopic} in {topic}. Use markdown formatting."
    quiz_response = model.generate_content(quiz_prompt)
    quiz = markdown2.markdown(quiz_response.text)

    return render_template('learn.html', content=content, quiz=quiz, topic=topic, subtopic=subtopic)

@app.route('/ask', methods=['POST'])
def ask_question():
    question = request.json.get('question')
    response = model.generate_content(question)
    return jsonify({'answer': markdown2.markdown(response.text)})

if __name__ == '__main__':
    app.run(debug=True)
