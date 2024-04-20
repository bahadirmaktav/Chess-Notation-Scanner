import 'package:flutter/material.dart';
import 'package:chess_notation_scanner_app/pages/home_page.dart';

void main() {
  runApp(const ChessNotationScannerApp());
}

class ChessNotationScannerApp extends StatelessWidget {
  const ChessNotationScannerApp({super.key});
  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      title: 'Chess Notation Scanner',
      home: MyHomePage(title: 'Flutter Demo Home Page'),
    );
  }
}
