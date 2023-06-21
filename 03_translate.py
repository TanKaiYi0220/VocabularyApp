import sys
import PySide6
from PySide6.QtCore import Qt, QCoreApplication, QTranslator, QEvent, QLocale, QLibraryInfo
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox
from googletrans import Translator


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
        # Emit a signal to notify the main window to switch to the insert page
        self.page_switched.emit("insert")

    def on_evaluate_clicked(self):
        # Emit a signal to notify the main window to switch to the evaluate page
        self.page_switched.emit("evaluate")

    # Define a signal to notify the main window about page switches
    page_switched = PySide6.QtCore.Signal(str)


class InsertPage(QWidget):
    def __init__(self):
        super().__init__()

        # Create a layout for the insert page
        layout = QVBoxLayout()

        # Create a label for the title
        title_label = QLabel("Insert Vocabulary")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title_label)

        # Create a horizontal layout for the text fields, labels, and translate button
        text_layout = QHBoxLayout()

        # Create the label and text field for "Vocabulary"
        vocab_label = QLabel("Vocabulary:")
        vocab_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        text_layout.addWidget(vocab_label)
        self.vocab_field = QLineEdit()
        text_layout.addWidget(self.vocab_field)

        # Create the label and text field for "Meaning"
        meaning_label = QLabel("Meaning:")
        meaning_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        text_layout.addWidget(meaning_label)
        self.meaning_field = QLineEdit()
        text_layout.addWidget(self.meaning_field)

        # Create the "Translate" button
        translate_button = QPushButton("Translate")
        translate_button.setStyleSheet("font-size: 18px; padding: 10px;")
        translate_button.clicked.connect(self.on_translate_clicked)
        text_layout.addWidget(translate_button)

        layout.addLayout(text_layout)

        # Create the "Save" button
        save_button = QPushButton("Save")
        save_button.setStyleSheet("font-size: 18px; padding: 10px;")
        save_button.clicked.connect(self.on_save_clicked)
        layout.addWidget(save_button)

        # Set the layout for the insert page widget
        self.setLayout(layout)

    def on_translate_clicked(self):
        vocab_text = self.vocab_field.text()

        # Translate the vocabulary text using the Google Translate API
        translator = Translator()
        translation = translator.translate(vocab_text, dest="zh-cn")

        # Populate the "Meaning" text field with the translated text
        self.meaning_field.setText(translation.text)

    def on_save_clicked(self):
        vocab = self.vocab_field.text()
        meaning = self.meaning_field.text()
        # TODO: Implement saving the vocabulary and meaning
        QMessageBox.information(self, "Save", f"Vocabulary: {vocab}\nMeaning: {meaning} saved successfully!")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window title and size
        self.setWindowTitle("Vocabulary App")
        self.setMinimumSize(400, 300)

        # Create the home page and insert page widgets
        self.home_page = HomePage()
        self.insert_page = InsertPage()

        # Connect the page_switched signal to switch_pages function
        self.home_page.page_switched.connect(self.switch_pages)

        # Set the central widget as the home page initially
        self.setCentralWidget(self.home_page)

    def switch_pages(self, page):
        if page == "insert":
            self.setCentralWidget(self.insert_page)
        elif page == "evaluate":
            # TODO: Implement the evaluate page
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set the application style to a modern look and feel
    app.setStyle("Fusion")

    # Create and set the translator for the application
    translator = QTranslator()
    translator.load("qtbase_" + QLocale.system().name(), QLibraryInfo.location(QLibraryInfo.TranslationsPath))
    app.installTranslator(translator)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
