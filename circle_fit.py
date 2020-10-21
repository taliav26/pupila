from PySide2.QtCore import QObject, Signal, Slot
import numpy as np
from skimage.measure import CircleModel


class CircleFit(QObject):
    result_ready = Signal(list)
    start_signal = Signal()

    def __init__(self, points, start_signal):
        super(CircleFit, self).__init__()
        start_signal.connect(self._run)
        self.points = points

    @Slot()
    def _run(self):

        a_points = np.array(self.points)
        cir = CircleModel()
        cir.estimate(a_points)

        self.result_ready.emit(cir.params)
        self.thread().quit()
