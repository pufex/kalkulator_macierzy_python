import PySide6.QtWidgets as qtw
import PySide6.QtCore as qtc
import winsound
import numpy as np

class MatrixDialog(qtw.QDialog):

    def __init__(self, matrix: np.ndarray, index: int):
        super().__init__()
        self.matrix = matrix
        self.index = index

        self.setWindowTitle(f"Macierz {index}")
        self.layout = qtw.QHBoxLayout()
        self.setLayout(self.layout)

        self.table = qtw.QTableWidget(self.matrix.shape[0], self.matrix.shape[1])
        self.table.horizontalHeader().setSectionResizeMode(qtw.QHeaderView.ResizeMode.ResizeToContents)
        self.table.cellChanged.connect(self.handle_cell_change)
        self.layout.addWidget(self.table)

        for i, row in enumerate(matrix):
            for j, el in enumerate(row):
                cell = qtw.QTableWidgetItem(str(el))
                self.table.setItem(i, j, cell)

    @qtc.Slot()
    def handle_cell_change(self, i, j):
        """
        Handles modifications of cells in the table widget.
        Updates the corresponding element in the underlying matrix. Plays a warning sound
        if the entered value is not a valid float.

        Args:
            i (int): Row index of the changed cell.
            j (int): Column index of the changed cell.
        """
        item = self.table.item(i, j)
        if item:
            try:
                self.matrix[i][j] = float(item.text() if item else 0)
            except ValueError:
                winsound.MessageBeep(winsound.MB_ICONWARNING)
            finally:
                item.setText(str(self.matrix[i][j]))