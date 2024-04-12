import tensorflow_datasets as tfds
import pandas as pd
import numpy as np
import cv2

class DatasetBuilder:
    def __init__(self):
        self.x_train = []
        self.y_train = []
        self.x_test = []
        self.y_test = []
        self.train_data_size = 0
        self.test_data_size = 0
        self.height_pixel_size = 0
        self.width_pixel_size = 0

    def build_dataset(self, hasy_root_path, dataset_root_path):
        self.__load_data(hasy_root_path)
        self.__save_to_csv(dataset_root_path)
        self.print_size_infos()

    def get_size_infos(self):
        return [self.train_data_size, self.test_data_size, self.height_pixel_size, self.width_pixel_size]

    def print_size_infos(self):
        print(f'train_data_size: {self.train_data_size}')
        print(f'test_data_size: {self.test_data_size}')
        print(f'height_pixel_size: {self.height_pixel_size}')
        print(f'width_pixel_size: {self.width_pixel_size}')

    def __save_to_csv(self, dataset_root_path):
        ######################################### DATASET CSV SAVE #########################################
        # Reshape the array to 2D (697932, 784) for CSV
        x_train_flattened = self.x_train.reshape(self.train_data_size, -1)
        x_test_flattened = self.x_test.reshape(self.test_data_size, -1)

        # Saves train image data to csv file
        df_train_image_data = pd.DataFrame(x_train_flattened)
        df_train_image_data.to_csv(dataset_root_path + '\\train_image_data.csv', index=False)

        # Saves train label data to csv file
        df_train_label_data = pd.DataFrame(self.y_train)
        df_train_label_data.to_csv(dataset_root_path + '\\train_label_data.csv', index=False)

        # Saves test image data to csv file
        df_test_image_data = pd.DataFrame(x_test_flattened)
        df_test_image_data.to_csv(dataset_root_path + '\\test_image_data.csv', index=False)

        # Saves test label data to csv file
        df_test_label_data = pd.DataFrame(self.y_test)
        df_test_label_data.to_csv(dataset_root_path + '\\test_label_data.csv', index=False)

        ####################################### DATASET CSV LOAD TEST #######################################
        # Loads train image data and verify with initial data
        loaded_df_train_image_data = pd.read_csv(dataset_root_path + '\\train_image_data.csv')
        loaded_array_train_image_data = loaded_df_train_image_data.to_numpy().reshape(self.train_data_size, self.height_pixel_size, self.width_pixel_size)
        print(f"train image data {np.array_equal(self.x_train, loaded_array_train_image_data)}")

        # Loads train label data and verify with initial data
        loaded_df_train_label_data = pd.read_csv(dataset_root_path + '\\train_label_data.csv')
        loaded_array_train_label_data = loaded_df_train_label_data.to_numpy().reshape(self.train_data_size)
        print(f"train label data {np.array_equal(self.y_train, loaded_array_train_label_data)}")

        # Loads test image data and verify with initial data
        loaded_df_test_image_data = pd.read_csv(dataset_root_path + '\\test_image_data.csv')
        loaded_array_test_image_data = loaded_df_test_image_data.to_numpy().reshape(self.test_data_size, self.height_pixel_size, self.width_pixel_size)
        print(f"test image data {np.array_equal(self.x_test, loaded_array_test_image_data)}")

        # Loads test label data and verify with initial data
        loaded_df_test_label_data = pd.read_csv(dataset_root_path + '\\test_label_data.csv')
        loaded_array_test_label_data = loaded_df_test_label_data.to_numpy().reshape(self.test_data_size)
        print(f"test label data {np.array_equal(self.y_test, loaded_array_test_label_data)}")

    def __load_data(self, hasy_root_path):
        # Load data from external sources
        self.__load_emnist_data()
        self.__load_hasy_data(hasy_root_path)

        # Convert lists to numpy arrays
        self.x_train = np.array(self.x_train)
        self.y_train = np.array(self.y_train)
        self.x_test = np.array(self.x_test)
        self.y_test = np.array(self.y_test)

        # Set variables related with size information
        self.__set_size_infos()

    def __set_size_infos(self):
        self.train_data_size   = len(self.x_train)
        self.test_data_size    = len(self.x_test)
        self.height_pixel_size = len(self.x_train[0])
        self.width_pixel_size  = len(self.x_train[0][0])

    def __load_emnist_data(self):
        # Loads emnist/byclass dataset
        (x_train_emnist, y_train_emnist), (x_test_emnist, y_test_emnist) = tfds.as_numpy(tfds.load('emnist', split=['train', 'test'], batch_size=-1, as_supervised=True))

        # Reshape array (697932, 28, 28, 1) to (697932, 28, 28) before filtering
        x_train_emnist = x_train_emnist.reshape((len(x_train_emnist), len(x_train_emnist[0]), len(x_train_emnist[0][0])))
        x_test_emnist = x_test_emnist.reshape((len(x_test_emnist), len(x_test_emnist[0]), len(x_test_emnist[0][0])))

        # Filter train and test data for chess annotation symbols/characters
        for i in range(len(x_train_emnist)):
            if ((y_train_emnist[i] >= 0) & (y_train_emnist[i] < 9)):
                self.x_train.append(cv2.transpose(x_train_emnist[i]))
                self.y_train.append(y_train_emnist[i])
            elif y_train_emnist[i] == 11:
                self.x_train.append(cv2.transpose(x_train_emnist[i]))
                self.y_train.append(20)
            elif y_train_emnist[i] == 20:
                self.x_train.append(cv2.transpose(x_train_emnist[i]))
                self.y_train.append(17)
            elif y_train_emnist[i] == 23:
                self.x_train.append(cv2.transpose(x_train_emnist[i]))
                self.y_train.append(21)
            elif y_train_emnist[i] == 26:
                self.x_train.append(cv2.transpose(x_train_emnist[i]))
                self.y_train.append(18)
            elif y_train_emnist[i] == 27:
                self.x_train.append(cv2.transpose(x_train_emnist[i]))
                self.y_train.append(19)
            elif ((y_train_emnist[i] >= 36) & (y_train_emnist[i] < 44)):
                self.x_train.append(cv2.transpose(x_train_emnist[i]))
                self.y_train.append(y_train_emnist[i] - 27)
            elif y_train_emnist[i] == 59:
                self.x_train.append(cv2.transpose(x_train_emnist[i]))
                self.y_train.append(23)

        for i in range(len(x_test_emnist)):
            if ((y_test_emnist[i] >= 0) & (y_test_emnist[i] < 9)):
                self.x_test.append(cv2.transpose(x_test_emnist[i]))
                self.y_test.append(y_test_emnist[i])
            elif y_test_emnist[i] == 11:
                self.x_test.append(cv2.transpose(x_test_emnist[i]))
                self.y_test.append(20)
            elif y_test_emnist[i] == 20:
                self.x_test.append(cv2.transpose(x_test_emnist[i]))
                self.y_test.append(17)
            elif y_test_emnist[i] == 23:
                self.x_test.append(cv2.transpose(x_test_emnist[i]))
                self.y_test.append(21)
            elif y_test_emnist[i] == 26:
                self.x_test.append(cv2.transpose(x_test_emnist[i]))
                self.y_test.append(18)
            elif y_test_emnist[i] == 27:
                self.x_test.append(cv2.transpose(x_test_emnist[i]))
                self.y_test.append(19)
            elif ((y_test_emnist[i] >= 36) & (y_test_emnist[i] < 44)):
                self.x_test.append(cv2.transpose(x_test_emnist[i]))
                self.y_test.append(y_test_emnist[i] - 27)
            elif y_test_emnist[i] == 59:
                self.x_test.append(cv2.transpose(x_test_emnist[i]))
                self.y_test.append(23)

    def __load_hasy_data(self, hasy_root_path):
        # Get image file path list and related label list for images contains #,-,+ symbols
        loaded_df_hasy = pd.read_csv(hasy_root_path + '\\hasy-data-labels.csv')
        loaded_array_hasy = loaded_df_hasy.to_numpy()
        label_filter = np.where((loaded_array_hasy[:,2] == '\#') | (loaded_array_hasy[:,2] == '-') | (loaded_array_hasy[:,2] == '+'))
        loaded_array_hasy_filtered = loaded_array_hasy[label_filter]

        # Split index set for %80 / %20 to create train and test data
        split_index = int(len(loaded_array_hasy_filtered) * 0.8)
        train_data_hasy, test_data_hasy = np.split(loaded_array_hasy_filtered, [split_index])
        x_train_hasy, y_train_hasy = train_data_hasy[:,0], train_data_hasy[:,2]
        x_test_hasy, y_test_hasy = test_data_hasy[:,0], test_data_hasy[:,2]

        # Fill x_train and y_train data with image and label data comes from hasy dataset
        for i in range(len(x_train_hasy)):
            abs_image_path = hasy_root_path + x_train_hasy[i]
            image = cv2.imread(abs_image_path)
            if image is not None:
                image = cv2.resize(image, (28, 28))
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                image = 255 - image
                self.x_train.append(image)
                if y_train_hasy[i] == '+':
                    self.y_train.append(24)
                elif y_train_hasy[i] == '-':
                    self.y_train.append(22)
                else: # y_train_hasy[i] = '/#'
                    self.y_train.append(25)

        # Fill x_test and y_test data with image and label data comes from hasy dataset
        for i in range(len(x_test_hasy)):
            abs_image_path = hasy_root_path + x_test_hasy[i]
            image = cv2.imread(abs_image_path)
            if image is not None:
                image = cv2.resize(image, (28, 28))
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                image = 255 - image
                self.x_test.append(image)
                if y_test_hasy[i] == '+':
                    self.y_test.append(24)
                elif y_test_hasy[i] == '-':
                    self.y_test.append(22)
                else: # y_test_hasy[i] = '/#'
                    self.y_test.append(25)