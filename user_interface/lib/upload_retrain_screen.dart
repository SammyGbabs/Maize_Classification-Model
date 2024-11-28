import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';

class UploadRetrainScreen extends StatefulWidget {
  const UploadRetrainScreen({super.key});

  @override
  _UploadRetrainScreenState createState() => _UploadRetrainScreenState();
}

class _UploadRetrainScreenState extends State<UploadRetrainScreen> {
  String? _statusMessage;

  void _uploadFile() async {
    FilePickerResult? result =
        await FilePicker.platform.pickFiles(allowMultiple: false);
    if (result != null) {
      String filePath = result.files.single.path!;
      print("Picked file path: $filePath");

      // Add your upload logic here (e.g., send to server).
    }
  }

  void _retrainModel() {
    setState(() {
      _statusMessage = "Model retrained successfully.";
    });

    // Add your retraining logic here (e.g., API call to retrain the model).
    // Once retraining is complete, display the evaluation message.
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Upload & Retrain")),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            ElevatedButton(
              onPressed: _uploadFile,
              child: const Text("Upload ZIP File for Retraining"),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _retrainModel,
              child: const Text("Retrain Model"),
            ),
            const SizedBox(height: 20),
            if (_statusMessage != null) ...[
              Text(_statusMessage!),
            ],
          ],
        ),
      ),
    );
  }
}
