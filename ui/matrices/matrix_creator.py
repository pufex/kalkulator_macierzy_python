import PySide6.QtWidgets as qtw
import PySide6.QtCore as qtc
import PySide6.QtGui as qtg

import numpy as np

from my_utils.validators import value_validator, shape_validator
from ui.messages import DefaultErrorMessageBox

class MatrixCreator(qtw.QDialog):
    matrix_created = qtc.Signal(np.ndarray)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create a matrix")
        self.setMinimumWidth(300)
        self.form = qtw.QFormLayout()
        self.setLayout(self.form)

        label = qtw.QLabel("Create a custom matrix")
        label.setFont(qtg.QFont(label.font().family(), 15))
        self.form.addRow(label)

        self.rows_line_edit = qtw.QLineEdit("1")
        self.rows_line_edit.setValidator(shape_validator)
        self.form.addRow("Rows", self.rows_line_edit)

        self.cols_line_edit = qtw.QLineEdit("1")
        self.cols_line_edit.setValidator(shape_validator)
        self.form.addRow("Cols", self.cols_line_edit)

        self.default_value_edit = qtw.QLineEdit("0.0")
        self.default_value_edit.setValidator(value_validator)
        self.form.addRow("Values", self.default_value_edit)

        self.accept = qtw.QPushButton("Create your matrix")
        self.accept.clicked.connect(self.create_custom_matrix)
        self.form.addRow(self.accept)

    @qtc.Slot()
    def create_custom_matrix(self):
        try:
            row = int(self.rows_line_edit.text())
            col = int(self.cols_line_edit.text())

            if not(1 <= row <= 15):
                raise ValueError
            if not(1 <= col <= 15):
                raise ValueError

            value = float(self.default_value_edit.text())

            self.matrix_created.emit(np.full((row, col), value))
        except:
            DefaultErrorMessageBox().exec()
        else:
            self.close()