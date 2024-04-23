import 'dart:io';

import 'package:camera/camera.dart';
import 'package:flutter/material.dart';

class ImagePage extends StatefulWidget {
  const ImagePage(this.file, {super.key});
  final XFile file;
  @override
  State<ImagePage> createState() => _ImagePageState();
}

class _ImagePageState extends State<ImagePage> {
  @override
  Widget build(BuildContext context) {
    File picture = File(widget.file.path);
    return Scaffold(
      appBar: AppBar(title: const Text('Image Preview')),
      body: Stack(children: [
        Center(
          child: Image.file(picture),
        ),
        Center(
          child: CustomPaint(painter: OverlayPainter(), size: Size(1080, 1920)),
        )
      ]),
    );
  }
}

class OverlayPainter extends CustomPainter {
  Color overlayColor;
  Color borderColor;
  Size _size = const Size(0, 0);

  Size get size => _size;
  Rect holeRect;
  double cornerRadius;

  OverlayPainter({
    this.cornerRadius = 5,
    this.holeRect = const Rect.fromLTRB(200, 200, 500, 500),
    this.overlayColor = const Color(0x88000000),
    this.borderColor = const Color(0xFFFF5555),
  });

  @override
  void paint(Canvas canvas, Size size) {
    _size = size;
    var paint = Paint()..color = overlayColor;

    var path = Path()
      ..moveTo(0, 0)
      ..lineTo(size.width, 0)
      ..lineTo(size.width, size.height)
      ..lineTo(0, size.height)
      ..lineTo(0, 0)

      /// Hole rectangle
      ..moveTo(holeRect.left, holeRect.top + cornerRadius)
      ..lineTo(holeRect.left, holeRect.height - cornerRadius)
      // Curved left-bottom corner
      ..quadraticBezierTo(holeRect.left, holeRect.height,
          holeRect.left + cornerRadius, holeRect.height)
      ..lineTo(holeRect.width - (cornerRadius), holeRect.height)
      // Curved right bottom corner
      ..quadraticBezierTo(holeRect.width, holeRect.height, holeRect.width,
          holeRect.height - cornerRadius)
      ..lineTo(holeRect.width, holeRect.top + cornerRadius)
      // Curved right top corner
      ..quadraticBezierTo(holeRect.width, holeRect.top,
          holeRect.width - cornerRadius, holeRect.top)
      ..lineTo(holeRect.left + cornerRadius, holeRect.top)
      // Curved left top corner
      ..quadraticBezierTo(holeRect.left, holeRect.top, holeRect.left,
          holeRect.top + cornerRadius)
      ..close();

    canvas.drawPath(path, paint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) {
    // TODO: implement shouldRepaint
    throw UnimplementedError();
  }
}
