import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import os

class ImageLoader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Local Image Loader")

        # Layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Widgets
        self.image_label = QLabel("Image will be shown here")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setFixedSize(300, 300)  # Optional: fixed size

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter image filename (e.g. mypic.png)")

        self.load_button = QPushButton("Load Image")
        self.load_button.clicked.connect(self.load_image)

        # Add widgets to layout
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.input_field)
        self.layout.addWidget(self.load_button)

    def load_image(self):
        filename = self.input_field.text().strip()

        if not filename:
            QMessageBox.warning(self, "Input Error", "Please enter an image filename.")
            return

        # Path restriction: only same folder as the script
        current_folder = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(current_folder, filename)

        if not os.path.isfile(full_path):
            QMessageBox.warning(self, "File Error", "File not found in the current directory.")
            return

        pixmap = QPixmap(full_path)
        if pixmap.isNull():
            QMessageBox.warning(self, "Load Error", "Failed to load image. Not a valid image file.")
            return

        # Resize pixmap to fit the label if needed
        scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio)
        self.image_label.setPixmap(scaled_pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageLoader()
    window.show()
    sys.exit(app.exec())