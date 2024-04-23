import 'package:chess_notation_scanner_app/main.dart';
import 'package:chess_notation_scanner_app/pages/image_page.dart';
import 'package:flutter/material.dart';
import 'package:camera/camera.dart';

class CameraPage extends StatefulWidget {
  const CameraPage({super.key});

  @override
  State<CameraPage> createState() => _CameraPageState();
}

class _CameraPageState extends State<CameraPage> {
  late CameraController _controller;
  @override
  void initState() {
    super.initState();
    _controller = CameraController(cameras[0], ResolutionPreset.max);
    _controller.initialize().then((_) {
      if (!mounted) {
        return;
      }
      setState(() {});
    }).catchError((Object e) {
      if (e is CameraException) {
        switch (e.code) {
          case 'CameraAccessDenied':
            print("Access was denied!");
            break;
          default:
            print(e.description);
            break;
        }
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(children: [
        Container(
          height: double.infinity,
          child: CameraPreview(_controller),
        ),
        Column(
          mainAxisAlignment: MainAxisAlignment.end,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Center(
              child: Container(
                margin: const EdgeInsets.all(20.0),
                child: MaterialButton(
                  onPressed: () async {
                    if (!_controller.value.isInitialized ||
                        _controller.value.isTakingPicture) {
                      return;
                    }
                    try {
                      await _controller.setFlashMode(FlashMode.auto);
                      XFile file = await _controller.takePicture();
                      Navigator.push(
                          context,
                          MaterialPageRoute(
                              builder: (context) => ImagePage(file)));
                    } on CameraException catch (e) {
                      debugPrint("Error occured while taking picture : $e");
                      return;
                    }
                  },
                  color: Colors.white,
                  child: const Text("Take a pciture"),
                ),
              ),
            )
          ],
        )
      ]),
    );
  }
}
