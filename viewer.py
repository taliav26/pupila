import os
import re
from PySide2.QtCore import QObject, QStringListModel, QUrl, Slot, Signal, Property, QAbstractItemModel


class Viewer(QObject):
    def __init__(self):
        QObject.__init__(self)
        self._selected_file = ""
        self._selected_file_folder = ""
        self._selected_file_siblings = QStringListModel(self)
        self._supported_file_extensions = r'.png$|.jpg$'

    def get_selected_file(self):
        return self._selected_file

    def get_selected_file_siblings(self):
        return self._selected_file_siblings

    def set_selected_file(self, file):
        if isinstance(file, QUrl):
            self._selected_file = file.toLocalFile()
        elif isinstance(file, str):
            self.selected_file = file
        self.on_selected_file.emit()
        # shape_fit.set_shape_params([])
        # shape_fit.set_selected_points([])
        # print(self._selected_file)
        self._detect_selected_file_siblings()

    @Slot(list)
    def set_selected_file_siblings(self, files):
        self._selected_file_siblings.setStringList(files)
        self.on_selected_file_siblings.emit()

    def _detect_selected_file_siblings(self):
        if self._selected_file_folder != os.path.dirname(self._selected_file):
            self._selected_file_folder = os.path.dirname(self._selected_file)
            temp_siblings = []
            with os.scandir(self._selected_file_folder) as d:
                for entry in d:
                    if entry.is_file() and re.search(self._supported_file_extensions, entry.name):
                        # if entry.name != self._selected_file:
                        file_path = os.path.abspath(os.path.join(self._selected_file_folder, entry.name))
                        temp_siblings.append(file_path)
            # print(temp_siblings)
            self.set_selected_file_siblings(temp_siblings)

    on_selected_file = Signal()
    on_selected_file_siblings = Signal()

    selected_file = Property(QUrl, get_selected_file, set_selected_file, notify=on_selected_file)
    selected_file_siblings = Property(QAbstractItemModel, get_selected_file_siblings, set_selected_file_siblings,
                                      notify=on_selected_file_siblings)
