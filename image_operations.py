from PySide2.QtCore import QObject, Signal, Slot
from skimage import exposure
from skimage import io


class ImageOperations(QObject):
    hist_eq_result = Signal()

    def __init__(self, ):
        super(ImageOperations, self).__init__()
        self._temp_image_path = ""

    @Slot(str)
    def histogram_eq(self, image_path):
        img = io.imread(image_path)
        img_eq = exposure.equalize_hist(img)
        io.imsave("output.jpg", (img_eq * 256).astype("uint8"))
        self.hist_eq_result.emit()
