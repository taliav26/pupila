# This Python file uses the following encoding: utf-8
import sys
import os
from PySide2 import QtGui
from PySide2.QtQuick import QQuickView
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine

from image_operations import ImageOperations
from shape_fit import ShapeFit
from viewer import Viewer

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    app.setOrganizationName("CENPIS/UO")
    app.setOrganizationDomain("uo.edu.cu")
    app.setApplicationName("Pupil Annotation")
    app.setWindowIcon(QtGui.QIcon('icons/icons8-spreadsheet-file-64.png'))

    view = QQuickView()
    view.setResizeMode(QQuickView.SizeRootObjectToView)
    qml_file = os.path.join(os.path.dirname(__file__), 'view.qml')

    viewer = Viewer()
    shape_fit = ShapeFit()
    image_operations = ImageOperations()

    viewer.on_selected_file.connect(shape_fit.reset_shape)
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("viewer", viewer)
    engine.rootContext().setContextProperty("shape_fit", shape_fit)
    engine.rootContext().setContextProperty("image_op", image_operations)

    engine.load(qml_file)

    shape_fit.on_shape_params.connect(engine.rootObjects()[0].updateEllipse)
    image_operations.result_ready.connect(engine.rootObjects()[0].setTempOutputImage)

    rc = app.exec_()

    sys.exit(rc)
