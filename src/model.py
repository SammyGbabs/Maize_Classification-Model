#Initializing the DenseNet201 model pre trained on ImageNet without top layers
base_model_densenet = DenseNet201(weights='imagenet', include_top=False, input_shape=(256, 256, 3))

# Selected layers for fine-tuning
x = base_model_densenet.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
x = Dropout(0.5)(x)
predictions = Dense(len(classes), activation='softmax')(x)

# model
model_densenet = Model(inputs=base_model_densenet.input, outputs=predictions)

# Freezing the base model layers
for layer in base_model_densenet.layers:
    layer.trainable = False

# Compiling the model
model_densenet.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Training the model using the train_ds and evaluating on val_ds
history = model_densenet.fit(
    train_ds,
    epochs = 10,
    validation_data = val_ds,
    verbose = 1,
)

#Saving ther model using pickle
import pickle

with open('model1.pkl', 'wb') as f:
    pickle.dump(model_densenet, f)

# Save the model to an HDF5 file
model_densenet.save('model_densenet.h5')

# Save the model with a .keras extension
model_densenet.save('model_densenet.keras')

#Saving the model using joblib
import joblib

joblib.dump(model_densenet, 'model_densenet.joblib')