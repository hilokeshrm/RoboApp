// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility in the flutter_test package. For example, you can send tap and scroll
// gestures. You can also use WidgetTester to find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:ollama_chat_flutter/main.dart';

void main() {
  testWidgets('App starts without crashing', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(const OllamaChatApp());

    // Verify that the app bar is present
    expect(find.text('🦙 Ollama Chat'), findsOneWidget);
    
    // Verify that the welcome message is present
    expect(find.textContaining('Hello! I\'m Llama 3.2'), findsOneWidget);
  });
}
