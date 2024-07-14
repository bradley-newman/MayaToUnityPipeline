from PySide2.QtCore import QObject
from PySide2.QtWidgets import QWidget, QLayout, QToolBar

__all__ = ["scale_qobjects", "print_qobject_tree"]


def scale_qobjects(objs: list[QObject], scale_value: int):
    if scale_value > 1:
        for obj in objs:
            if isinstance(obj, QToolBar):
                toolbar = obj
                toolbar.setIconSize(toolbar.iconSize() * scale_value)
            elif isinstance(obj, QWidget):
                obj.setMinimumSize(obj.minimumWidth() * scale_value, obj.minimumHeight() * scale_value)
            elif isinstance(obj, QLayout):
                margins = list(obj.getContentsMargins())
                margins = [float(margin) for margin in margins]

                for i in range(len(margins)):
                    margins[i] *= scale_value

                margins = [round(margin) for margin in margins]
                obj.setContentsMargins(margins[0], margins[1], margins[2], margins[3])


def print_qobject_tree(qobject, indent=4):
    for child in qobject.children():
        if hasattr(child, 'isVisible'):
            print("  " * indent + str(child) + ", isVisible: " + str(child.isVisible()))
        else:
            print("  " * indent + str(child))
        print_qobject_tree(child, indent + 1)
