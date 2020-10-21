import QtQuick 2.12
import QtQuick.Controls 2.14
import QtQuick.Controls.Material 2.12
import QtQuick.Dialogs 1.0



ApplicationWindow {
    id: window
    width: 900
    height: 520
    visible:true
    title: qsTr("PUPILA: Pupil Annotation")

    function updateEllipse() {
        var context = ellipse_canvas.getContext("2d")
        context.reset()
        if (viewer.ellipse_params.length == 5) {
           ellipse_canvas.requestPaint()
        }
    }

    menuBar: MenuBar {


        Menu {
            title: qsTr("&File")
            Action { text: qsTr("&Open...")
                onTriggered: fileDialog.open()
            }
            Action { text: qsTr("&Save") }
            Action { text: qsTr("Save &As...") }
            MenuSeparator { }
            Action { text: qsTr("&Quit") }
        }
        Menu {
            title: qsTr("&Fit")
            Action { text: qsTr("Ellipse")
                onTriggered:viewer.set_shape("ellipse")
                   }
            Action { text: qsTr("&Circle")
                onTriggered: viewer.set_shape("circle")
            }
            Action { text: qsTr("&Paste") }
        }
        Menu {
            title: qsTr("&Help")
            Action { text: qsTr("&About") }
        }
    }

    SplitView {
        anchors.fill: parent
        orientation: Qt.Horizontal

        Rectangle {
            id: leftItem
            visible: viewer.selected_file.toString() !== ""
            SplitView.minimumWidth: window.width*0.05
            SplitView.preferredWidth: window.width*0.2
            SplitView.maximumWidth: window.width*0.3
            color: "white"
            ScrollView {
                anchors.fill: parent
                ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
                ScrollBar.vertical.policy: ScrollBar.AlwaysOn

                ListView {
                    id: listView
                    model: viewer.selected_file_siblings
                    width: parent.width
                    height: parent.height
                    anchors.fill: parent
                    spacing: 10

                    // The delegate presents the information stored in the model
                    delegate: Rectangle {
                        border.color: Material.color(Material.Grey, (display === viewer.selected_file.toString()) ? Material.Shade700 : Material.Shade300)
                        border.width: (display === viewer.selected_file.toString()) ? 3 : 1
                        width: parent.width
                        height: parent.width * 0.60


                        Image {
                            asynchronous: true
                            fillMode: Image.PreserveAspectCrop
                            source: display
                            width: parent.width - 20
                            height: parent.width * 0.56
                            anchors.centerIn: parent

                            BusyIndicator {
                                running: parent.status === Image.Loading
                                anchors.centerIn: parent
                            }

                        }

                        MouseArea {
                            anchors.fill: parent
                            cursorShape: Qt.PointingHandCursor
                            onClicked: {
                                viewer.selected_file = display

                            }
                        }
                    }
                }
            }

        }

        Rectangle {
            id: centerItem
            SplitView.minimumWidth: window.width*0.6
            SplitView.fillWidth: true
            color: "white"

            Rectangle {
                anchors.fill: parent
                z: dragArea.z+1
                visible: (viewer.selected_file.toString() === "")
                Label {
                    text: qsTr("Arrastra una imagen aquí para abrir")
                    color: Material.color(Material.Grey, Material.Shade400)
                    anchors.centerIn: parent

                }

                    }


            BusyIndicator {
                running: mapImage.status === Image.Loading
                anchors.centerIn: parent
                z: dragArea.z + 4
            }

            Flickable {
                id: flick
                anchors.fill: parent
                clip: true

                Rectangle {
                    id: rect
                    width: mapImage.sourceSize.width
                    height: mapImage.sourceSize.height

                    transform: Scale {
                        id: scaler
                        origin.x: pinchArea.m_x2
                        origin.y: pinchArea.m_y2
                        xScale: pinchArea.m_zoom2
                        yScale: pinchArea.m_zoom2
                    }

                    Repeater {
                       model: viewer.selected_points

                       Canvas{
                            id:points_canvas
                            width: parent.width
                            height: parent.height
                            z: dragArea.z + 50
                            visible: viewer.selected_points.length > 0

                            onPaint: {
                                var context = getContext("2d")
                                context.linewidth = 1
                                context.strokeStyle = Qt.rgba(255, 0, 0, 1)
                                context.fillStyle = Qt.rgba(255, 0, 0, 1);
                                context.arc(modelData.x,modelData.y,2,0,2*Math.PI,false)
                                context.fill()
                                context.stroke()


                            }
                        }
                    }



                    Canvas{
                        id:ellipse_canvas
                        width: parent.width
                        height: parent.height
                        z: dragArea.z + 50
                        visible: viewer.ellipse_params.length > 0

                        onPaint: {
                            var context = getContext("2d")
                            context.reset()
                            context.linewidth = 1
                            context.strokeStyle = Qt.rgba(255, 0, 0, 1)
                            context.save()
                            if(viewer.get_shape() == "ellipse")
                                context.beginPath()
                                context.translate(viewer.ellipse_params[0], viewer.ellipse_params[1])
                                context.rotate(viewer.ellipse_params[4])
                                context.ellipse(-viewer.ellipse_params[2], -viewer.ellipse_params[3], viewer.ellipse_params[2] * 2, viewer.ellipse_params[3] * 2)
                                context.stroke()
                                context.restore()
                                context.moveTo(viewer.ellipse_params[0],viewer.ellipse_params[1]-10)
                                context.lineTo(viewer.ellipse_params[0],viewer.ellipse_params[1]+10)
                                context.moveTo(viewer.ellipse_params[0]-10,viewer.ellipse_params[1])
                                context.lineTo(viewer.ellipse_params[0]+10,viewer.ellipse_params[1])
                                context.stroke()
                            if(viewer.get_shape() == "circle")
                                context.arc(x_centro,y_centro,radio,0,2*Math.PI,false)

                                //ctx.fillStyle = Qt.rgba(1,0,0,0);
                                //ctx.fillRect(0,0,width,height);


                        }
                    }

                    Image {
                        id:mapImage
                        asynchronous: true
                        fillMode: Image.PreserveAspectFit
                        source: viewer.selected_file


                    }


                    PinchArea {
                        id: pinchArea
                        anchors.fill: parent
                        property real m_x1: 0
                        property real m_y1: 0
                        property real m_y2: 0
                        property real m_x2: 0
                        property real m_zoom1: 1
                        property real m_zoom2: 1
                        property real m_max: 2
                        property real m_min: 0.2

                        onPinchStarted: {
                            console.log("Pinch Started")
                            m_x1 = scaler.origin.x
                            m_y1 = scaler.origin.y
                            m_x2 = pinch.startCenter.x
                            m_y2 = pinch.startCenter.y
                            rect.x = rect.x + (pinchArea.m_x1-pinchArea.m_x2)*(1-pinchArea.m_zoom1)
                            rect.y = rect.y + (pinchArea.m_y1-pinchArea.m_y2)*(1-pinchArea.m_zoom1)
                        }
                        onPinchUpdated: {
                            console.log("Pinch Updated")
                            m_zoom1 = scaler.xScale
                            var dz = pinch.scale-pinch.previousScale
                            var newZoom = m_zoom1+dz
                            if (newZoom <= m_max && newZoom >= m_min) {
                                m_zoom2 = newZoom
                            }
                        }
                        MouseArea {
                            id: dragArea
                            hoverEnabled: true
                            anchors.fill: parent
                            drag.target: rect
                            drag.filterChildren: true
                            property var selected_point: Qt.point(mouseX, mouseY)
                            function log_mouse_position() {
                                if(viewer.selected_file.toString() !== "") {
                                    labelStatus.text = " X: " + Math.round(dragArea.mouseX * pinchArea.scale) + " Y: " + Math.round(dragArea.mouseY * pinchArea.scale)
                                }
                            }

                            onClicked: {
                                selected_point.X = Math.round(mouseX * pinchArea.scale)
                                selected_point.Y = Math.round(mouseY * pinchArea.scale)
                                viewer.add_new_point(selected_point)

                            }

                            onMouseXChanged: {
                                log_mouse_position()
                            }

                            onMouseYChanged: {
                                log_mouse_position()
                            }

                            onWheel: {
                                console.log("Wheel Scrolled")
                                pinchArea.m_x1 = scaler.origin.x
                                pinchArea.m_y1 = scaler.origin.y
                                pinchArea.m_zoom1 = scaler.xScale
                                pinchArea.m_x2 = mouseX
                                pinchArea.m_y2 = mouseY

                                var newZoom
                                if (wheel.angleDelta.y > 0) {
                                    newZoom = pinchArea.m_zoom1+0.1
                                    if (newZoom <= pinchArea.m_max) {
                                        pinchArea.m_zoom2 = newZoom
                                    } else {
                                        pinchArea.m_zoom2 = pinchArea.m_max
                                    }
                                } else {
                                    newZoom = pinchArea.m_zoom1-0.1
                                    if (newZoom >= pinchArea.m_min) {
                                        pinchArea.m_zoom2 = newZoom
                                    } else {
                                        pinchArea.m_zoom2 = pinchArea.m_min
                                    }
                                }
                                rect.x = rect.x + (pinchArea.m_x1-pinchArea.m_x2)*(1-pinchArea.m_zoom1)
                                rect.y = rect.y + (pinchArea.m_y1-pinchArea.m_y2)*(1-pinchArea.m_zoom1)

                                console.debug(rect.width+" -- "+rect.height+"--"+rect.scale)

                            }
                        }
                    }
                }
            }
        }

        Rectangle {
            id: rightItem
            visible: viewer.selected_file.toString() !== ""
            SplitView.minimumWidth: window.width*0.2
            SplitView.maximumWidth: window.width*0.3
            color: "white"
            Text {
                text: "Tools panel"
                anchors.centerIn: parent
            }
        }
    }

    Rectangle {
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        height: labelStatus.height
        width: labelStatus.width
        border.color: Material.color(Material.Grey, Material.Shade200)
        color: Material.color(Material.Grey, Material.Shade100)
        visible: labelStatus.text.length > 0
        z: 30
        Label {
            id:labelStatus
            anchors.left: parent.left
            anchors.verticalCenter: parent.verticalCenter
            padding: 5
            elide: Text.ElideRight
            text: ""
        }
    }


    FileDialog{
        id: fileDialog
        title: qsTr("Seleccionar archivo o carpeta")
        nameFilters: [ "Image files (*.jpg *.png *.bmp)" ]
        onAccepted: {

            viewer.selected_file = fileDialog.fileUrl

        }
    }
}


