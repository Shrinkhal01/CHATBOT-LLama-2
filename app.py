from flask import Flask, render_template, request, jsonify
import requests
import json
import os

app = Flask(__name__, static_folder='static')

class OllamaChatbot:
    def __init__(self, base_url, model, history_file):
        self.base_url = base_url
        self.model = model
        self.chat_history = []
        self.system_prompt = ""
        self.keep_alive = "10m"
        self.history_file = history_file
        self.load_history()

    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as file:
                self.chat_history = json.load(file)
        else:
            self.chat_history = []

    def save_history(self):
        with open(self.history_file, 'w') as file:
            json.dump(self.chat_history, file)

    def generate_completion(self, prompt, system_message="", stream=True):
        headers = {"Content-Type": "application/json"}
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": stream,
            "system": system_message,
            "keep_alive": self.keep_alive
        }
        response = requests.post(f"{self.base_url}/api/generate", headers=headers, data=json.dumps(data), stream=stream)
        
        if stream:
            full_response = ""
            for line in response.iter_lines():
                if line:
                    try:
                        response_part = json.loads(line.decode('utf-8'))['response']
                        full_response += response_part
                        yield response_part
                    except (json.JSONDecodeError, KeyError) as e:
                        print(f"\nError parsing response: {e}")
                        return
            yield full_response
        else:
            try:
                return response.json()['response']
            except (json.JSONDecodeError, KeyError) as e:
                print(f"\nError parsing response: {e}")
                return ""

    def chat(self, user_input):
        self.chat_history.append({"role": "user", "content": user_input})
        prompt = "\n".join([f"{entry['role']}: {entry['content']}" for entry in self.chat_history])
        try:
            full_message = ""
            for message in self.generate_completion(prompt, self.system_prompt):
                full_message += message
            self.chat_history.append({"role": "bot", "content": full_message})
            self.save_history()
            return full_message
        except requests.exceptions.RequestException as e:
            print(f"\nError: {e}")
            return "Error: Failed to generate response."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def handle_chat():
    user_input = request.form['user_input']
    base_url = "http://localhost:11434"
    model = "llama2:latest"
    history_file = 'nfs/chat_history.txt'
    chatbot = OllamaChatbot(base_url, model, history_file)
    response = chatbot.chat(user_input)
    return jsonify({'response': response})

@app.route('/history', methods=['GET'])
def get_history():
    history_file = 'nfs/chat_history.txt'
    if os.path.exists(history_file):
        with open(history_file, 'r') as file:
            chat_history = json.load(file)
        chat_history_display = [f"{entry['role']}: {entry['content']}" for entry in chat_history]
        return jsonify(chat_history_display)
    return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)