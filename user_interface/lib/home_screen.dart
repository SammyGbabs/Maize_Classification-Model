import 'package:flutter/material.dart';
import 'prediction_screen.dart';
import 'upload_retrain_screen.dart';
import 'visualization_screen.dart';

class HomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Maize Classification')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => PredictionScreen()),
                );
              },
              child: Text("Go to Prediction Screen"),
            ),
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                      builder: (context) => UploadRetrainScreen()),
                );
              },
              child: Text("Go to Upload & Retrain Screen"),
            ),
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                      builder: (context) => VisualizationScreen()),
                );
              },
              child: Text("Go to Visualizations Screen"),
            ),
          ],
        ),
      ),
    );
  }
}
