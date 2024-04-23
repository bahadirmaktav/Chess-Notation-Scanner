import 'dart:io';
import 'dart:typed_data';

import 'package:camera/camera.dart';
import 'package:chess_notation_scanner_app/utils/image_process_manager.dart';
import 'package:flutter/material.dart';

class ImagePageWidget extends StatefulWidget {
  const ImagePageWidget(this.file, this.cutImageHeight, this.cutImageWidth,
      {super.key});
  final XFile file;
  final double cutImageHeight;
  final double cutImageWidth;

  @override
  State<ImagePageWidget> createState() => _ImagePageWidgetState();
}

class _ImagePageWidgetState extends State<ImagePageWidget> {
  late ImageProcessManager imageProcessManager = ImageProcessManager();

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<Uint8List>(
      future: imageProcessManager.cutOutImage(widget.file.path,
          widget.cutImageHeight.toInt(), widget.cutImageWidth.toInt()),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const CircularProgressIndicator();
        } else if (snapshot.hasError) {
          return Text('Error: ${snapshot.error}');
        } else {
          return Scaffold(
            appBar: AppBar(title: const Text('Image Preview')),
            body: Stack(children: [
              Center(child: Image.memory(snapshot.data!)),
            ]),
          );
        }
      },
    );
  }
}
