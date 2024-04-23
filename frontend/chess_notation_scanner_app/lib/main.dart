import 'package:camera/camera.dart';
import 'package:chess_notation_scanner_app/pages/navbar_page_widget.dart';
import 'package:flutter/material.dart';

// TODO(MBM): Define camera declarations and initialization in camera page.
late List<CameraDescription> cameras;

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  cameras = await availableCameras();
  runApp(const ChessNotationScannerApp());
}

class ChessNotationScannerApp extends StatelessWidget {
  const ChessNotationScannerApp({super.key});
  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      title: 'Chess Notation Scanner',
      home: NavbarPageWidget(),
    );
  }
}
