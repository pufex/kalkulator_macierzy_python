import PySide6.QtWidgets as qtw
import PySide6.QtCore as qtc
import PySide6.QtGui as qtg
import winsound
import numpy as np
import os

class MatrixDialog(qtw.QDialog):

    theres_matrix = qtc.Signal(np.ndarray)

    def __init__(self, matrix: np.ndarray, index: int = None):
        super().__init__()
        self.matrix = matrix
        self.index = index

        self.setWindowTitle(f"Macierz {index}")
        self.layout = qtw.QVBoxLayout()
        self.setLayout(self.layout)

        if index is None:
            self.save_button = qtw.QPushButton(self)
            self.save_button.setIcon(qtg.QIcon(os.path.join(os.getcwd(), "img/quicksave.png")))
            self.save_button.setIconSize(qtc.QSize(20, 20))
            self.save_button.clicked.connect(self.append_this_matrix)
            self.layout.addWidget(self.save_button, alignment= qtc.Qt.AlignmentFlag.AlignLeft)

        self.table = qtw.QTableWidget(self.matrix.shape[0], self.matrix.shape[1])
        self.table.horizontalHeader().setSectionResizeMode(qtw.QHeaderView.ResizeMode.ResizeToContents)
        self.table.cellChanged.connect(self.handle_cell_change)
        self.layout.addWidget(self.table)

        for i, row in enumerate(matrix):
            for j, el in enumerate(row):
                cell = qtw.QTableWidgetItem(str(el))
                self.table.setItem(i, j, cell)

    @qtc.Slot()
    def append_this_matrix(self):
        self.theres_matrix.emit(self.matrix)
        self.close()

    @qtc.Slot()
    def handle_cell_change(self, i, j):

        item = self.table.item(i, j)
        if item:
            try:
                self.matrix[i][j] = float(item.text() if item else 0)
            except ValueError:
                winsound.MessageBeep(winsound.MB_ICONWARNING)
            finally:
                item.setText(str(self.matrix[i][j]))