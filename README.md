# Ollama Chatbot

The Ollama Chatbot is an AI-powered web application that facilitates real-time interaction with users. Using the advanced Ollama Llama 2 model, this chatbot is built with Flask for the backend and HTML, CSS, and jQuery for a responsive and user-friendly interface. It supports instant messaging, chat history, and can be customized with additional data to answer specific questions, making it ideal for various applications, including educational support.
To run this deep learning based chatbot you need to download the llama2:latest from the link given below:
[Download llama2:latest](https://ollama.com/library/llama2)

## Features

- Real-time Messaging: Instantaneous chat interaction with the bot.
- Chat History: View and scroll through previous conversations.
- User-friendly Interface: Designed for easy navigation and interaction.
- Responsive Design: Works seamlessly across devices.
- **Chat History Storage:** Stores chat history in `chat_history.json` for persistent conversation history.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/ollama-chatbot.git
   cd ollama-chatbot
Install dependencies:

bash
Copy code
pip install flask requests
Download the Ollama Llama 2 model:

You can download the pre-trained Ollama Llama 2 model from the Ollama GitHub repository.

Run the application:

bash
Copy code
python app.py
Open your web browser:

Navigate to http://localhost:5000 to start using the chatbot.

File Structure
app.py: Backend Flask application handling bot interactions.
templates/index.html: Frontend HTML providing the chat interface.
static/:
artificial-intelligence.png: Bot avatar image.
user.jpg: User avatar image.
chat_history.json: Stores chat history for persistent conversations.
Usage
Sending Messages:
Type your message in the input field and press Enter or click Send to send it.

Viewing Chat History:
Scroll through the chat history displayed on the left side of the interface.

Screenshots
![ss](https://github.com/Shrinkhal01/CHATBOT-LLama-2/assets/97280075/ce4e3afd-8551-499a-a430-b06c832a1712)


License
This project is licensed under the MIT License. See the LICENSE file for details.

Contributing
Feel free to contribute to this project! Fork it and submit a pull request with any improvements or features you'd like to add.

About
This project was developed by Shrinkhal. Contact me at shrinkhalshrinkhal22@gmail.com for any questions or feedback.
