from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

class OllamaChatbot:
    def __init__(self, base_url, model):
        self.base_url = base_url
        self.model = model
        self.chat_history = []
        self.system_prompt = ""
        self.keep_alive = "10m"

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
    chatbot = OllamaChatbot(base_url, model)
    response = chatbot.chat(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
