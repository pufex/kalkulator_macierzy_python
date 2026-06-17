import PySide6.QtWidgets as qtw
import PySide6.QtCore as qtc
from my_utils.validators import shape_validator
from ui.messages import DefaultErrorMessageBox


class ShapeDialog(qtw.QDialog):

    commited = qtc.Signal(tuple)

    def __init__(self, title = "Give matrix shape"):

        super().__init__()
        self.setWindowTitle(title)
        self.form_layout = qtw.QFormLayout()
        self.setLayout(self.form_layout)

        self.rows_edit_line = qtw.QLineEdit("1")
        self.rows_edit_line.setValidator(shape_validator)
        self.form_layout.addRow("Rows", self.rows_edit_line)

        self.cols_edit_line = qtw.QLineEdit("1")
        self.cols_edit_line.setValidator(shape_validator)
        self.form_layout.addRow("Rows", self.cols_edit_line)

        button = qtw.QPushButton("Enter")
        button.clicked.connect(self.send_shape)
        self.form_layout.addRow(button)

    @qtc.Slot()
    def send_shape(self):
        """
        Retrieves the rows and columns entered by the user, validates them,
        emits the `commited` signal with the shape tuple, and closes the dialog.

        If an error occurs during parsing, shows an error message box.
        """
        try:
            rows = int(self.rows_edit_line.text())
            cols = int(self.cols_edit_line.text())
            self.commited.emit((rows, cols))
        except:
            DefaultErrorMessageBox().exec()
        else:
            self.close()


