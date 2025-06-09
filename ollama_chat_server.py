from flask import Flask, render_template, request, jsonify, Response
import requests
import json
import socket

app = Flask(__name__)

# Ollama API endpoint
OLLAMA_URL = "http://localhost:11434/api/generate"

def get_local_ip():
    """Get the local IP address of this machine"""
    try:
        # Connect to a remote server to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "localhost"

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    # Prepare the request to Ollama
    payload = {
        "model": "llama3.2",
        "prompt": user_message,
        "stream": False
    }
    
    try:
        # Send request to Ollama
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result.get('response', 'No response from AI')
            return jsonify({'response': ai_response})
        else:
            return jsonify({'error': f'Ollama API error: {response.status_code}'}), 500
            
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Connection error: {str(e)}'}), 500

@app.route('/stream_chat', methods=['POST'])
def stream_chat():
    """Streaming endpoint for real-time responses"""
    user_message = request.json.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    def generate():
        payload = {
            "model": "llama3.2",
            "prompt": user_message,
            "stream": True
        }
        
        try:
            response = requests.post(OLLAMA_URL, json=payload, stream=True, timeout=60)
            
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        try:
                            data = json.loads(line.decode('utf-8'))
                            if 'response' in data:
                                yield f"data: {json.dumps({'token': data['response']})}\n\n"
                            if data.get('done', False):
                                yield f"data: {json.dumps({'done': True})}\n\n"
                                break
                        except json.JSONDecodeError:
                            continue
            else:
                yield f"data: {json.dumps({'error': f'Ollama API error: {response.status_code}'})}\n\n"
                
        except requests.exceptions.RequestException as e:
            yield f"data: {json.dumps({'error': f'Connection error: {str(e)}'})}\n\n"
    
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    local_ip = get_local_ip()
    port = 5000
    
    print(f"\n=== Ollama Chat Server ===")
    print(f"Server starting on: http://{local_ip}:{port}")
    print(f"Access from your phone: http://{local_ip}:{port}")
    print(f"Make sure your phone is connected to the same WiFi network!")
    print(f"========================\n")
    
    # Run the Flask app accessible from any IP on the network
    app.run(host='0.0.0.0', port=port, debug=True)

