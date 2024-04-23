import 'dart:io';
import 'dart:typed_data';
import 'package:image/image.dart';

class ImageProcessManager {
  Future<Uint8List> cutOutImage(
      String imageFilePath, int height, int width) async {
    // Convert image path to File
    File file = File(imageFilePath);

    // Decode the image
    Image image = decodeImage(await file.readAsBytes())!;

    print("width ${width}");
    print("height ${height}");

    print("image.width ${image.width}");
    print("image.width ${image.height}");

    // Define the rectangle to cut out
    int x = (image.width - width) ~/ 2; // x of top-left
    int y = (image.height - height) ~/ 2; // y of top-left

    print("x ${x}");
    print("y ${y}");

    // Cut out the specified rectangle
    Image cutOutImage =
        copyCrop(image, x: x, y: y, width: width, height: height);

    // Convert the image back to bytes
    Uint8List cutOutBytes = Uint8List.fromList(encodePng(cutOutImage));

    return cutOutBytes;
  }
}
