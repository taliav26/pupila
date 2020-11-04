import os
import re
from PySide2.QtCore import QObject, QStringListModel, QUrl, Slot, Signal, Property, QAbstractItemModel


class Viewer(QObject):
    def __init__(self):
        QObject.__init__(self)
        self._selected_file = ""
        self._selected_file_folder = ""
        self._selected_file_siblings = QStringListModel(self)
        self._original_selected_file = ""
        self._supported_file_extensions = r'.png$|.jpg$'
        self._next_file = ""
        self._show_threshold_slider = False
        self._show_gamma_gain_slider = False
        self._show_log_gain_slider = False

    # self._selected_file
    def get_selected_file(self):
        return self._selected_file

    def set_selected_file(self, file):
        if isinstance(file, QUrl):
            self._selected_file = file.toLocalFile()
        elif isinstance(file, str):
            self._selected_file = file
        self.on_selected_file.emit(self._selected_file)
        self._original_selected_file = self._selected_file
        self._detect_selected_file_siblings()
        self._detect_selected_file_next()

    # self._next_file
    def get_next_file(self):
        return self._next_file

    @Slot(str)
    def set_next_file(self, next_file):
        self._next_file = next_file
        self.on_next_file.emit()


    # self._original_selected_file
    def get_original_selected_file(self):
        return self._original_selected_file

    def set_original_selected_file(self, file):
        self._original_selected_file = file

    # self._show_threshold_slider
    def get_show_threshold_slider(self):
        return self._show_threshold_slider

    def set_show_threshold_slider(self, value):
        self._show_threshold_slider = value
        self.on_show_threshold_slider.emit()

    # self._show_gamma_gain_slider
    def get_show_gamma_gain_slider(self):
        return self._show_gamma_gain_slider

    def set_show_gamma_gain_slider(self, value):
        self._show_gamma_gain_slider = value
        self.on_show_gamma_gain_slider.emit()

    # self._show_log_gain_slider
    def get_show_log_gain_slider(self):
        return self._show_log_gain_slider

    def set_show_log_gain_slider(self, value):
        self._show_log_gain_slider = value
        self.on_show_log_gain_slider.emit()

    # self._selected_file_siblings
    def get_selected_file_siblings(self):
        return self._selected_file_siblings

    @Slot(list)
    def set_selected_file_siblings(self, files):
        self._selected_file_siblings.setStringList(files)
        self.on_selected_file_siblings.emit()

    # auxiliary methods
    @Slot(str)
    def set_temp_selected_file(self, temp_file):
        self._selected_file = temp_file
        self.on_selected_file.emit(temp_file)

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
            temp_siblings = sorted(temp_siblings)
            print(temp_siblings)
            self.set_selected_file_siblings(temp_siblings)

    def _detect_selected_file_next(self):
        # Detect next file
        file_siblings = self._selected_file_siblings.stringList()
        current_index = None
        for i, s in enumerate(file_siblings):
            if self._selected_file in s:
                current_index = i
        if current_index is not None and current_index < len(file_siblings) - 1:
            self.set_next_file(file_siblings[current_index + 1])
        else:
            self.set_next_file("")

    # signals
    on_next_file = Signal()
    on_selected_file = Signal(str)
    on_selected_file_siblings = Signal()
    on_show_threshold_slider = Signal()
    on_show_gamma_gain_slider = Signal()
    on_show_log_gain_slider = Signal()

    # properties
    show_threshold_slider = Property(bool, get_show_threshold_slider, set_show_threshold_slider,
                                     notify=on_show_threshold_slider)
    show_gamma_gain_slider = Property(bool, get_show_gamma_gain_slider, set_show_gamma_gain_slider,
                                      notify=on_show_gamma_gain_slider)
    show_log_gain_slider = Property(bool, get_show_log_gain_slider, set_show_log_gain_slider,
                                    notify=on_show_log_gain_slider)
    next_file = Property(str, get_next_file, set_next_file,
                         notify=on_next_file)
    selected_file = Property(QUrl, get_selected_file, set_selected_file,
                             notify=on_selected_file)
    original_selected_file = Property(str, get_original_selected_file, set_original_selected_file,
                                      notify=on_selected_file)
    selected_file_siblings = Property(QAbstractItemModel, get_selected_file_siblings, set_selected_file_siblings,
                                      notify=on_selected_file_siblings)
