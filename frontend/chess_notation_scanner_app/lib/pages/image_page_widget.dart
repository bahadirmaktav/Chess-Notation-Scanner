import 'dart:io';

import 'package:camera/camera.dart';
import 'package:flutter/material.dart';

class ImagePageWidget extends StatefulWidget {
  const ImagePageWidget(this.file, {super.key});
  final XFile file;
  @override
  State<ImagePageWidget> createState() => _ImagePageWidgetState();
}

class _ImagePageWidgetState extends State<ImagePageWidget> {
  @override
  Widget build(BuildContext context) {
    File picture = File(widget.file.path);
    return Scaffold(
      appBar: AppBar(title: const Text('Image Preview')),
      body: Stack(children: [
        Center(
          child: Image.file(picture),
        ),
      ]),
    );
  }
}
