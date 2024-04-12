import matplotlib.pyplot as plt
import tensorflow as tf
import pandas as pd
import numpy as np
import cv2
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.utils import to_categorical
from keras.models import Sequential

class ModelBuilder:
    def __init__(self):
        # TODO(MBM) : Gets these values from DatasetBuilder.
        self.train_data_size   = 405131
        self.test_data_size    = 67732
        self.height_pixel_size = 28
        self.width_pixel_size  = 28
        self.x_train = np.array([])
        self.y_train = np.array([])
        self.x_test = np.array([])
        self.y_test = np.array([])
        self.model = None
        self.history = None

    def create_fnn_model(self):
        # Create model
        self.model = Sequential([
            Flatten(input_shape=(28, 28)),
            Dense(128, activation='relu'),
            Dense(26, activation='softmax')
        ])

        # Compile model
        self.model.compile(optimizer='adam',
                    loss='categorical_crossentropy',
                    metrics=['accuracy'])
        
    def create_cnn_model(self):
        # Create model
        self.model = Sequential([
            Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
            MaxPooling2D((2, 2)),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D((2, 2)),
            Conv2D(64, (3, 3), activation='relu'),
            Flatten(),
            Dense(64, activation='relu'),
            Dense(26, activation='softmax')
        ])

        # Compile model
        self.model.compile(optimizer='adam',
                    loss='categorical_crossentropy',
                    metrics=['accuracy'])

    def train_the_model(self):
        # Load data
        self.__load_data()

        # Normalization
        self.x_train = self.x_train / 255.0
        self.x_test = self.x_test / 255.0

        # Set outputs as categorical. eg. 4 to [0,0,0,0,1,0,0,0...]
        # There are 26 classes total (symbols, characters etc.)
        self.y_train = to_categorical(self.y_train, 26)
        self.y_test = to_categorical(self.y_test, 26)

        # Train model
        self.history = self.model.fit(self.x_train, self.y_train, epochs=6, validation_data=(self.x_test, self.y_test))

    def plot_loss_accuracy_graphs(self):
        # Plot Loss-Epoch Graph
        plt.plot(self.history.history['loss'], label='Training Loss')
        plt.plot(self.history.history['val_loss'], label='Validation Loss')
        plt.title('Training and Validation Loss')
        plt.xlabel('Epoch')
        plt.ylabel('Loss Value')
        plt.legend()
        plt.show()

        # Plot Accuracy-Epoch Graph 
        plt.plot(self.history.history['accuracy'], label='Training Accuracy')
        plt.plot(self.history.history['val_accuracy'], label='Validation Accuracy')
        plt.title('Training and Validation Accuracy')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.legend()
        plt.show()

    def save_the_model(self, version):
        # Save model
        self.model.save(f"..\\models\\channo_v{version}.keras")

    def __load_data(self):
        # Loads train image data and verify with initial data
        loaded_df_train_image_data = pd.read_csv('..\\dataset\\train_image_data.csv')
        loaded_array_train_image_data = loaded_df_train_image_data.to_numpy().reshape(self.train_data_size, self.height_pixel_size, self.width_pixel_size)

        # Loads train label data and verify with initial data
        loaded_df_train_label_data = pd.read_csv('..\\dataset\\train_label_data.csv')
        loaded_array_train_label_data = loaded_df_train_label_data.to_numpy().reshape(self.train_data_size)

        # Loads test image data and verify with initial data
        loaded_df_test_image_data = pd.read_csv('..\\dataset\\test_image_data.csv')
        loaded_array_test_image_data = loaded_df_test_image_data.to_numpy().reshape(self.test_data_size, self.height_pixel_size, self.width_pixel_size)

        # Loads test label data and verify with initial data
        loaded_df_test_label_data = pd.read_csv('..\\dataset\\test_label_data.csv')
        loaded_array_test_label_data = loaded_df_test_label_data.to_numpy().reshape(self.test_data_size)

        # Set train and test data names to x and y for simplicity
        self.x_train, self.y_train = loaded_array_train_image_data, loaded_array_train_label_data
        self.x_test, self.y_test = loaded_array_test_image_data, loaded_array_test_label_data