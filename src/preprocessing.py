import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Function to split the dataset into training, validation, and testing sets
def splitting_dataset_tf(ds, train_split=0.7, val_split=0.15, test_split=0.15, shuffle=True, shuffle_size=10000):
    ds_size = len(ds)
    if shuffle:
        ds = ds.shuffle(shuffle_size, seed=12)
    train_size = int(train_split * ds_size)
    val_size = int(val_split * ds_size)

    train_ds = ds.take(train_size)
    val_ds = ds.skip(train_size).take(val_size)
    test_ds = ds.skip(train_size).skip(val_size)
    return train_ds, val_ds, test_ds

# Function to preprocess datasets with caching, shuffling, and prefetching
def preprocess_dataset(train_ds, val_ds, test_ds, buffer_size=tf.data.AUTOTUNE):
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=buffer_size)
    val_ds = val_ds.cache().shuffle(1000).prefetch(buffer_size=buffer_size)
    test_ds = test_ds.cache().shuffle(1000).prefetch(buffer_size=buffer_size)
    return train_ds, val_ds, test_ds

# Scaling layer for resizing and normalizing image pixels
def scaling_layer(image_size):
    return tf.keras.Sequential([
        layers.Resizing(image_size, image_size),
        layers.Rescaling(1.0 / 255)
    ])

# Data augmentation using ImageDataGenerator
def create_data_augmentor():
    return ImageDataGenerator(
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
