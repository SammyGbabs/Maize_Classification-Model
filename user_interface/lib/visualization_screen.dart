import 'package:flutter/material.dart';

class VisualizationScreen extends StatelessWidget {
  const VisualizationScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Visualizations")),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            // Display your images or graphs here.
            Image.network('https://example.com/your-visualization-image.png'),
            const SizedBox(height: 20),
            const Text(
              "Here is the story behind the visualization.",
              style: TextStyle(fontSize: 18),
            ),
          ],
        ),
      ),
    );
  }
}
