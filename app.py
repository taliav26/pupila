# This Python file uses the following encoding: utf-8
import sys
import os
import re
from PySide2.QtQuick import QQuickView
from PySide2.QtGui import QGuiApplication, QPainter
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtCore import QObject, QUrl, Signal, Slot, Property, QStringListModel, QAbstractItemModel, QPointF, QThread
from ajustes import ellipse_fitting, circle_fitting

MINIMUM_POINTS = 5


class ShapeFit(QObject):
    result_ready = Signal(list)
    start = Signal()

    def __init__(self):
        super(ShapeFit, self).__init__()
        self.start.connect(self.fit_shape)
        self.points = None

    @Slot()
    def fit_shape(self):
        app.processEvents()
        if viewer.get_shape() == "ellipse":
            result = ellipse_fitting(self.points)
            self.result_ready.emit(result)
        if viewer.get_shape() == "circle":
            result = circle_fitting(self.points)
            self.result_ready.emit(result)


class Viewer(QObject):
    def __init__(self):
        QObject.__init__(self)
        self._selected_points = []
        self._selected_file = ""
        self._selected_file_folder = ""
        self._selected_file_siblings = QStringListModel(self)
        self._supported_file_extensions = r'.png$|.jpg$'
        self._shape_params = []
        self._shape = " "

    def get_selected_points(self):
        return self._selected_points

    def get_selected_file(self):
        return self._selected_file

    def get_selected_file_siblings(self):
        return self._selected_file_siblings

    @Slot(QPointF)
    def add_new_point(self, point):
        if len(self._selected_points) == 0:
            self.set_shape_params([])
        if (len(self._selected_points) < MINIMUM_POINTS) & (self._shape != " "):
            self._selected_points.append(point)
            self.on_selected_point.emit()
            print(self._selected_points)
            if (len(self._selected_points) == MINIMUM_POINTS) and self._shape:
                shape_fit.points = [p.toTuple() for p in self._selected_points]
                shape_fit.start.emit()


    def set_selected_points(self, points):
        self._selected_points = points
        self.on_selected_point.emit()

    def set_selected_file(self, file):
        if isinstance(file, QUrl):
            self._selected_file = file.toLocalFile()
        elif isinstance(file, str):
            self.selected_file = file
        self.on_selected_file.emit()
        self.set_shape_params([])
        self.set_selected_points([])
        #        print(self._selected_file)
        self._detect_selected_file_siblings()

    @Slot(list)
    def set_selected_file_siblings(self, files):
        self._selected_file_siblings.setStringList(files)
        self.on_selected_file_siblings.emit()

    def get_shape_params(self):
        return self._shape_params

    @Slot(str)
    def set_shape(self, shape):
        self._shape = shape
        print(self._shape)

    @Slot()
    def get_shape(self):
        return self._shape

    @Slot(list)
    def set_shape_params(self, params):
        print(params)
        self._selected_points = []
        self._shape_params = params
        self.on_shape_params.emit()

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

    on_shape_params = Signal()
    on_selected_file = Signal()
    on_selected_file_siblings = Signal()
    on_selected_point = Signal()
    on_selected_shape = Signal()

    ellipse_params = Property('QVariantList', get_shape_params, set_shape_params, notify=on_shape_params)
    selected_points = Property('QVariantList', get_selected_points, set_selected_points, notify=on_selected_point)
    selected_file = Property(QUrl, get_selected_file, set_selected_file, notify=on_selected_file)
    selected_file_siblings = Property(QAbstractItemModel, get_selected_file_siblings, set_selected_file_siblings,
                                      notify=on_selected_file_siblings)


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)

    app.setOrganizationName("Some Company")
    app.setOrganizationDomain("somecompany.com")
    app.setApplicationName("Amazing Application")

    view = QQuickView()
    view.setResizeMode(QQuickView.SizeRootObjectToView)
    qml_file = os.path.join(os.path.dirname(__file__), 'view.qml')

    viewer = Viewer()

    worker_thread = QThread()
    shape_fit = ShapeFit()
    shape_fit.result_ready.connect(viewer.set_shape_params)
    shape_fit.moveToThread(worker_thread)
    worker_thread.start()

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("viewer", viewer)
    engine.load(qml_file)

    viewer.on_shape_params.connect(engine.rootObjects()[0].updateEllipse)

    rc = app.exec_()
    worker_thread.quit()
    worker_thread.wait()
    sys.exit(rc)
