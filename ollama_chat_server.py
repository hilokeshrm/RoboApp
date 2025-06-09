from flask import Flask, render_template, request, jsonify, Response
import requests
import json
import socket
import logging
from datetime import datetime
import sys

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('ollama_chat_server.log')
    ]
)
logger = logging.getLogger(__name__)

# Ollama API endpoint
OLLAMA_URL = "http://localhost:11434/api/generate"

def log_request_details(endpoint, client_ip, user_agent, data=None):
    """Log detailed request information"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{'='*60}")
    print(f"🔵 INCOMING REQUEST - {timestamp}")
    print(f"{'='*60}")
    print(f"📍 Endpoint: {endpoint}")
    print(f"🌐 Client IP: {client_ip}")
    print(f"🖥️  User Agent: {user_agent}")
    if data:
        print(f"📨 Request Data: {json.dumps(data, indent=2)}")
    print(f"{'='*60}\n")
    
    logger.info(f"Request to {endpoint} from {client_ip}")

def log_response_details(endpoint, status_code, response_data=None, is_stream=False):
    """Log detailed response information"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{'='*60}")
    print(f"🔴 OUTGOING RESPONSE - {timestamp}")
    print(f"{'='*60}")
    print(f"📍 Endpoint: {endpoint}")
    print(f"📊 Status Code: {status_code}")
    if is_stream:
        print(f"🔄 Response Type: STREAMING")
    else:
        print(f"📤 Response Type: REGULAR")
        if response_data:
            # Truncate long responses for display
            if isinstance(response_data, dict) and 'response' in response_data:
                content = response_data['response']
                if len(content) > 200:
                    display_content = content[:200] + "...[truncated]"
                else:
                    display_content = content
                print(f"💬 AI Response: {display_content}")
            else:
                print(f"📤 Response Data: {json.dumps(response_data, indent=2)}")
    print(f"{'='*60}\n")
    
    logger.info(f"Response from {endpoint} - Status: {status_code}")

def log_ollama_communication(prompt, response_preview=None, is_stream=False):
    """Log communication with Ollama"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{'~'*60}")
    print(f"🤖 OLLAMA COMMUNICATION - {timestamp}")
    print(f"{'~'*60}")
    print(f"➡️  SENDING TO OLLAMA:")
    print(f"   Model: llama3.2")
    print(f"   Stream: {is_stream}")
    print(f"   Prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")
    
    if response_preview and not is_stream:
        print(f"⬅️  RECEIVED FROM OLLAMA:")
        preview = response_preview[:150] + "..." if len(response_preview) > 150 else response_preview
        print(f"   Response: {preview}")
    elif is_stream:
        print(f"⬅️  STREAMING FROM OLLAMA: [Real-time streaming active]")
    
    print(f"{'~'*60}\n")
    
    logger.info(f"Ollama communication - Prompt length: {len(prompt)}, Stream: {is_stream}")

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
    # Log web interface access
    log_request_details(
        endpoint='/',
        client_ip=request.remote_addr,
        user_agent=request.headers.get('User-Agent', 'Unknown')
    )
    return render_template('chat.html')

@app.route('/status', methods=['GET'])
def server_status():
    """Server status endpoint for debugging"""
    log_request_details(
        endpoint='/status',
        client_ip=request.remote_addr,
        user_agent=request.headers.get('User-Agent', 'Unknown')
    )
    
    status_info = {
        'server': 'Ollama Chat Server',
        'status': 'running',
        'timestamp': datetime.now().isoformat(),
        'ollama_url': OLLAMA_URL,
        'local_ip': get_local_ip()
    }
    
    log_response_details('/status', 200, status_info)
    return jsonify(status_info)

@app.route('/chat', methods=['POST'])
def chat():
    # Log incoming request details
    log_request_details(
        endpoint='/chat',
        client_ip=request.remote_addr,
        user_agent=request.headers.get('User-Agent', 'Unknown'),
        data=request.json
    )
    
    user_message = request.json.get('message', '')
    
    if not user_message:
        error_response = {'error': 'No message provided'}
        log_response_details('/chat', 400, error_response)
        return jsonify(error_response), 400
    
    # Log communication with Ollama
    log_ollama_communication(user_message, is_stream=False)
    
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
            
            # Log Ollama response preview
            log_ollama_communication(user_message, ai_response, is_stream=False)
            
            response_data = {'response': ai_response}
            log_response_details('/chat', 200, response_data)
            return jsonify(response_data)
        else:
            error_response = {'error': f'Ollama API error: {response.status_code}'}
            log_response_details('/chat', 500, error_response)
            return jsonify(error_response), 500
            
    except requests.exceptions.RequestException as e:
        error_response = {'error': f'Connection error: {str(e)}'}
        log_response_details('/chat', 500, error_response)
        return jsonify(error_response), 500

@app.route('/stream_chat', methods=['POST'])
def stream_chat():
    """Streaming endpoint for real-time responses"""
    # Log incoming streaming request details
    log_request_details(
        endpoint='/stream_chat',
        client_ip=request.remote_addr,
        user_agent=request.headers.get('User-Agent', 'Unknown'),
        data=request.json
    )
    
    user_message = request.json.get('message', '')
    
    if not user_message:
        error_response = {'error': 'No message provided'}
        log_response_details('/stream_chat', 400, error_response)
        return jsonify(error_response), 400
    
    # Log streaming communication with Ollama
    log_ollama_communication(user_message, is_stream=True)
    
    def generate():
        payload = {
            "model": "llama3.2",
            "prompt": user_message,
            "stream": True
        }
        
        token_count = 0
        accumulated_response = ""
        
        try:
            response = requests.post(OLLAMA_URL, json=payload, stream=True, timeout=60)
            
            if response.status_code == 200:
                print(f"\n🔄 STARTING STREAM for prompt: {user_message[:50]}...")
                
                for line in response.iter_lines():
                    if line:
                        try:
                            data = json.loads(line.decode('utf-8'))
                            if 'response' in data:
                                token = data['response']
                                token_count += 1
                                accumulated_response += token
                                
                                # Log every 10 tokens or if it's a significant token
                                if token_count % 10 == 0 or len(token.strip()) > 1:
                                    print(f"🔄 Stream token #{token_count}: '{token}' | Accumulated length: {len(accumulated_response)}")
                                
                                yield f"data: {json.dumps({'token': token})}\n\n"
                                
                            if data.get('done', False):
                                print(f"\n✅ STREAM COMPLETED")
                                print(f"📊 Total tokens sent: {token_count}")
                                print(f"📏 Total response length: {len(accumulated_response)}")
                                print(f"📝 Final response preview: {accumulated_response[:100]}...\n")
                                
                                log_response_details('/stream_chat', 200, None, is_stream=True)
                                yield f"data: {json.dumps({'done': True})}\n\n"
                                break
                        except json.JSONDecodeError:
                            continue
            else:
                error_msg = f'Ollama API error: {response.status_code}'
                print(f"❌ STREAM ERROR: {error_msg}")
                log_response_details('/stream_chat', 500, {'error': error_msg}, is_stream=True)
                yield f"data: {json.dumps({'error': error_msg})}\n\n"
                
        except requests.exceptions.RequestException as e:
            error_msg = f'Connection error: {str(e)}'
            print(f"❌ STREAM CONNECTION ERROR: {error_msg}")
            log_response_details('/stream_chat', 500, {'error': error_msg}, is_stream=True)
            yield f"data: {json.dumps({'error': error_msg})}\n\n"
    
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    local_ip = get_local_ip()
    port = 5000
    
    print(f"\n{'='*50}")
    print(f"🚀 OLLAMA CHAT SERVER WITH DETAILED LOGGING")
    print(f"{'='*50}")
    print(f"🌐 Server URL: http://{local_ip}:{port}")
    print(f"📱 Mobile Access: http://{local_ip}:{port}")
    print(f"📊 Status Endpoint: http://{local_ip}:{port}/status")
    print(f"📝 Log File: ollama_chat_server.log")
    print(f"🔍 Detailed logging: ENABLED")
    print(f"{'='*50}")
    print(f"📋 Available Endpoints:")
    print(f"   GET  /          - Web interface")
    print(f"   GET  /status    - Server status")
    print(f"   POST /chat      - Regular chat")
    print(f"   POST /stream_chat - Streaming chat")
    print(f"{'='*50}")
    print(f"⚠️  Make sure:")
    print(f"   • Ollama is running on localhost:11434")
    print(f"   • Your device is on the same WiFi network")
    print(f"   • Firewall allows connections on port {port}")
    print(f"{'='*50}\n")
    
    # Log server startup
    logger.info(f"Server starting on {local_ip}:{port}")
    
    # Run the Flask app accessible from any IP on the network
    app.run(host='0.0.0.0', port=port, debug=True)

