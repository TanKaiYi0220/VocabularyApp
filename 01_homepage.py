import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel


class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        # Create a layout for the home page
        layout = QVBoxLayout()

        # Create a label for the title
        title_label = QLabel("Vocabulary App")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title_label)

        # Create the "Insert" button
        insert_button = QPushButton("Insert")
        insert_button.setStyleSheet("font-size: 18px; padding: 10px;")
        insert_button.clicked.connect(self.on_insert_clicked)
        layout.addWidget(insert_button)

        # Create the "Evaluate" button
        evaluate_button = QPushButton("Evaluate")
        evaluate_button.setStyleSheet("font-size: 18px; padding: 10px;")
        evaluate_button.clicked.connect(self.on_evaluate_clicked)
        layout.addWidget(evaluate_button)

        # Set the layout for the home page widget
        self.setLayout(layout)

    def on_insert_clicked(self):
        # TODO: Implement the functionality for the "Insert" button
        print("Insert button clicked")

    def on_evaluate_clicked(self):
        # TODO: Implement the functionality for the "Evaluate" button
        print("Evaluate button clicked")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window title and size
        self.setWindowTitle("Vocabulary App")
        self.setMinimumSize(400, 300)

        # Set the central widget as the home page
        self.setCentralWidget(HomePage())


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set the application style to a modern look and feel
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
