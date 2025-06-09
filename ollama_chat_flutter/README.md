# Ollama Chat Flutter

A Flutter frontend application for chatting with Ollama models via your Flask server.

## Features

- 💬 Real-time chat with Ollama models
- 🔄 Support for both regular and streaming responses
- 📱 Mobile-friendly responsive design
- 💾 Message history persistence
- ⚙️ Configurable server settings
- 🎨 Clean, modern UI similar to your web interface
- 📋 Copy messages to clipboard
- 🗑️ Delete individual messages
- 🔗 Connection status indicator

## Prerequisites

- Flutter SDK installed
- Your Ollama chat server running (the Flask app you already have)
- Device connected to the same network as your server

## Setup

1. **Get dependencies:**
   ```bash
   flutter pub get
   ```

2. **Update server URL:**
   - Open the app and go to Settings
   - Enter your server's IP address and port (e.g., `http://192.168.1.100:5000`)
   - Test the connection

3. **Run the app:**
   ```bash
   flutter run
   ```

## Configuration

### Finding Your Server IP

Your Flask server shows the IP address when it starts. Look for:
```
=== Ollama Chat Server ===
Server starting on: http://192.168.1.100:5000
Access from your phone: http://192.168.1.100:5000
```

Use this URL in the Flutter app settings.

### Default Server URL

The app defaults to `http://192.168.1.100:5000`. You can change this in:
- `lib/services/api_service.dart` (line 6)
- Or through the Settings screen in the app

## API Compatibility

This Flutter app works with your existing Flask server endpoints:
- `POST /chat` - Regular chat messages
- `POST /stream_chat` - Streaming responses
- `GET /` - Connection testing

## Building for Release

### Android APK
```bash
flutter build apk --release
```

### iOS (requires macOS)
```bash
flutter build ios --release
```

## Project Structure

```
lib/
├── main.dart                 # App entry point
├── models/
│   └── message.dart         # Chat message model
├── providers/
│   └── chat_provider.dart   # State management
├── screens/
│   ├── chat_screen.dart     # Main chat interface
│   └── settings_screen.dart # Configuration screen
├── services/
│   └── api_service.dart     # API communication
└── widgets/
    └── message_widget.dart  # Message bubble widget
```

## Usage

1. **Start your Flask server** (the one you already have)
2. **Launch the Flutter app**
3. **Configure the server URL** in Settings if needed
4. **Start chatting** with your Ollama model!

### Features

- **Send messages**: Type and press send or Enter
- **Stream responses**: Toggle in the menu for real-time response streaming
- **Copy messages**: Long press any message to copy
- **Delete messages**: Long press to access delete option
- **Clear chat**: Use the menu or Settings to clear all messages
- **Connection status**: Check the status indicator in the top bar

## Troubleshooting

1. **"Not connected to server"**:
   - Check that your Flask server is running
   - Verify the server URL in Settings
   - Ensure your device is on the same network

2. **"Connection failed"**:
   - Check firewall settings on the server machine
   - Try the server URL in a web browser first

3. **Messages not sending**:
   - Check the connection status indicator
   - Verify Ollama is running on the server

## Network Requirements

- Your phone/device and computer must be on the same WiFi network
- The Flask server must be accessible from other devices on the network
- Default port 5000 should not be blocked by firewall

Enjoy chatting with your Ollama models on mobile! 🚀
