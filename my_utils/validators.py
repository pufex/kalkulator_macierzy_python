import PySide6.QtGui as qtg

class ShapeValidator(qtg.QValidator):
    def __init__(self):
        super().__init__()

    def validate(self, text: str, pos: int):
        try:
            if text == "":
                return qtg.QValidator.State.Intermediate, text, pos

            number = int(text)
            if number < 1 or number > 99:
                raise ValueError
        except:
            return qtg.QValidator.State.Invalid, text, pos
        else:
            return qtg.QValidator.State.Acceptable, text, pos

class ValueValidator(qtg.QValidator):
    def __init__(self):
        super().__init__()

    def validate(self, text: str, pos: int):
        try:
            if text == "":
                return qtg.QValidator.State.Intermediate
            float(text)
        except:
            return qtg.QValidator.State.Invalid
        else:
            return qtg.QValidator.State.Acceptable

shape_validator = ShapeValidator()
value_validator = ValueValidator()