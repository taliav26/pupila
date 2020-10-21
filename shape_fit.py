from PySide2.QtCore import QObject, Slot, QPointF, Signal, Property, QThread

from circle_fit import CircleFit
from ellipse_fit import EllipseFit

MINIMUM_POINTS = 5

global app


class ShapeFit(QObject):

    def __init__(self):
        super(ShapeFit, self).__init__()
        self._selected_points = []
        self._shape_params = []
        self._shape = ""
        self.worker_thread = None

    def get_selected_points(self):
        return self._selected_points

    def set_selected_points(self, points):
        self._selected_points = points
        self.on_selected_point.emit()

    def get_shape_params(self):
        return self._shape_params

    @Slot(list)
    def set_shape_params(self, params):
        if len(params) == 3 and self._shape == "circle":
            params = [float(params[0]), float(params[1]), float(params[2]), float(params[2]), 0]
        print(params)
        self._selected_points = []
        self._shape_params = params
        self.on_shape_params.emit()

    @Slot()
    def reset_shape(self):
        self.set_shape_params([])
        self.set_selected_points([])
    @Slot()
    def get_shape(self):
        return self._shape

    @Slot(str)
    def set_shape(self, shape):
        self._shape = shape
        print(self._shape)

    @Slot(QPointF)
    def add_new_point(self, point):
        if self._shape:
            if len(self._selected_points) == 0:
                self.set_shape_params([])
            if len(self._selected_points) < MINIMUM_POINTS:
                self._selected_points.append(point)
                self.on_selected_point.emit()
                print(self._selected_points)
                if len(self._selected_points) == MINIMUM_POINTS:
                    self.fit_shape()

    def fit_shape(self):
        self.worker_thread = QThread()
        points = [p.toTuple() for p in self._selected_points]

        if self._shape == "ellipse":
            shape = EllipseFit(points=points, start_signal=self.worker_thread.started)
        elif self._shape == "circle":
            shape = CircleFit(points=points, start_signal=self.worker_thread.started)
        else:
            return

        shape.result_ready.connect(self.set_shape_params)
        shape.moveToThread(self.worker_thread)
        self.worker_thread.start()
        QThread.msleep(1)

    on_selected_point = Signal()
    on_shape_params = Signal()

    selected_points = Property('QVariantList', get_selected_points, set_selected_points, notify=on_selected_point)
    ellipse_params = Property('QVariantList', get_shape_params, set_shape_params, notify=on_shape_params)