from PySide2.QtCore import QObject, Slot, QPointF, Signal, Property, QThread
import pandas as pd
from circle_fit import CircleFit
from ellipse_fit import EllipseFit
import csv

MINIMUM_POINTS = 5


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
        self.reset_shape()
        self._shape = shape
        self.on_shape.emit()

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

    @Slot(str)
    def save2csv(self, file_name):
        print(file_name)
        name_dict = {
            'X_Center': [self._shape_params[0]],
            'Y_Center': [self._shape_params[1]],
            'Radius': [(self._shape_params[2] + self._shape_params[3]) / 2],
            'Major_axis': [self._shape_params[2]],
            'Minor_axis': [self._shape_params[3]],
            'Angle_of_Rotation': [self._shape_params[4]]
        }

        df = pd.DataFrame(name_dict)
        print(df)
        df.to_csv(file_name + '.csv', index=False)

        '''exp_csv = open(file_name + '.csv', 'w')
        writer = csv.writer(exp_csv)

        writer.writerow(self.shape_params)
        exp_csv.close()'''

    @Slot(str)
    def display_annotation(self, file_name):
        self.reset_shape()
        data = pd.read_csv(file_name + '.csv')
        data_list = [data.columns.values.tolist()] + data.values.tolist()
        params = data_list[1]  # values x_center, y_center, aprox_radius, major_axis, minor_axis, angle
        params.pop(2)
        print(params)
        self.set_shape_params(params)

    on_selected_point = Signal()
    on_shape_params = Signal()
    on_shape = Signal()

    shape = Property(str, get_shape, set_shape, notify=on_shape)
    shape_params = Property('QVariantList', get_shape_params, set_shape_params, notify=on_shape_params)
    selected_points = Property('QVariantList', get_selected_points, set_selected_points, notify=on_selected_point)
