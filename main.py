import sys

import numpy as np
import PySide6.QtWidgets as qtw
import PySide6.QtCore as qtc
import PySide6.QtGui as qtg

from file_management.files import FileManager
from my_types.global_types import CtxDict
from ui.file_managment.loading import LoadMenu
from ui.file_managment.saving import SaveMenu
from ui.messages import DefaultErrorMessageBox
from ui.matrices.matrix_dialog import MatrixDialog
from ui.matrices.matrix_creator import MatrixCreator
from ui.matrices.shape_dialog import ShapeDialog
from ui.algorithms.pick_matrices_dialog import PickMatricesDialog

from algorithms.linear_systems import gauss_elimination as gs

# TODO: Shape Dialog -> a dialog that returns shape of new matrix

class Window(qtw.QMainWindow):
    def __init__(self, ctx: CtxDict):
        super().__init__()

        self.ctx = ctx
        self.matrixButtons = []

        self.setWindowTitle("Matrices")
        self.setMinimumWidth(275)

        self.central_widget = qtw.QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = qtw.QGridLayout()
        self.layout.setSizeConstraint(qtw.QGridLayout.SizeConstraint.SetFixedSize)
        self.central_widget.setLayout(self.layout)

        self._create_file_menu()
        self._create_algorithm_menu()
        self._create_toolbar()

        self.buttons_group = qtw.QButtonGroup(self.layout)
        self.buttons_group.idClicked.connect(self.open_matrix_dialog)
        self.update_matrices_ui()

    @qtc.Slot()
    def update_matrices_ui(self):
        for button in list(self.buttons_group.buttons()):
            self.layout.removeWidget(button)
            self.buttons_group.removeButton(button)
            button.deleteLater()

        for index, matrix in enumerate(self.ctx["matrices"]):
            button = qtw.QPushButton(f"Matrix {index}", self)
            self.buttons_group.addButton(button, index)
            self.layout.addWidget(button, index // 3 + 1, index % 3 + 1)

    @qtc.Slot()
    def append_matrix_in_ui(self, matrix: np.ndarray):
        self.ctx["matrices"].append(matrix)
        index = len(self.ctx["matrices"]) - 1
        button = qtw.QPushButton(f"Matrix {index}", self)
        self.buttons_group.addButton(button, index)
        self.layout.addWidget(button, index // 3 + 1, index % 3 + 1)

    def _create_file_menu(self):
        menu_bar = self.menuBar()
        file_menu = qtw.QMenu("Files", menu_bar)
        menu_bar.addMenu(file_menu)

        load_matrices = qtg.QAction(qtg.QIcon("img/load.png"), "Load matrices", self)
        load_matrices.setStatusTip("Load matrices from a file")
        load_matrices.triggered.connect(self.open_load_dialog)
        file_menu.addAction(load_matrices)

        quick_load = qtg.QAction(qtg.QIcon("img/quick-load.png"), "Quick Load", self)
        quick_load.setStatusTip("Quickly load up matrices")
        quick_load.triggered.connect(self.load_from_current_file)
        file_menu.addAction(quick_load)

        save_matrices = qtg.QAction(qtg.QIcon("img/save.png"), "Save", self)
        save_matrices.setStatusTip("Save matrices from to a file")
        save_matrices.triggered.connect(self.open_save_dialog)
        file_menu.addAction(save_matrices)

        save_matrices_quickly = qtg.QAction(qtg.QIcon("img/quicksave.png"), "Quick Save", self)
        save_matrices_quickly.setStatusTip("Save matrices quickly.")
        save_matrices_quickly.triggered.connect(self.save_to_current_file)
        file_menu.addAction(save_matrices_quickly)

    @qtc.Slot()
    def open_load_dialog(self):
        load_menu = LoadMenu(self.ctx)
        load_menu.matrices_loaded.connect(self.update_matrices_ui)
        load_menu.exec()

    @qtc.Slot()
    def load_from_current_file(self):
        try:
            matrices = self.ctx["f_manager"].load_saved_file(self.ctx["f_manager"].current_file)
            self.ctx["matrices"].clear()
            self.ctx["matrices"] = matrices
            self.update_matrices_ui()
        except IndexError:
            error_message_box = qtw.QMessageBox()
            error_message_box.setWindowTitle("No current file")
            error_message_box.setText("You haven't opened a file yet.")
            error_message_box.setIcon(qtw.QMessageBox.Icon.Critical)
            error_message_box.exec()
        except:
            error_message_box = DefaultErrorMessageBox()
            error_message_box.exec()


    @qtc.Slot()
    def open_save_dialog(self):
        save_menu = SaveMenu(self.ctx)
        save_menu.exec()

    @qtc.Slot()
    def save_to_current_file(self):
        try:
            f_manager.save_to_file(self.ctx["f_manager"].current_file, self.ctx["matrices"])
        except IndexError:
            error_message_box = qtw.QMessageBox()
            error_message_box.setWindowTitle("No current file")
            error_message_box.setText("You haven't opened a file yet.")
            error_message_box.setIcon(qtw.QMessageBox.Icon.Critical)
            error_message_box.exec()
        except:
            error_message_box = DefaultErrorMessageBox()
            error_message_box.exec()

    def _create_algorithm_menu(self):
        algorithm_menu = qtw.QMenu("Algorithms")
        self.menuBar().addMenu(algorithm_menu)

        # menu_bar.addAction(qtw.QWidgetAction(qtw.QLabel("Systems of equations")))

        gaussian_elimination = qtg.QAction(qtg.QIcon("img/gaussian_icon.png"), "Gaussian elimination", self)
        gaussian_elimination.setStatusTip("Solve system of equation using Gaussian Elimination algorithm")
        gaussian_elimination.triggered.connect(self.open_gaussian_menu)
        algorithm_menu.addAction(gaussian_elimination)

    def open_gaussian_menu(self):
        gaussian_menu = PickMatricesDialog(self.ctx, ("A", "b"), "Gaussian Elimination")
        gaussian_menu.args_collected.connect(self.do_gaussian)
        gaussian_menu.exec()

    def do_gaussian(self, matrices: list[np.ndarray]):
        A, b = matrices
        x = gs(A, b)
        x_dialog = MatrixDialog(x)
        x_dialog.theres_matrix.connect(self.append_matrix_in_ui)
        x_dialog.exec()

    def _create_toolbar(self):
        self.toolbar = qtw.QToolBar("Files")
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)

        add_matrix = qtg.QAction(qtg.QIcon("img/add_matrix.png"), "Add a matrix", self)
        add_matrix.setStatusTip("Add a matrix specified by you")
        add_matrix.triggered.connect(self.open_matrix_creator)
        self.toolbar.addAction(add_matrix)

        add_eye = qtg.QAction(qtg.QIcon("img/eye.png"), "Add an eye", self)
        add_eye.setStatusTip("Add an eye to matrices")
        add_eye.triggered.connect(self.open_eye_menu)
        self.toolbar.addAction(add_eye)

    @qtc.Slot()
    def open_matrix_creator(self):
        matrix_creator = MatrixCreator()
        matrix_creator.matrix_created.connect(self.append_matrix_in_ui)
        matrix_creator.exec()

    @qtc.Slot()
    def open_eye_menu(self):
        eye_menu = ShapeDialog("Create an eye")
        eye_menu.commited.connect(self.append_an_eye)
        eye_menu.exec()

    @qtc.Slot()
    def append_an_eye(self, shape: tuple[int, int]):
        w, k = shape
        self.append_matrix_in_ui(np.eye(w, k))

    @qtc.Slot()
    def open_matrix_dialog(self, index: int):
        matrix = self.ctx["matrices"][index]
        matrix_dialog = MatrixDialog(matrix, index)
        matrix_dialog.exec()

f_manager = FileManager()
matrices = None
try:
    matrices = f_manager.load_saved_file(f_manager.current_file)
except:
    matrices = []

ctx: CtxDict = {
    "f_manager": f_manager,
    "matrices": matrices
}

app = qtw.QApplication(sys.argv)

app.setWindowIcon(qtg.QIcon("img/icon.png"))
app.setApplicationName("Matrices.py")

window = Window(ctx)
window.show()

app.exec()





