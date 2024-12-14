from PyQt6.QtWidgets import QDialog, QGridLayout, QLineEdit, QComboBox, QPushButton, QApplication, QLabel, QMessageBox
import sys
import sqlite3


# Class to handle database connection
class DatabaseConnection():
    def __init__(self, database_file="database.db"):
        self.database_file = database_file

    def connect(self):
        connection = sqlite3.connect(self.database_file)
        return connection


# Dialog to insert new student data
class InsertDialog(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Add Student Data")
        layout = QGridLayout()

        # Input field for student name
        self.line_edit_name = QLineEdit()
        self.line_edit_name.setPlaceholderText("Name")
        layout.addWidget(self.line_edit_name, 0, 0)

        # Dropdown for selecting course
        self.combo_box = QComboBox()
        self.combo_box.addItems(["Math", "Astronomy", "Physics", "Biology"])
        layout.addWidget(self.combo_box, 1, 0)

        # Input field for phone number
        self.line_edit_phone = QLineEdit()
        self.line_edit_phone.setPlaceholderText("Phone")
        layout.addWidget(self.line_edit_phone, 2, 0)

        # Submit button
        self.button = QPushButton("Submit")
        self.button.clicked.connect(self.accept)
        layout.addWidget(self.button, 3, 0)

        self.setLayout(layout)

    def add_data(self):
        name = self.line_edit_name.text()
        course = self.combo_box.currentText()
        phone = self.line_edit_phone.text()

        # Connect to the database and insert new student data
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)", (name, course, phone))
        connection.commit()
        cursor.close()
        connection.close()
        self.main_window.load_data()


# Dialog to search for student data
class SearchDialog(QDialog):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.setWindowTitle("Search Student Data")
        layout = QGridLayout()

        # Input field for searching by student name
        self.line_search_name = QLineEdit()
        self.line_search_name.setPlaceholderText("Search Student by Name")
        layout.addWidget(self.line_search_name, 1, 1)

        # Search button
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.accept)
        layout.addWidget(self.search_button, 2, 1)

        self.setLayout(layout)

    def search_data(self):
        name = self.line_search_name.text()
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students WHERE name == ?", (name,))
        element = cursor.fetchone()
        cursor.close()
        connection.close()
        return element


# Dialog to edit existing student data
class EditDialog(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Update Student Data")
        layout = QGridLayout()

        # Get student name from selected row
        self.index = self.main_window.table.currentRow()
        student_name = main_window.table.item(self.index, 1).text()

        # Input field for student name
        self.line_edit_name = QLineEdit(student_name)
        self.line_edit_name.setPlaceholderText("Name")
        layout.addWidget(self.line_edit_name, 0, 0)

        # Get course name from selected row
        course_name = self.main_window.table.item(self.index, 2).text()
        self.combo_box = QComboBox()
        self.combo_box.addItems(["Math", "Astronomy", "Physics", "Biology"])
        self.combo_box.setCurrentText(course_name)
        layout.addWidget(self.combo_box, 1, 0)

        # Input field for phone number
        current_mobile = self.main_window.table.item(self.index, 3).text()
        self.line_edit_phone = QLineEdit(current_mobile)
        self.line_edit_phone.setPlaceholderText("Phone")
        layout.addWidget(self.line_edit_phone, 2, 0)

        # Update button
        self.button = QPushButton("Update")
        self.button.clicked.connect(self.accept)
        layout.addWidget(self.button, 3, 0)

        self.setLayout(layout)

    def edit(self):
        name = self.line_edit_name.text()
        course = self.combo_box.currentText()
        phone = self.line_edit_phone.text()
        id = self.main_window.table.item(self.index, 0).text()

        # Connect to the database and update student data
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute(f"UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?", (name, course, phone, id))
        connection.commit()
        cursor.close()
        connection.close()
        self.main_window.load_data()


# Dialog to delete student data
class DeleteDialog(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Update Student Data")

        layout = QGridLayout()
        confirmation = QLabel("Are you sure you want to delete?")
        yes_button = QPushButton("yes")
        yes_button.clicked.connect(self.yes)
        no = QPushButton("no")
        no.clicked.connect(self.close)

        layout.addWidget(confirmation, 0, 0)
        layout.addWidget(yes_button, 0, 1)
        layout.addWidget(no, 0, 2)

        self.setLayout(layout)

    def yes(self):
        self.index = self.main_window.table.currentRow()
        id = self.main_window.table.item(self.index, 0).text()

        # Connect to the database and delete student data
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM students WHERE id == ?", (id,))
        connection.commit()
        cursor.close()
        connection.close()
        self.close()
        self.main_window.load_data()


# Dialog to show information about the application
class AboutDialog(QMessageBox):
    def __init__(self, main_window):
        super().__init__()
        self.setWindowTitle("About")
        content = """Student Management System

Welcome to the Student Management System! This application is designed to help you efficiently manage student data with ease. Whether you are an educator, administrator, or simply need to keep track of student information, this app provides a user-friendly interface to handle all your needs.

Key Features:

Add Student Data: Easily add new student records, including their name, course, and contact information.
Search Students: Quickly search for students by name to find their details.
Edit Student Information: Update existing student records to keep information current.
Delete Student Records: Remove student records that are no longer needed.
View All Students: Display all student data in a clear and organized table format.
How to Use:

Add a Student: Click on the "Add Student" button in the toolbar or menu to open the dialog for entering new student information.
Search for a Student: Use the "Search Student" button to find a student by name. If the student exists, their information will be displayed.
Edit a Student: Select a student from the table and click "Edit Record" in the status bar to update their details.
Delete a Student: Select a student from the table and click "Delete Record" in the status bar to remove their record.
About: Learn more about the application by clicking on the "About" option in the help menu.
This app is built with PyQt6, providing a robust and responsive interface for managing student data. We hope you find it useful and easy to use!"""
        self.setText(content)
