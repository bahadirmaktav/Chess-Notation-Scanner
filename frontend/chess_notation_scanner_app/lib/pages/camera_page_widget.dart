import 'package:camera/camera.dart';
import 'package:chess_notation_scanner_app/pages/image_page_widget.dart';
import 'package:flutter/material.dart';
import 'package:flutterflow_ui/flutterflow_ui.dart';

import '../main.dart';
import 'camera_page_model.dart';

export 'camera_page_model.dart';

class CameraPageWidget extends StatefulWidget {
  const CameraPageWidget({super.key});

  @override
  State<CameraPageWidget> createState() => _CameraPageWidgetState();
}

class _CameraPageWidgetState extends State<CameraPageWidget> {
  late CameraPageModel _model;
  late CameraController _controller;
  late double _selectionBoxHeight;
  late double _selectionBoxWidth;
  final double _selectionBoxWidthRatio = 0.7;
  final double _selectionBoxRatio = 1.5;
  final scaffoldKey = GlobalKey<ScaffoldState>();

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => CameraPageModel());
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
  void dispose() {
    _model.dispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    _selectionBoxWidth =
        MediaQuery.of(context).size.width * _selectionBoxWidthRatio;
    _selectionBoxHeight = _selectionBoxWidth * _selectionBoxRatio;
    print("screen width ${MediaQuery.of(context).size.width}");
    print("screen height ${MediaQuery.of(context).size.height}");
    return GestureDetector(
      onTap: () => _model.unfocusNode.canRequestFocus
          ? FocusScope.of(context).requestFocus(_model.unfocusNode)
          : FocusScope.of(context).unfocus(),
      child: Scaffold(
        key: scaffoldKey,
        backgroundColor: FlutterFlowTheme.of(context).primaryBackground,
        appBar: AppBar(
            backgroundColor: const Color(0xBE0A0A0A),
            iconTheme: const IconThemeData(color: Colors.white)),
        body: SafeArea(
          top: true,
          child: Stack(
            children: [
              SizedBox(
                height: double.infinity,
                child: CameraPreview(_controller),
              ),
              Align(
                alignment: const AlignmentDirectional(0.0, 1.2),
                child: Container(
                  width: MediaQuery.sizeOf(context).width * 1.0,
                  height: MediaQuery.sizeOf(context).height * 0.25,
                  decoration: const BoxDecoration(
                    color: Color(0xBE0A0A0A),
                  ),
                ),
              ),
              Align(
                alignment: const AlignmentDirectional(0.0, 0.8),
                child: FlutterFlowIconButton(
                  borderColor: FlutterFlowTheme.of(context).primaryBackground,
                  borderRadius: 20.0,
                  borderWidth: 1.0,
                  buttonSize: 50.0,
                  fillColor: FlutterFlowTheme.of(context).primaryBackground,
                  icon: Icon(
                    Icons.photo_camera_outlined,
                    color: FlutterFlowTheme.of(context).primaryText,
                    size: 24.0,
                  ),
                  onPressed: () async {
                    if (!_controller.value.isInitialized ||
                        _controller.value.isTakingPicture) {
                      return;
                    }
                    try {
                      await _controller.setFlashMode(FlashMode.auto);
                      XFile file = await _controller.takePicture();
                      print(file.path);
                      Navigator.push(
                          context,
                          MaterialPageRoute(
                              builder: (context) => ImagePageWidget(file,
                                  _selectionBoxHeight, _selectionBoxWidth)));
                    } on CameraException catch (e) {
                      debugPrint("Error occured while taking picture : $e");
                      return;
                    }
                  },
                ),
              ),
              Align(
                alignment: const AlignmentDirectional(0.0, 0.0),
                child: Container(
                  width: _selectionBoxWidth,
                  height: _selectionBoxHeight,
                  decoration: BoxDecoration(
                    color: const Color(0x00FFFFFF),
                    border: Border.all(
                      color: FlutterFlowTheme.of(context).primaryText,
                      width: 2.0,
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
