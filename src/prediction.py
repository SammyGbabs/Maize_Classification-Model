# Prediction on test data using DenseNet201 model
test_preds = model_densenet.predict(test_ds)
test_preds = np.argmax(test_preds, axis=1)

true_labels = []
for images, labels in test_ds:
    true_labels.extend(labels.numpy())

# Report for DenseNet201
print(classification_report(true_labels, test_preds, target_names=classes))

#Making a prediction
import numpy as np
for images_batch, labels_batch in test_ds.take(1):
  img_1 = images_batch[0].numpy().astype('uint8')
  img1_label = labels_batch[0].numpy()

  print('First image to predict:')
  plt.imshow(img_1)
  print('Actual label on dataset:', classes[img1_label])

  batch_prediction = model_densenet.predict(images_batch)
  print('Predicted label by model:', classes[np.argmax(batch_prediction[0])])
  plt.axis("off")