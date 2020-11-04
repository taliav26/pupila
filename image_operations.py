from PySide2.QtCore import QObject, Signal, Slot, Property
from skimage import exposure
from skimage import io
from skimage.filters import threshold_otsu


class ImageOperations(QObject):
    def __init__(self, ):
        super(ImageOperations, self).__init__()
        self._temp_output_name = ""
        self._temp_output_name_base = "_temp_output"
        self._temp_output_id = 0
        self._temp_output_ext = ".jpg"
        self._optimal_threshold = 0
        self.generate_temp_output_name()

    # self._temp_output_name
    def get_temp_output_name(self):
        return self._temp_output_name

    def set_temp_output_name(self, temp_name):
        self._temp_output_name = temp_name

    # self._optimal_threshold
    def get_optimal_threshold(self):
        return self._optimal_threshold

    def set_optimal_threshold(self, thresh):
        self._optimal_threshold = thresh
        self.on_optimal_threshold_ready.emit()

    # auxiliary methods
    def generate_temp_output_name(self):
        self._temp_output_id = int(not self._temp_output_id)
        self.set_temp_output_name(self._temp_output_name_base + str(self._temp_output_id) + self._temp_output_ext)

    @Slot(str)
    def histogram_eq(self, image_path):
        self.generate_temp_output_name()
        img = io.imread(image_path)
        img_eq = exposure.equalize_hist(img)
        io.imsave(self._temp_output_name, (img_eq * 255).astype("uint8"))
        self.result_ready.emit()

    @Slot(str, int)
    def threshold(self, image_path, threshold):
        self.generate_temp_output_name()
        img = io.imread(image_path)
        binary = img > threshold
        io.imsave(self._temp_output_name, binary.astype("uint8") * 255)
        self.result_ready.emit()

    @Slot(str, int)
    def gamma(self, image_path, gain):
        self.generate_temp_output_name()
        img = io.imread(image_path)
        gamma_corrected = exposure.adjust_gamma(img, gain)
        io.imsave(self._temp_output_name, (gamma_corrected * 255).astype("uint8"))
        self.result_ready.emit()

    @Slot(str, int)
    def logarithmic(self, image_path, gain):
        self.generate_temp_output_name()
        img = io.imread(image_path)
        logarithmic_corrected = exposure.adjust_log(img, gain)
        io.imsave(self._temp_output_name, (logarithmic_corrected * 255).astype("uint8"))
        self.result_ready.emit()

    @Slot(str)
    def detect_optimal_threshold(self, image_path):
        img = io.imread(image_path)
        self.set_optimal_threshold(threshold_otsu(img))

    # signals
    result_ready = Signal()
    on_optimal_threshold_ready = Signal()

    # properties
    temp_output_name = Property(str, get_temp_output_name, set_temp_output_name, notify=result_ready)
    optimal_threshold = Property(int, get_optimal_threshold, set_optimal_threshold, notify=on_optimal_threshold_ready)
