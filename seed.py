import os
import cv2
import openpyxl
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox, QFileDialog
import pandas as pd
import matplotlib.pyplot as plt

def get_image_path():
    """Prompt user to input the path of the image."""
    file_path, _ = QFileDialog.getOpenFileName(None, "Open Image", "", "Image Files (*.png *.jpg *.jpeg)")
    return file_path if os.path.isfile(file_path) else None

def extract_properties(image_filename):
    """Extract properties from the image."""
    try:
        # Read the image
        image = cv2.imread(image_filename)
        
        if image is None:
            raise ValueError("Error: Unable to read the image file.")
        
        # Convert image to HSV color space
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Color ranges for seed types (Wheat, Pea, Corn)
        color_ranges = {
            "Wheat": [(20, 100, 100), (30, 255, 255), "Pale Yellow", 7],
            "Pea": [(36, 25, 25), (86, 255, 255), "Green", 5],
            "Pomegranate": [(0, 100, 100), (10, 255, 255), "Red", 12]
        }
        
        # Placeholder for detected properties
        detected_color = "Unknown"
        shape = "Unknown"
        size_mm = "Unknown"
        purity = "Unknown"
        health = "Unknown"
        germination_rate = "Unknown"
        name = None
        
        # Loop through each color range
        for seed_type, (lower_range, upper_range, color_name, size) in color_ranges.items():
            # Create mask using color range
            mask = cv2.inRange(hsv_image, np.array(lower_range), np.array(upper_range))
            
            # Find contours in the mask
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # Check if any contours are found
            if contours:
                # Assume the largest contour represents the seed
                contour = max(contours, key=cv2.contourArea)
                
                # Calculate properties (shape and size)
                perimeter = cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
                area = cv2.contourArea(contour)
                
                # Assign detected properties
                detected_color = color_name
                shape = "Square" if len(approx) == 4 else "Circle"
                size_mm = size
                name = seed_type
                
                # Placeholder for dynamic properties
                dynamic_purity = determine_purity(image, contour)  # Function to determine purity
                dynamic_health = determine_health(dynamic_purity)  # Function to determine health based on purity
                dynamic_germination_rate = determine_germination_rate(dynamic_purity)  # Function to determine germination rate based on purity
                
                # Update the properties
                purity = dynamic_purity
                health = dynamic_health
                germination_rate = dynamic_germination_rate
                
                break
        
        return detected_color, shape, size_mm, purity, health, germination_rate, name
    
    except Exception as e:
        print("Error:", str(e))
        return None, None, None, None, None, None, None

def determine_purity(image, contour):
    """Determine purity based on image analysis."""
    # Placeholder logic to determine purity based on image analysis
    # Calculate the purity based on the intensity of the detected color and other factors
    # For demonstration, let's use HSV values and assume higher values indicate higher purity
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_image, np.array([0, 50, 50]), np.array([255, 255, 255]))
    purity_score = cv2.countNonZero(mask) / (image.shape[0] * image.shape[1]) * 100
    return int(purity_score)

def determine_health(purity):
    """Determine health based on purity."""
    # Placeholder logic to determine health based on purity
    if purity <= 30:
        return "Poor"
    elif 30 < purity <= 60:
        return "Fair"
    elif 60 < purity <= 90:
        return "Good"
    else:
        return "Excellent"

def determine_germination_rate(purity):
    """Determine germination rate based on purity."""
    # Placeholder logic to determine germination rate based on purity
    if purity <= 30:
        return 10
    elif 30 < purity <= 60:
        return 40
    elif 60 < purity <= 90:
        return 70
    else:
        return 90

def main():
    app = QApplication([])
    main_window = QMainWindow()
    main_window.setWindowTitle("Seed Analyzer")

    def analyze_image():
        image_path = get_image_path()
        if image_path:
            color, shape, size_mm, purity, health, germination_rate, object_name = extract_properties(image_path)

            if None not in [color, shape, size_mm, purity, health, germination_rate, object_name]:
                wb = openpyxl.Workbook()
                ws = wb.active

                ws.append(["Color", "Shape", "Size (mm)", "Purity", "Health", "Germination Rate (%)", "Name"])
                ws.append([color, shape, size_mm, purity, health, germination_rate, object_name])

                wb.save("extracted_properties.xlsx")

                QMessageBox.information(main_window, "Success", "Image scanning completed and Dataset Updated successfully")

                # Plot graph
                plot_graph()

            else:
                QMessageBox.critical(main_window, "Error", "Failed to analyze the image.")

    def plot_graph():
        # Read data from the Excel file
        df = pd.read_excel("extracted_properties.xlsx")
    
        # Plot the graph with a straight line
        plt.plot(df["Name"], df["Germination Rate (%)"], marker='o', linestyle='-')
        plt.xlabel("Seed Name", fontsize=12, labelpad=10)
        plt.ylabel("Germination Rate (%)", fontsize=12, labelpad=10)
        plt.title("Germination Rate", fontsize=14, pad=20, loc="center")
        plt.xticks(rotation=45, ha="center")
        plt.yticks(np.arange(0, max(df["Germination Rate (%)"]) + 10, 10))
        plt.ylim(0, max(df["Germination Rate (%)"]) + 10)
        plt.xlim(-0.5, len(df["Name"]) - 0.5)
        plt.grid(False)  # Remove grid lines
        plt.show()
            
    analyze_button = QPushButton("Analyze Image", main_window)
    analyze_button.clicked.connect(analyze_image)
    main_window.setCentralWidget(analyze_button)

    main_window.show()
    app.exec_()

if __name__ == "__main__":
    main()