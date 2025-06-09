# 🦙 Ollama Chat Server

A simple, mobile-friendly web interface to chat with Ollama's Llama 3.2 model from any device on your local network.

![Ollama Chat Server](https://img.shields.io/badge/Ollama-Chat%20Server-blue?style=for-the-badge&logo=llama)
![Python](https://img.shields.io/badge/Python-3.10+-green?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20Server-red?style=for-the-badge&logo=flask)

## ✨ Features

- 💬 **Real-time Chat**: Instant communication with Llama 3.2
- 📱 **Mobile Optimized**: Beautiful, responsive design for phones and tablets
- 🌐 **Network Access**: Access from any device on the same WiFi network
- ⚡ **Fast Responses**: Efficient communication with Ollama API
- 🎨 **Modern UI**: Clean, intuitive chat interface
- 🔄 **Error Handling**: Robust error handling and retry mechanisms
- 🖥️ **Cross-Platform**: Works on Windows, macOS, and Linux

## 🚀 Quick Start

### Prerequisites

1. **Ollama installed and running**
   ```bash
   # Install Ollama (if not already installed)
   # Visit: https://ollama.ai/download
   
   # Pull Llama 3.2 model
   ollama pull llama3.2
   
   # Verify Ollama is running
   ollama list
   ```

2. **Python 3.10 or higher**
   ```bash
   python --version
   ```

### Installation

1. **Clone or download this project**
   ```bash
   git clone <your-repo-url>
   cd ollama-chat-server
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install manually:
   ```bash
   pip install flask requests
   ```

3. **Start the server**
   ```bash
   python ollama_chat_server.py
   ```

4. **Access from your devices**
   - The server will display the local IP address when it starts
   - Open your browser and go to: `http://YOUR_LOCAL_IP:5000`
   - Example: `http://192.168.1.100:5000`

## 📱 Mobile Access

### Steps to access from your phone:

1. **Ensure same network**: Make sure your phone is connected to the same WiFi network as your computer
2. **Note the IP address**: When you start the server, it will display something like:
   ```
   === Ollama Chat Server ===
   Server starting on: http://192.168.1.100:5000
   Access from your phone: http://192.168.1.100:5000
   ========================
   ```
3. **Open browser on phone**: Navigate to the displayed URL
4. **Start chatting**: Begin your conversation with Llama 3.2!

## 📁 Project Structure

```
ollama-chat-server/
├── ollama_chat_server.py    # Main Flask server
├── templates/
│   └── chat.html           # Mobile-optimized chat interface
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🔧 Configuration

### Changing the Model

To use a different Ollama model, edit `ollama_chat_server.py`:

```python
# Change this line (around line 36)
payload = {
    "model": "llama3.2",  # Change to your preferred model
    "prompt": user_message,
    "stream": False
}
```

### Changing the Port

To use a different port, edit the last section of `ollama_chat_server.py`:

```python
if __name__ == '__main__':
    local_ip = get_local_ip()
    port = 5000  # Change this to your preferred port
    # ...
```

## 🛠️ API Endpoints

- `GET /` - Serves the chat interface
- `POST /chat` - Sends messages to Ollama and returns responses
- `POST /stream_chat` - Streaming endpoint for real-time responses (future feature)

## 🔒 Security Considerations

⚠️ **Important**: This server is designed for local network use only.

- The server runs in debug mode for development
- No authentication or encryption is implemented
- Only use on trusted local networks
- Do not expose to the internet without proper security measures

## 📋 Requirements

- Python 3.10+
- Flask 2.3.3+
- Requests 2.31.0+
- Ollama running locally
- Llama 3.2 model downloaded

## 🐛 Troubleshooting

### Common Issues

1. **"Connection error" messages**
   - Ensure Ollama is running: `ollama list`
   - Check if Llama 3.2 is available: `ollama pull llama3.2`

2. **Can't access from phone**
   - Verify both devices are on the same WiFi network
   - Check if firewall is blocking port 5000
   - Try accessing from computer first: `http://localhost:5000`

3. **"Model not found" error**
   - Pull the model: `ollama pull llama3.2`
   - Check available models: `ollama list`

4. **Server won't start**
   - Check if port 5000 is already in use
   - Ensure Python dependencies are installed
   - Try running with elevated permissions

### Debug Mode

To run with more verbose logging:

```python
# In ollama_chat_server.py, change the last line to:
app.run(host='0.0.0.0', port=port, debug=True)
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Ideas for improvements:
- [ ] User authentication
- [ ] Chat history persistence
- [ ] Multiple model support
- [ ] Real-time streaming responses
- [ ] File upload support
- [ ] Dark/light theme toggle
- [ ] Message export functionality

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) for the amazing local LLM platform
- [Flask](https://flask.palletsprojects.com/) for the lightweight web framework
- [Meta](https://ai.meta.com/llama/) for the Llama model

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review [Ollama documentation](https://github.com/ollama/ollama)
3. Open an issue in this repository

---

**Happy Chatting with Llama 3.2!** 🦙💬

