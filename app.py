from flask import Flask, render_template, request, jsonify#these libraries are used to create the web application
import requests#this is used to send requests to the llama server
import json#this is used to parse the response from the llama server
import os#os is used to check for filesystem permissions location

app = Flask(__name__)
#this is used to create the web application :)

class OllamaChatbot:
    def __init__(self, base_url, model):
        self.base_url = base_url
        self.model = model
        self.chat_history = self.load_chat_history()
        self.system_prompt = ""
        self.keep_alive = "10m"
    #the init function is used to initialize the chatbot with the base url, model, chat history, system prompt, and keep alive time


    def load_chat_history(self):
        if os.path.exists("chat_history.json"):
            with open("chat_history.json", "r") as file:
                return json.load(file)
        return []
    #the load_chat_history function is used to load the chat history from the chat_history.json file


    def save_chat_history(self):
        with open("chat_history.json", "w") as file:
            json.dump(self.chat_history, file)
    #the save_chat_history function is used to save the chat history to the chat_history.json file


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
        else:
            try:
                return response.json()['response']
            except (json.JSONDecodeError, KeyError) as e:
                print(f"\nError parsing response: {e}")
                return ""
    #the generate_completion function is used to generate a completion from the llama server using the prompt, system message, and keep alive time


    def chat(self, user_input):
        self.chat_history.append({"role": "user", "content": user_input})
        prompt = "\n".join([f"{entry['role']}: {entry['content']}" for entry in self.chat_history])
        try:
            full_message = ""
            for message in self.generate_completion(prompt, self.system_prompt):#generates completion
                full_message += message
            self.chat_history.append({"role": "bot", "content": full_message})#appends completion to chat history
            self.save_chat_history()
            return full_message
        except requests.exceptions.RequestException as e:#checks if there is an error
            print(f"\nError: {e}")
            return "Error: Failed to generate response."
    #the chat function is used to handle the chat functionality of the chatbot, including user input, generating responses, and saving chat history


@app.route('/')
def index():
    base_url = "http://localhost:11434"
    model = "llama2:latest"
    chatbot = OllamaChatbot(base_url, model)
    chat_history = chatbot.chat_history
    return render_template('index.html', chat_history=chat_history)
#the index method is used to render the index.html file and display the chat history

@app.route('/chat', methods=['POST'])
def handle_chat():
    user_input = request.form['user_input']
    base_url = "http://localhost:11434"
    model = "llama2:latest"
    chatbot = OllamaChatbot(base_url, model)
    response = chatbot.chat(user_input)
    return jsonify({'response': response})
#the handle_chat method is used to handle the chat functionality of the chatbot, including user input and generating responses


if __name__ == '__main__':
    app.run(debug=True)
#this condition is used to run the web application if the app.py file is executed directly
