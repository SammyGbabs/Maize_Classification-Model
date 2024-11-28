import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

class PredictionScreen extends StatefulWidget {
  const PredictionScreen({super.key});

  @override
  _PredictionScreenState createState() => _PredictionScreenState();
}

class _PredictionScreenState extends State<PredictionScreen> {
  final ImagePicker _picker = ImagePicker();
  String? _prediction;
  double? _confidence;

  void _predictImage() {
    // Here, add your API call or model prediction logic.
    setState(() {
      _prediction = "Maize Disease: XYZ";
      _confidence = 0.85;
    });
  }

  void _pickImage() async {
    final XFile? image = await _picker.pickImage(source: ImageSource.gallery);
    if (image != null) {
      // Use the picked image for prediction.
      print("Picked image path: ${image.path}");
      // Trigger prediction (e.g., upload the image to the backend).
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Prediction")),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            ElevatedButton(
              onPressed: _pickImage,
              child: const Text("Upload Image for Prediction"),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _predictImage,
              child: const Text("Predict"),
            ),
            const SizedBox(height: 20),
            if (_prediction != null) ...[
              Text("Prediction: $_prediction"),
              Text("Confidence: ${(_confidence! * 100).toStringAsFixed(2)}%"),
            ]
          ],
        ),
      ),
    );
  }
}
