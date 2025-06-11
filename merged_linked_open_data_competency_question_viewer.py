import sys
import requests
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QListWidget, QListWidgetItem
from PyQt6.QtGui import QPixmap, QFont, QColor
from PyQt6.QtCore import Qt, QByteArray
import os

from competency_question_query import OntologyQuery  

class OntologyViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ontology Viewer")
        self.resize(1000, 600)

        self.ontology = OntologyQuery()

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # Left side - Image and dropdown
        left_layout = QVBoxLayout()
        self.layout.addLayout(left_layout, 1)

        self.material_dropdown = QComboBox()
        self.material_dropdown.addItems(self.ontology.get_materials())
        self.material_dropdown.currentIndexChanged.connect(self.on_material_selected)
        left_layout.addWidget(self.material_dropdown)

        self.image_label = QLabel("No image")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(self.image_label)

        # Right side - Related individuals
        self.right_list = QListWidget()
        self.right_list.setWordWrap(True)  # Allow text to wrap
        self.right_list.setSpacing(4)      # Add spacing between items
        
        self.layout.addWidget(self.right_list, 2)

        # Initial load
        self.on_material_selected(0)

    def on_material_selected(self, index):
        material_uri = self.material_dropdown.currentText()

        # Update image
        image_path = self.ontology.get_image_path(material_uri)
        if image_path and os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            self.image_label.setPixmap(pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio))
        #handle case where the imageis in the internet
        elif material_uri.startswith("http://") or material_uri.startswith("https://"):
            # self.image_label.setText(image_path)
            #image_path = "https://collectie.wereldculturen.nl/cc/imageproxy.ashx?server=localhost&port=17581&filename=images//Images/TM-Extra//TM-ALB-2022-9.jpg"
            print(f"Loading image from URL: {image_path}")
            try:
                pixmap = QPixmap()
                response = requests.get(image_path)
                print(f"Response status code: {response}")
                response.raise_for_status()
                pixmap.loadFromData(QByteArray(response.content))
                self.image_label.setPixmap(pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio))
            except Exception as e:
                print(f"Failed to load image from URL: {e}")
        else:
            self.image_label.setText("No image found")

        # Update related individuals
        self.right_list.clear()
        properties = [
            "hasCondition",
            "hasRule",
            "hasNeed",
            "hasRequirementFrom",
            "isOwnedPrimarilyBy",
            "assigned"
        ]

        for prop in properties:
            individuals = self.ontology.get_related_individuals(material_uri, prop)
            if individuals:
                # Section header
                header = QListWidgetItem(f"{prop}")
                header.setFont(QFont("Montserrat", 14, QFont.Weight.Bold))
                header.setForeground(QColor("#1a73e8"))
                self.right_list.addItem(header)

                for ind_data in individuals:
                    # Add direct classes
                    self.right_list.addItem(QListWidgetItem(", ".join(ind_data["direct_classes"]) or "—"))
                                
                    # Individual name - BOLD
                    individual_item = QListWidgetItem(ind_data["individual"])
                    bold_font = QFont("Montserrat", 11)
                    bold_font.setBold(True)
                    individual_item.setFont(bold_font)
                    self.right_list.addItem(individual_item)

                    if prop == "hasCondition": # Add Condition explanations
                        # Add explanations
                        explanations = self.ontology.get_explanations(individual_uri=ind_data["uri"], generic_prop="hasGenericConditionExplanation", specific_prop="hasSpecificConditionExplanation")
                        for explanation_type, explanation_list in explanations.items():
                            if explanation_list:
                                explanation_item = QListWidgetItem(f"{explanation_type.capitalize()} Explanations: {', '.join(explanation_list)}")
                                explanation_item.setFont(QFont("Montserrat", 10))
                                self.right_list.addItem(explanation_item)
                    elif prop == "hasRule": # Add Rule explanations
                        # Add explanations
                        explanations = self.ontology.get_explanations(individual_uri = ind_data["uri"], generic_prop="hasGenericRuleExplanation", specific_prop="hasSpecificRuleExplanation")
                        for explanation_type, explanation_list in explanations.items():
                            if explanation_list:
                                explanation_item = QListWidgetItem(f"{explanation_type.capitalize()} Explanations: {', '.join(explanation_list)}")
                                explanation_item.setFont(QFont("Montserrat", 10))
                                self.right_list.addItem(explanation_item)
                                

                    # Spacer
                    self.right_list.addItem(QListWidgetItem(""))

    def extract_label(self, uri):
        # Get fragment after the last '#' or '/'
        uri_str = str(uri)
        if '#' in uri_str:
            return uri_str.split('#')[-1]
        elif '/' in uri_str:
            return uri_str.split('/')[-1]
        else:
            return uri_str

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OntologyViewer() 
    window.show()
    sys.exit(app.exec())