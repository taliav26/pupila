from PySide2.QtCore import QObject, Signal, Slot
import numpy as np
from skimage.measure import EllipseModel


class EllipseFit(QObject):
    result_ready = Signal(list)
    start_signal = Signal()

    def __init__(self, points, start_signal):
        super(EllipseFit, self).__init__()
        start_signal.connect(self._run)
        self.points = points

    @Slot()
    def _run(self):
        print("ellipse run")

        a_points = np.array(self.points)
        ell = EllipseModel()
        ell.estimate(a_points)
        print("params " + str(ell.params))
        self.result_ready.emit(ell.params)
        self.thread().quit()
