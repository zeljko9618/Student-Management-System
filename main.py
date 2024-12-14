from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QToolBar, QLineEdit, QComboBox, \
    QPushButton, QDialog, QMessageBox, QStatusBar
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3
from dialogs import InsertDialog, SearchDialog, EditDialog, DeleteDialog, AboutDialog


# Class to handle database connection
class DatabaseConnection():
    def __init__(self, database_file="database.db"):
        self.database_file = database_file

    def connect(self):
        connection = sqlite3.connect(self.database_file)
        return connection


# Main window class for the application
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setFixedWidth(600)
        self.setFixedHeight(400)

        # Menu bar
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")

        # Add student action
        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.add_student_dialog)
        file_menu_item.addAction(add_student_action)

        # Search student action
        search_student_action = QAction(QIcon("icons/search.png"), "Search Student", self)
        search_student_action.triggered.connect(self.search_student_dialog)
        file_menu_item.addAction(search_student_action)

        # About action
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)
        about_action.triggered.connect(self.about)

        # Table to display student data
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # Toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_student_action)

        # Status bar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        # Edit and delete buttons in the status bar
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit_student_dialog)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete_student_dialog)

        # Remove existing buttons to avoid duplicates
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def about(self):
        # Show about dialog
        dialog = AboutDialog(self)
        dialog.exec()

    def edit_student_dialog(self):
        # Show edit student dialog
        dialog = EditDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            dialog.edit()

    def delete_student_dialog(self):
        # Show delete student dialog
        dialog = DeleteDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_data()

    def add_student_dialog(self):
        # Show add student dialog
        dialog = InsertDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            dialog.add_data()

    def search_student_dialog(self):
        # Show search student dialog
        dialog = SearchDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.search_data()
            if data:
                self.load_data(data)
            else:
                QMessageBox.information(self, "No Results", "No student found with that name.")

    def load_data(self, data=None):
        if data:
            # Load specific student data
            self.table.setRowCount(1)
            for column, value in enumerate(data):
                self.table.setItem(0, column, QTableWidgetItem(str(value)))
        else:
            # Load all student data from the database
            connection = DatabaseConnection().connect()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM students")
            rows = cursor.fetchall()
            self.table.setRowCount(len(rows))
            for row_index, row_data in enumerate(rows):
                for column_index, value in enumerate(row_data):
                    self.table.setItem(row_index, column_index, QTableWidgetItem(str(value)))
            cursor.close()
            connection.close()


# Main application
app = QApplication(sys.argv)
main_window = MainWindow()
main_window.load_data()
main_window.show()
sys.exit(app.exec())
