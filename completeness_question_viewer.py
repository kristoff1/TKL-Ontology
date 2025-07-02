import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QListWidget, QListWidgetItem
from PyQt6.QtGui import QPixmap, QFont, QColor
from PyQt6.QtCore import Qt

from completeness_question_query import CompletenessQuery  # Get query functions

class CompletenessQuestionViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Completeness Question Viewer")
        self.resize(1000, 600)

        self.ontology = CompletenessQuery()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # Left side - Selected Label and label dropdown selectors
        left_layout = QVBoxLayout()
        self.layout.addLayout(left_layout, 1)
        self.label_dropdown = QComboBox()
        self.label_dropdown.addItems(self.ontology.get_label_individuals())
        self.label_dropdown.currentIndexChanged.connect(self.on_label_selected)
        left_layout.addWidget(self.label_dropdown)

        #Right side - Label classes, properties, and range concepts
        right_layout = QVBoxLayout()
        self.layout.addLayout(right_layout, 2)
        self.triple_list = QListWidget()
        self.triple_list.setWordWrap(True)  # Allow text to wrap
        self.triple_list.setSpacing(4)      # Add spacing between items
        right_layout.addWidget(self.triple_list)

        #initial load
        self.on_label_selected(0)

    def extract_text(self, uri):
        # Get fragment after the last '#' or '/'
        uri_str = str(uri)
        if '/' in uri_str:
            return uri_str.split('/')[-1]
        else:
            return uri_str

    def on_label_selected(self, index):
        label_individual = self.label_dropdown.currentText()
        
        # Get label class
        label_classes = self.ontology.get_label_concept(label_individual)
        self.triple_list.clear()
        for label_class in label_classes:
            rule_properties = self.ontology.get_rule_sub_object_properties(label_class)
            condition_properties = self.ontology.get_condition_sub_object_properties(label_class)
            purpose_properties = self.ontology.get_purpose_sub_object_properties(label_class)
            for property_name in rule_properties + condition_properties + purpose_properties:
                range_classes = self.ontology.get_range_classes_of_property(property_name)
                for range_class in range_classes:
                    trimmed_label_class = self.extract_text(label_class)
                    trimmed_property_name = self.extract_text(property_name)
                    trimmed_range_class = self.extract_text(range_class)
                    item = QListWidgetItem(f"{(trimmed_label_class)} - {trimmed_property_name} -> {trimmed_range_class}")
                    item.setFont(QFont("Arial", 12, QFont.Weight.Normal))
                    item.setForeground(QColor(0, 0, 128))  
                    self.triple_list.addItem(item)

        rules_boolean = self.ontology.get_indicated_rules_of_label(label_individual)
        for rule, status in rules_boolean.items():
            trimmed_rule = self.extract_text(rule)
            if status:
                item = QListWidgetItem(f"{trimmed_rule}: True")
                item.setForeground(QColor(0, 200, 20))
            else:
                item = QListWidgetItem(f"{trimmed_rule}: False")
                item.setForeground(QColor(200, 0, 0))
            item.setFont(QFont("Arial", 12, QFont.Weight.Medium))
            self.triple_list.addItem(item)

        condition_boolean = self.ontology.get_indicated_conditions_of_label(label_individual)
        for condition, status in condition_boolean.items():
            trimmed_condition = self.extract_text(condition)
            if status:
                item = QListWidgetItem(f"{trimmed_condition}: True")
                item.setForeground(QColor(0, 200, 20))
            else:
                item = QListWidgetItem(f"{trimmed_condition}: False")
                item.setForeground(QColor(200, 0, 0))
            item.setFont(QFont("Arial", 12, QFont.Weight.Medium))
            self.triple_list.addItem(item)

        purpose_boolean = self.ontology.get_indicated_purposes_of_label(label_individual)
        for purpose, status in purpose_boolean.items():
            trimmed_purpose = self.extract_text(purpose)
            if status:
                item = QListWidgetItem(f"{trimmed_purpose}: True")
                item.setForeground(QColor(0, 200, 20))
            else:
                item = QListWidgetItem(f"{trimmed_purpose}: False")
                item.setForeground(QColor(200, 0, 0))
            item.setFont(QFont("Arial", 12, QFont.Weight.Medium))
            self.triple_list.addItem(item)

        information_boolean = self.ontology.get_indicated_information_of_label(label_individual)
        for information, status in information_boolean.items():
            trimmed_information = self.extract_text(information)
            if status:
                item = QListWidgetItem(f"{trimmed_information}: True")
                item.setForeground(QColor(0, 200, 20))
            else:
                item = QListWidgetItem(f"{trimmed_information}: False")
                item.setForeground(QColor(200, 0, 0))
            item.setFont(QFont("Arial", 12, QFont.Weight.Medium))
            self.triple_list.addItem(item)    

        #rules_boolean.items = [f"{self.extract_text(rule)}: {status}" for rule, status in rules_boolean.items()]
        #self.triple_list.addItem(QListWidgetItem(f"Rules Boolean: {rules_boolean}"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = CompletenessQuestionViewer()
    viewer.show()
    sys.exit(app.exec())



    