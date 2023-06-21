import sys
from PySide6.QtCore import Qt, QCoreApplication, QTranslator, QEvent, QLocale, QLibraryInfo
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox
from googletrans import Translator

import sqlite3

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

        # Create the label and text field for "Vocabulary"
        vocab_label = QLabel("Vocabulary:")
        vocab_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(vocab_label)
        self.vocab_field = QLineEdit()
        layout.addWidget(self.vocab_field)

        # Create the "Translate" button
        translate_button = QPushButton("Translate")
        translate_button.setStyleSheet("font-size: 18px; padding: 10px;")
        translate_button.clicked.connect(self.on_translate_clicked)
        layout.addWidget(translate_button)

        # Create the label and text field for "Meaning"
        meaning_label = QLabel("Meaning:")
        meaning_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(meaning_label)
        self.meaning_field = QLineEdit()
        layout.addWidget(self.meaning_field)

        # Create the "Save" button
        save_button = QPushButton("Save")
        save_button.setStyleSheet("font-size: 18px; padding: 10px;")
        save_button.clicked.connect(self.on_save_clicked)
        layout.addWidget(save_button)

        # Center-align the components
        layout.setAlignment(Qt.AlignCenter)

        # Set the layout for the insert page widget
        self.setLayout(layout)

    def on_translate_clicked(self):
        vocab_text = self.vocab_field.text()

        # Translate the vocabulary text using the Google Translate API
        translator = Translator()
        translation = translator.translate(vocab_text, dest="zh-tw")

        # Populate the "Meaning" text field with the translated text
        self.meaning_field.setText(translation.text)

    def on_save_clicked(self):
        vocab = self.vocab_field.text().lower()
        meaning = self.meaning_field.text()

        # Check if the word already exists in the database
        cursor.execute("SELECT id, weight FROM vocabulary WHERE word=?", (vocab,))
        existing_word = cursor.fetchone()
        if existing_word:
            word_id, weight = existing_word
            weight += 1
            # Update the weight of the existing word in the database
            cursor.execute("UPDATE vocabulary SET weight=? WHERE id=?", (weight, word_id))
            conn.commit()
            QMessageBox.information(self, "Existed", f"Vocabulary: {vocab}\nMeaning: {meaning} repeated {weight} times!")
        else:
            # Insert the new word with weight 1 into the database
            cursor.execute("INSERT INTO vocabulary (word, meaning) VALUES (?, ?)", (vocab, meaning))
            conn.commit()
            QMessageBox.information(self, "Save", f"Vocabulary: {vocab}\nMeaning: {meaning} saved successfully!")

        # Clear the text fields
        self.vocab_field.clear()
        self.meaning_field.clear()


class EvaluatePage(QWidget):
    def __init__(self):
        super().__init__()

        # Create a layout for the evaluate page
        layout = QVBoxLayout()

        # Create a label for the title
        title_label = QLabel("Evaluate Vocabulary")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title_label)

        # TODO: Add evaluation components

        # Center-align the components
        layout.setAlignment(Qt.AlignCenter)

        # Set the layout for the evaluate page widget
        self.setLayout(layout)


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

        # Center-align the components
        layout.setAlignment(Qt.AlignCenter)

        # Set the layout for the home page widget
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window title and size
        self.setWindowTitle("Vocabulary App")
        self.setMinimumSize(400, 300)

        # Create the home page widget
        self.home_page = QWidget()

        # Create a layout for the home page
        layout = QVBoxLayout()

        # Create a label for the title
        title_label = QLabel("Vocabulary App")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title_label)

        # Create a menu bar
        menu_bar = self.menuBar()

        # Create a "File" menu
        page_menu = menu_bar.addMenu("Pages")

        # Create the action for the home page
        home_action = QAction("Home", self)
        home_action.triggered.connect(self.switch_to_home)
        page_menu.addAction(home_action)

        # Create the action for the insert page
        insert_action = QAction("Insert", self)
        insert_action.triggered.connect(self.switch_to_insert)
        page_menu.addAction(insert_action)

        # Create the action for the evaluate page
        evaluate_action = QAction("Evaluate", self)
        evaluate_action.triggered.connect(self.switch_to_evaluate)
        page_menu.addAction(evaluate_action)

        # Set the layout for the main window widget
        self.switch_to_home()

    def switch_to_home(self):
        home_page = HomePage()
        self.setCentralWidget(home_page)

    def switch_to_insert(self):
        insert_page = InsertPage()
        self.setCentralWidget(insert_page)

    def switch_to_evaluate(self):
        evaluate_page = EvaluatePage()
        self.setCentralWidget(evaluate_page)


if __name__ == "__main__":
    # Create a database connection
    conn = sqlite3.connect("vocabulary.db")
    cursor = conn.cursor()

    # Create a table for storing vocabulary with weights
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vocabulary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT,
            meaning TEXT,
            weight INTEGER DEFAULT 1
        )
    """)
    conn.commit()

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
