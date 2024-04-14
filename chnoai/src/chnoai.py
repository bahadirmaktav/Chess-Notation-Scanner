import tensorflow as tf
import numpy as np
import cv2

class Chnoai:
    def __init__():
        None

    # Converts picture of chess notation paper to chess algebraic notation matrix
    def img2alno(self, image):
        sliced_images = self.__extract_images_horizontally(image)
        
        None

    # Extracts images for each moves
    def __extract_move_images(self, sliced_images):
        move_images = []

        # Convert the image to grayscale
        sliced_image_gray = cv2.cvtColor(sliced_images[0], cv2.COLOR_BGR2GRAY)

        # Uses Otsu method for thresholding the image 
        ret, sliced_image_thresh = cv2.threshold(sliced_image_gray, 0, 255, cv2.THRESH_OTSU)

        ctrs, _ = cv2.findContours(sliced_image_thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])

        # Calculate average bounding contour area
        areas = [cv2.contourArea(ctr) for ctr in ctrs]
        average_area = sum(areas) / len(areas)

        # Define thresholds as a percentage of the average area
        lower_threshold = 30000  # 0.5 * average_area
        upper_threshold = 40000 # 6.0 * average_area

        extracted_move_boxes = []
        for i, ctr in enumerate(sorted_ctrs):
            x, y, w, h = cv2.boundingRect(ctr)
            area = w*h
            if lower_threshold < area < upper_threshold:
                # rect = cv2.rectangle(chmove_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # cv2.imshow('rect', rect)
                extracted_move_boxes.append(sliced_image_gray[y:y + h, x:x + w])

    # Extracts symbol images from move images
    def __extract_symbols(self, move_images):
        None

    # Uses cnn model to predict symbol and returns the predicted symbol list as characters
    def __predict_symbols(self, symbol_images):
        None

    # Maps prediction value to character
    def __map_symbol_character(self, prediction_value):
        None
    
    # Slice image splitted with horizontal lines
    def __extract_images_horizontally(self, image):
        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Uses Otsu method for thresholding the image 
        ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Detect horizontal lines
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (80,1))
        detect_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
        cnts = cv2.findContours(detect_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        # Gets average list of contours y axis
        cnts_y_averages = []
        for cnt in cnts:
            temp_total = 0
            for pnt in cnt:
                temp_total += pnt[0][1]
            cnts_y_averages.append(temp_total / len(cnt))
        cnts_y_averages.sort()

        # Filter average list, remove close average dublicates
        filtered_cnts_y_averages = [cnts_y_averages[0]]
        for i in range(1, len(cnts_y_averages)):
            if cnts_y_averages[i] > cnts_y_averages[i - 1] + 20: # offset
                filtered_cnts_y_averages.append(cnts_y_averages[i])

        # Gets sliced images according to average values
        sliced_images = []
        for i in range(1, len(filtered_cnts_y_averages)):
            temp_sliced_image = image[int(filtered_cnts_y_averages[i - 1]) : int(filtered_cnts_y_averages[i]), : len(image[0])]
            temp_sliced_image = cv2.copyMakeBorder(temp_sliced_image, 2, 2, 2, 2, cv2.BORDER_CONSTANT, value=(0, 0, 0))
            sliced_images.append(temp_sliced_image)

        return sliced_images