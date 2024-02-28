import cv2
import numpy as np
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication

# 各种类初始值
red_Circles_num = 0
red_Rectangle_num = 0
orange_Circles_num = 0
orange_Rectangle_num = 0
yellow_Circles_num = 0
yellow_Rectangle_num = 0
green_Circles_num = 0
green_Rectangle_num = 0


font = cv2.FONT_HERSHEY_SIMPLEX
lower_red = np.array([156, 43, 46])
higher_red = np.array([180, 255, 255])
lower_orange = np.array([11, 43, 46])
higher_orange = np.array([25, 255, 255])
lower_yellow = np.array([26, 43, 46])
higher_yellow = np.array([34, 255, 255])
lower_green = np.array([35, 110, 106])  # 绿色阈值下界
higher_green = np.array([77, 255, 255])  # 绿色阈值上界

cap = cv2.VideoCapture(0)  # 打开电脑内置摄像头

if cap.isOpened():
    while 1:
        ret, frame = cap.read()  # 按帧读取，这是读取一帧
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # 用来进行轮廓标记的图像
        imgContour = frame.copy()

        # 灰度转换、模糊、边缘提取
        imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
        imgCanny = cv2.Canny(imgBlur, 60, 70)
        print(imgCanny.shape)

        # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # 把BGR图像转换为HSV格式

        mask_red = cv2.inRange(hsv, lower_red, higher_red)  # 过滤出红色部分，获得红色的掩膜,去掉背景
        mask_red = cv2.medianBlur(mask_red, 7)  # 中值滤波(把数字图像中的一点的值用该点的邻域各点的中值代替，让周围像素值接近真实值，从而消除孤立的噪声点)
        mask_orange = cv2.inRange(hsv, lower_orange, higher_orange)  # 获得橘色部分掩膜
        mask_orange = cv2.medianBlur(mask_orange, 7)
        mask_yellow = cv2.inRange(hsv, lower_yellow, higher_yellow)
        mask_yellow = cv2.medianBlur(mask_yellow, 7)
        mask_green = cv2.inRange(hsv, lower_green, higher_green)
        mask_green = cv2.medianBlur(mask_green, 7)
        # mask = cv2.bitwise_or(mask_red, mask_red)  # 三部分掩膜进行按位或运算

        cnts1, hierarchy1 = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # 轮廓检测
        cnts2, hierarchy2 = cv2.findContours(mask_orange, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cnts3, hierarchy3 = cv2.findContours(mask_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cnts4, hierarchy4 = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


        for cnt in cnts1:
            # 计算各个轮廓包围的面积
            area = cv2.contourArea(cnt)
            print(area)
            # 当面积大于3500时进行处理
            if area > 3500:
                # 画轮廓线（蓝色）
                cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)

                # 将光滑的轮廓线折线化
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

                # 画近似折线 （红色）
                cv2.polylines(imgContour, [approx], True, (11, 150, 255), 2)
                objCor = len(approx)

                # 四条线段时，根据目标包围矩形的宽高比判断是长方形还是正方形
                if objCor <= 6:
                    objectType = "Rectangle"

                # 四条以上线段时为圆形
                elif objCor > 6:
                    objectType = "Circles"

                else:
                    objectType = "None"
                (x, y, w, h) = cv2.boundingRect(cnt) # 该函数返回矩阵四个点
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2) # 将检测到的颜色框起来
                cv2.putText(frame, "red_" + str(objectType), (x + w + 20, y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                            (0, 0, 255), 2)

        for cnt in cnts2:
            area = cv2.contourArea(cnt)
            print(area)
            if area > 3500:

                cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)

                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

                cv2.polylines(imgContour, [approx], True, (0, 0, 255), 2)
                objCor = len(approx)

                if objCor <= 6:
                    objectType = "Rectangle"

                    # 四条以上线段时为圆形
                elif objCor > 6:
                    objectType = "Circles"

                else:
                    objectType = "None"
                (x, y, w, h) = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (11, 150, 255), 2)
                cv2.putText(frame, "orange_" + str(objectType), (x + w + 20, y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (11, 150, 255), 2)

        for cnt in cnts3:
            area = cv2.contourArea(cnt)
            print(area)
            if area > 3500:
                cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)

                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

                cv2.polylines(imgContour, [approx], True, (0, 0, 255), 2)
                objCor = len(approx)

                if objCor <= 6:
                    objectType = "Rectangle"

                    # 四条以上线段时为圆形
                elif objCor > 6:
                    objectType = "Circles"

                else:
                    objectType = "None"
                (x, y, w, h) = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (25, 255, 255), 2)
                cv2.putText(frame, "yellow_" + str(objectType), (x + w + 20, y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (25, 255, 255), 2)

        for cnt in cnts4:
            area = cv2.contourArea(cnt)
            print(area)
            if area > 3500:
                cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)

                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

                cv2.polylines(imgContour, [approx], True, (0, 0, 255), 2)
                objCor = len(approx)

                if objCor <= 6:
                    objectType = "Rectangle"

                    # 四条以上线段时为圆形
                elif objCor > 6:
                    objectType = "Circles"

                else:
                    objectType = "None"
                (x, y, w, h) = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, "Green_" + str(objectType), (x + w + 20, y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)


        cv2.imshow("img", frame)
        cv2.imshow("edge", imgCanny)
        cv2.imshow("shape", imgContour)
        cv2.imshow("red", mask_red)
        k = cv2.waitKey(20) & 0xFF

        if k == 27:
            for cnt in cnts1:
                area = cv2.contourArea(cnt)
                print(area)
                if area > 3500:
                    cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)

                    peri = cv2.arcLength(cnt, True)
                    approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

                    cv2.polylines(imgContour, [approx], True, (11, 150, 255), 2)
                    objCor = len(approx)

                    if objCor <= 6:
                        objectType = "Rectangle"

                        # 四条以上线段时为圆形
                    elif objCor > 6:
                        objectType = "Circles"

                    else:
                        objectType = "None"
                    (x, y, w, h) = cv2.boundingRect(cnt)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.putText(frame, "red_" + str(objectType), (x + w + 20, y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    if ("Circles" == str(objectType)):
                        red_Circles_num += 1
                    if ("Rectangle" == str(objectType)):
                        red_Rectangle_num += 1

            for cnt in cnts2:
                area = cv2.contourArea(cnt)
                print(area)
                if area > 3500:
                    cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
                    peri = cv2.arcLength(cnt, True)
                    approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                    cv2.polylines(imgContour, [approx], True, (0, 0, 255), 2)
                    objCor = len(approx)

                    if objCor <= 6:
                        objectType = "Rectangle"

                        # 四条以上线段时为圆形
                    elif objCor > 6:
                        objectType = "Circles"

                    else:
                        objectType = "None"
                    (x, y, w, h) = cv2.boundingRect(cnt)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (11, 150, 255), 2)
                    cv2.putText(frame, "orange_" + str(objectType), (x + w + 20, y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (11, 150, 255), 2)
                    if ("Circles" == str(objectType)):
                        orange_Circles_num += 1
                    if ("Rectangle" == str(objectType)):
                        orange_Rectangle_num += 1

            for cnt in cnts3:
                area = cv2.contourArea(cnt)
                print(area)
                if area > 3500:
                    cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
                    peri = cv2.arcLength(cnt, True)
                    approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                    cv2.polylines(imgContour, [approx], True, (0, 0, 255), 2)
                    objCor = len(approx)

                    if objCor <= 6:
                        objectType = "Rectangle"

                        # 四条以上线段时为圆形
                    elif objCor > 6:
                        objectType = "Circles"

                    else:
                        objectType = "None"
                    (x, y, w, h) = cv2.boundingRect(cnt)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (25, 255, 255), 2)
                    cv2.putText(frame, "yellow_" + str(objectType), (x + w + 20, y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (25, 255, 255), 2)
                    if ("Circles" == str(objectType)):
                        yellow_Circles_num += 1
                    if ("Rectangle" == str(objectType)):
                        yellow_Rectangle_num += 1

            for cnt in cnts4:
                area = cv2.contourArea(cnt)
                print(area)
                if area > 3500:
                    cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
                    peri = cv2.arcLength(cnt, True)
                    approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                    cv2.polylines(imgContour, [approx], True, (0, 0, 255), 2)
                    objCor = len(approx)

                    if objCor <= 6:
                        objectType = "Rectangle"

                        # 四条以上线段时为圆形
                    elif objCor > 6:
                        objectType = "Circles"

                    else:
                        objectType = "None"
                    (x, y, w, h) = cv2.boundingRect(cnt)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, "Green_" + str(objectType), (x + w + 20, y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    if ("Circles" == str(objectType)):
                        green_Circles_num += 1
                    if ("Rectangle" == str(objectType)):
                        green_Rectangle_num += 1


            break

        from PyQt5 import QtCore, QtGui, QtWidgets


        class Ui_MainWindow(object):
            def __init__(self):
                self.price = None
                self.price = 4 * red_Rectangle_num + \
                             5 * red_Circles_num + \
                             6 * orange_Rectangle_num + \
                             7 * orange_Circles_num + \
                             8 * yellow_Rectangle_num + \
                             9 * yellow_Circles_num + \
                             10 * green_Rectangle_num + \
                             11 * green_Circles_num

                print(self.price)
            def setupUi(self, MainWindow):
                MainWindow.setObjectName("MainWindow")
                MainWindow.resize(765, 500)
                self.centralwidget = QtWidgets.QWidget(MainWindow)
                self.centralwidget.setObjectName("centralwidget")
                self.label_3 = QtWidgets.QLabel(self.centralwidget)
                self.label_3.setGeometry(QtCore.QRect(360, 40, 111, 16))
                self.label_3.setObjectName("label_3")
                self.label_2 = QtWidgets.QLabel(self.centralwidget)
                self.label_2.setGeometry(QtCore.QRect(360, 60, 381, 391))
                self.label_2.setText("")
                self.label_2.setPixmap(QtGui.QPixmap("erweima.png"))
                self.label_2.setObjectName("label_2")
                self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
                self.tableWidget.setGeometry(QtCore.QRect(10, 30, 331,400))
                self.tableWidget.setObjectName("tableWidget")
                self.tableWidget.setColumnCount(2)
                self.tableWidget.setRowCount(9)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setVerticalHeaderItem(0, item)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setVerticalHeaderItem(1, item)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setVerticalHeaderItem(2, item)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setVerticalHeaderItem(3, item)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setVerticalHeaderItem(4, item)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setVerticalHeaderItem(5, item)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setVerticalHeaderItem(6, item)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setVerticalHeaderItem(7, item)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setVerticalHeaderItem(8, item)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setHorizontalHeaderItem(0, item)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setHorizontalHeaderItem(1, item)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(0, 0, item)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(0, 1, item)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(1, 0, item)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(1, 1, item)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(2, 0, item)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(2, 1, item)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(3, 0, item)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(3, 1, item)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(4, 0, item)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(4, 1, item)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(5, 0, item)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(5, 1, item)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(6, 0, item)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(6, 1, item)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(7, 0, item)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(7, 1, item)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(8, 0, item)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(8, 1, item)
                MainWindow.setCentralWidget(self.centralwidget)
                self.menubar = QtWidgets.QMenuBar(MainWindow)
                self.menubar.setGeometry(QtCore.QRect(0, 0, 765, 26))
                self.menubar.setObjectName("menubar")
                MainWindow.setMenuBar(self.menubar)
                self.statusbar = QtWidgets.QStatusBar(MainWindow)
                self.statusbar.setObjectName("statusbar")
                MainWindow.setStatusBar(self.statusbar)

                self.retranslateUi(MainWindow)
                QtCore.QMetaObject.connectSlotsByName(MainWindow)

            def retranslateUi(self, MainWindow):
                _translate = QtCore.QCoreApplication.translate
                MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
                self.label_3.setText(_translate("MainWindow", "请扫码付款"))
                item = self.tableWidget.verticalHeaderItem(0)
                item.setText(_translate("MainWindow", "红色方盘"))
                item = self.tableWidget.verticalHeaderItem(1)
                item.setText(_translate("MainWindow", "红色圆盘"))
                item = self.tableWidget.verticalHeaderItem(2)
                item.setText(_translate("MainWindow", "橙色方盘"))
                item = self.tableWidget.verticalHeaderItem(3)
                item.setText(_translate("MainWindow", "橙色圆盘"))
                item = self.tableWidget.verticalHeaderItem(4)
                item.setText(_translate("MainWindow", "黄色方盘"))
                item = self.tableWidget.verticalHeaderItem(5)
                item.setText(_translate("MainWindow", "黄色圆盘"))
                item = self.tableWidget.verticalHeaderItem(6)
                item.setText(_translate("MainWindow", "绿色方盘"))
                item = self.tableWidget.verticalHeaderItem(7)
                item.setText(_translate("MainWindow", "绿色圆盘"))
                item = self.tableWidget.verticalHeaderItem(8)
                item.setText(_translate("MainWindow", "总价"))
                item = self.tableWidget.horizontalHeaderItem(0)
                item.setText(_translate("MainWindow", "数量（个）"))
                item = self.tableWidget.horizontalHeaderItem(1)
                item.setText(_translate("MainWindow", "单价（元）"))
                __sortingEnabled = self.tableWidget.isSortingEnabled()
                self.tableWidget.setSortingEnabled(False)
                item = self.tableWidget.item(0, 1)
                item.setText(_translate("MainWindow", "4"))
                item = self.tableWidget.item(1, 1)
                item.setText(_translate("MainWindow", "5"))
                item = self.tableWidget.item(2, 1)
                item.setText(_translate("MainWindow", "6"))
                item = self.tableWidget.item(3, 1)
                item.setText(_translate("MainWindow", "7"))
                item = self.tableWidget.item(4, 1)
                item.setText(_translate("MainWindow", "8"))
                item = self.tableWidget.item(5, 1)
                item.setText(_translate("MainWindow", "9"))
                item = self.tableWidget.item(6, 1)
                item.setText(_translate("MainWindow", "10"))
                item = self.tableWidget.item(7, 1)
                item.setText(_translate("MainWindow", "11"))
                self.tableWidget.setSortingEnabled(__sortingEnabled)
                item = self.tableWidget.item(0, 0)
                item.setText(_translate("MainWindow ", str(red_Rectangle_num)))
                item = self.tableWidget.item(1, 0)
                item.setText(_translate("MainWindow ", str(red_Circles_num)))
                item = self.tableWidget.item(2, 0)
                item.setText(_translate("MainWindow ", str(orange_Rectangle_num)))
                item = self.tableWidget.item(3, 0)
                item.setText(_translate("MainWindow ", str(orange_Circles_num)))
                item = self.tableWidget.item(4, 0)
                item.setText(_translate("MainWindow ", str(yellow_Rectangle_num)))
                item = self.tableWidget.item(5, 0)
                item.setText(_translate("MainWindow ", str(yellow_Circles_num)))
                item = self.tableWidget.item(6, 0)
                item.setText(_translate("MainWindow ", str(green_Rectangle_num)))
                item = self.tableWidget.item(7, 0)
                item.setText(_translate("MainWindow ", str(green_Circles_num)))
                item = self.tableWidget.item(8, 1)
                item.setText(_translate("MainWindow ", str(self.price)))
                self.tableWidget.setSortingEnabled(__sortingEnabled)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    widgets = QtWidgets.QMainWindow()
    Ui = Ui_MainWindow()
    Ui.setupUi(widgets)
    widgets.show()
    sys.exit(app.exec_())  # 若不加此语句则程序运行不报错，但是窗口不弹出

cv2.waitKey(0)  # time.sleep()
cv2.destroyAllWindows()