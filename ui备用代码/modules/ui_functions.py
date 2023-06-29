# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

# MAIN FILE
# ///////////////////////////////////////////////////////////////
from main import *

# GLOBALS
# ///////////////////////////////////////////////////////////////
GLOBAL_STATE = False
GLOBAL_TITLE_BAR = True

class UIFunctions(MainWindow):
    # MAXIMIZE/RESTORE
    # ///////////////////////////////////////////////////////////////
    def maximize_restore(self):
        global GLOBAL_STATE
        status = GLOBAL_STATE
        if status == False:
            self.showMaximized()
            GLOBAL_STATE = True
            self.ui.appMargins.setContentsMargins(0, 0, 0, 0)
            self.ui.maximizeRestoreAppBtn.setToolTip("Restore")
            self.ui.maximizeRestoreAppBtn.setIcon(QIcon(u":/icons/images/icons/icon_restore.png"))
            self.ui.frame_size_grip.hide()
            self.left_grip.hide()
            self.right_grip.hide()
            self.top_grip.hide()
            self.bottom_grip.hide()
        else:
            GLOBAL_STATE = False
            self.showNormal()
            self.resize(self.width()+1, self.height()+1)
            self.ui.appMargins.setContentsMargins(10, 10, 10, 10)
            self.ui.maximizeRestoreAppBtn.setToolTip("Maximize")
            self.ui.maximizeRestoreAppBtn.setIcon(QIcon(u":/icons/images/icons/icon_maximize.png"))
            self.ui.frame_size_grip.show()
            self.left_grip.show()
            self.right_grip.show()
            self.top_grip.show()
            self.bottom_grip.show()

    # RETURN STATUS
    # ///////////////////////////////////////////////////////////////
    def returStatus(self):
        return GLOBAL_STATE

    # SET STATUS
    # ///////////////////////////////////////////////////////////////
    def setStatus(self, status):
        global GLOBAL_STATE
        GLOBAL_STATE = status

    # TOGGLE MENU
    # ///////////////////////////////////////////////////////////////
    def toggleMenu(self, enable):
        if enable:
            # GET WIDTH
            width = self.ui.leftMenuBg.width()
            maxExtend = Settings.MENU_WIDTH
            standard = 60

            # SET MAX WIDTH
            if width == 60:
                widthExtended = maxExtend
            else:
                widthExtended = standard

            # ANIMATION
            self.animation = QPropertyAnimation(self.ui.leftMenuBg, b"minimumWidth")
            self.animation.setDuration(Settings.TIME_ANIMATION)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QEasingCurve.InOutQuart)
            self.animation.start()

    # TOGGLE LEFT BOX
    # ///////////////////////////////////////////////////////////////
    def toggleLeftBox(self, enable):
        if enable:
            # GET WIDTH
            width = self.ui.extraLeftBox.width()
            widthRightBox = self.ui.extraRightBox.width()
            maxExtend = Settings.LEFT_BOX_WIDTH
            color = Settings.BTN_LEFT_BOX_COLOR
            standard = 0

            # GET BTN STYLE
            style = self.ui.toggleLeftBox.styleSheet()

            # SET MAX WIDTH
            if width == 0:
                widthExtended = maxExtend
                # SELECT BTN
                self.ui.toggleLeftBox.setStyleSheet(style + color)
                if widthRightBox != 0:
                    style = self.ui.settingsTopBtn.styleSheet()
                    self.ui.settingsTopBtn.setStyleSheet(style.replace(Settings.BTN_RIGHT_BOX_COLOR, ''))
            else:
                widthExtended = standard
                # RESET BTN
                self.ui.toggleLeftBox.setStyleSheet(style.replace(color, ''))
                
        UIFunctions.start_box_animation(self, width, widthRightBox, "left")

    # TOGGLE RIGHT BOX
    # ///////////////////////////////////////////////////////////////
    def toggleRightBox(self, enable):
        if enable:
            # GET WIDTH
            width = self.ui.extraRightBox.width()
            widthLeftBox = self.ui.extraLeftBox.width()
            maxExtend = Settings.RIGHT_BOX_WIDTH
            color = Settings.BTN_RIGHT_BOX_COLOR
            standard = 0

            # GET BTN STYLE
            style = self.ui.settingsTopBtn.styleSheet()

            # SET MAX WIDTH
            if width == 0:
                widthExtended = maxExtend
                # SELECT BTN
                self.ui.settingsTopBtn.setStyleSheet(style + color)
                if widthLeftBox != 0:
                    style = self.ui.toggleLeftBox.styleSheet()
                    self.ui.toggleLeftBox.setStyleSheet(style.replace(Settings.BTN_LEFT_BOX_COLOR, ''))
            else:
                widthExtended = standard
                # RESET BTN
                self.ui.settingsTopBtn.setStyleSheet(style.replace(color, ''))

            UIFunctions.start_box_animation(self, widthLeftBox, width, "right")

    def start_box_animation(self, left_box_width, right_box_width, direction):
        right_width = 0
        left_width = 0 

        # Check values
        if left_box_width == 0 and direction == "left":
            left_width = 240
        else:
            left_width = 0
        # Check values
        if right_box_width == 0 and direction == "right":
            right_width = 240
        else:
            right_width = 0       

        # ANIMATION LEFT BOX        
        self.left_box = QPropertyAnimation(self.ui.extraLeftBox, b"minimumWidth")
        self.left_box.setDuration(Settings.TIME_ANIMATION)
        self.left_box.setStartValue(left_box_width)
        self.left_box.setEndValue(left_width)
        self.left_box.setEasingCurve(QEasingCurve.InOutQuart)

        # ANIMATION RIGHT BOX        
        self.right_box = QPropertyAnimation(self.ui.extraRightBox, b"minimumWidth")
        self.right_box.setDuration(Settings.TIME_ANIMATION)
        self.right_box.setStartValue(right_box_width)
        self.right_box.setEndValue(right_width)
        self.right_box.setEasingCurve(QEasingCurve.InOutQuart)

        # GROUP ANIMATION
        self.group = QParallelAnimationGroup()
        self.group.addAnimation(self.left_box)
        self.group.addAnimation(self.right_box)
        self.group.start()

    # SELECT/DESELECT MENU
    # ///////////////////////////////////////////////////////////////
    # SELECT
    def selectMenu(getStyle):
        select = getStyle + Settings.MENU_SELECTED_STYLESHEET
        return select

    # DESELECT
    def deselectMenu(getStyle):
        deselect = getStyle.replace(Settings.MENU_SELECTED_STYLESHEET, "")
        return deselect

    # START SELECTION
    def selectStandardMenu(self, widget):
        for w in self.ui.topMenu.findChildren(QPushButton):
            if w.objectName() == widget:
                w.setStyleSheet(UIFunctions.selectMenu(w.styleSheet()))

    # RESET SELECTION
    def resetStyle(self, widget):
        for w in self.ui.topMenu.findChildren(QPushButton):
            if w.objectName() != widget:
                w.setStyleSheet(UIFunctions.deselectMenu(w.styleSheet()))

    # IMPORT THEMES FILES QSS/CSS
    # ///////////////////////////////////////////////////////////////
    def theme(self, file, useCustomTheme):
        if useCustomTheme:
            str = open(file, 'r').read()
            self.ui.styleSheet.setStyleSheet(str)

    # START - GUI DEFINITIONS
    # ///////////////////////////////////////////////////////////////
    def uiDefinitions(self):
        def dobleClickMaximizeRestore(event):
            # IF DOUBLE CLICK CHANGE STATUS
            if event.type() == QEvent.MouseButtonDblClick:
                QTimer.singleShot(250, lambda: UIFunctions.maximize_restore(self))
        self.ui.titleRightInfo.mouseDoubleClickEvent = dobleClickMaximizeRestore

        if Settings.ENABLE_CUSTOM_TITLE_BAR:
            #STANDARD TITLE BAR
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)

            # MOVE WINDOW / MAXIMIZE / RESTORE
            def moveWindow(event):
                # IF MAXIMIZED CHANGE TO NORMAL
                if UIFunctions.returStatus(self):
                    UIFunctions.maximize_restore(self)
                # MOVE WINDOW
                if event.buttons() == Qt.LeftButton:
                    self.move(self.pos() + event.globalPos() - self.dragPos)
                    self.dragPos = event.globalPos()
                    event.accept()
            self.ui.titleRightInfo.mouseMoveEvent = moveWindow

            # CUSTOM GRIPS
            self.left_grip = CustomGrip(self, Qt.LeftEdge, True)
            self.right_grip = CustomGrip(self, Qt.RightEdge, True)
            self.top_grip = CustomGrip(self, Qt.TopEdge, True)
            self.bottom_grip = CustomGrip(self, Qt.BottomEdge, True)

        else:
            self.ui.appMargins.setContentsMargins(0, 0, 0, 0)
            self.ui.minimizeAppBtn.hide()
            self.ui.maximizeRestoreAppBtn.hide()
            self.ui.closeAppBtn.hide()
            self.ui.frame_size_grip.hide()

        # DROP SHADOW
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(17)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.ui.bgApp.setGraphicsEffect(self.shadow)

        # RESIZE WINDOW
        self.sizegrip = QSizeGrip(self.ui.frame_size_grip)
        self.sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")

        # MINIMIZE
        self.ui.minimizeAppBtn.clicked.connect(lambda: self.showMinimized())

        # MAXIMIZE/RESTORE
        self.ui.maximizeRestoreAppBtn.clicked.connect(lambda: UIFunctions.maximize_restore(self))

        # CLOSE APPLICATION
        self.ui.closeAppBtn.clicked.connect(lambda: self.close())

    def resize_grips(self):
        if Settings.ENABLE_CUSTOM_TITLE_BAR:
            self.left_grip.setGeometry(0, 10, 10, self.height())
            self.right_grip.setGeometry(self.width() - 10, 10, 10, self.height())
            self.top_grip.setGeometry(0, 0, self.width(), 10)
            self.bottom_grip.setGeometry(0, self.height() - 10, self.width(), 10)

    # ///////////////////////////////////////////////////////////////
    # END - GUI DEFINITIONS



import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from ui import ui_main_win

# 主窗口
class main_win(QWidget):

    def __init__(self,parent = None):

        # 从文件中加载UI定义
        super(main_win, self).__init__(parent)
        self.ui = ui_main_win.Ui_Form()
        self.ui.setupUi(self)

        self.setWindowFlag(Qt.FramelessWindowHint)		#将界面设置为无框
        self.setAttribute(Qt.WA_TranslucentBackground)	#将界面属性设置为半透明
        self.shadow = QGraphicsDropShadowEffect()		#设定一个阴影,半径为 4,颜色为 2, 10, 25,偏移为 0,0
        self.shadow.setBlurRadius(4)
        self.shadow.setColor(QColor(2, 10, 25))
        self.shadow.setOffset(0, 0)
        self.ui.frame.setGraphicsEffect(self.shadow)	#为frame设定阴影效果

        # 按钮绑定退出信号
        # self.ui.pushButton_2.clicked.connect(app.quit)
        # 更改按钮为绑定关闭窗口信号
        self.ui.pushButton_2.clicked.connect(self.close)

        # 开启鼠标跟踪后，鼠标离开窗口或进入窗口会触发 mouseMoveEvent 事件
        self.setMouseTracking(True)
        # 初始化各扳机的状态
        self.initDrag()
        # 主窗口绑定事件过滤器
        self.ui.frame.installEventFilter(self)  # 初始化事件过滤器

        # 托盘菜单初始化
        self.tray_icon()


#   -------------------------------------------------托盘菜单功能-----------------------------------------------

    # 托盘菜单初始化
    def tray_icon(self):
        # 创建菜单的项目，并连接对应信号
        self.create_actions()
        # 把项目添加到菜单中( QMenu(self) )
        self.create_tray_icon()

    # 创建菜单的项目，并连接对应信号
    def create_actions(self):

        self._restore_action = QAction("显示主界面")
        self._restore_action.triggered.connect(self.showNormal)

        self._quit_action = QAction("退出")
        self._quit_action.triggered.connect(self.app_quit)

    # 把项目添加到菜单中( QMenu(self) )
    def create_tray_icon(self):
        self._tray_icon_menu = QMenu(self)
        self._tray_icon_menu.addAction(self._restore_action)
        # 添加分隔符
        self._tray_icon_menu.addSeparator()
        self._tray_icon_menu.addAction(self._quit_action)
        # 设置托盘图标，图片必须为正方形
        self._tray_icon = QSystemTrayIcon()
        self._tray_icon.setIcon(QIcon(r'img\logo.png'))
        self._tray_icon.setContextMenu(self._tray_icon_menu)

        # 在系统托盘显示此对象
        self._tray_icon.show()

        # 动作信号
        self._tray_icon.activated.connect(self.iconActivated)

    # 动作信号
    def iconActivated(self,reason):
        # 输出在鼠标在托盘图标上的动作
        print(reason)

        # 双击
        if reason == QSystemTrayIcon.DoubleClick:

            if self._tray_icon.isVisible():
                self.showNormal()

        # 右击
        if reason == QSystemTrayIcon.Context:

            if self._tray_icon.isVisible():
                # 菜单跟随鼠标
                self._tray_icon_menu.exec(QPoint(QCursor.pos().x() - 55 ,QCursor.pos().y() - 90))
            else:
                self.hide()

    # 退出
    def app_quit(self):
        # 先释放资源再退出，用于解决退出后图标不消失的问题
        self._restore_action = None
        self._quit_action = None
        self._tray_icon = None
        self._tray_icon_menu = None
        app.quit()

#   -------------------------------------------------事件过滤器-------------------------------------------------

    def eventFilter(self, obj, event):
        # 事件过滤器,用于解决鼠标进入其它控件后还原为标准鼠标样式
        if isinstance(event, QEnterEvent):
            self.setCursor(Qt.ArrowCursor)
        return super().eventFilter(obj, event)


#   -----------------------------------------------移动与拉伸功能------------------------------------------------

    # 初始化各扳机的状态
    def initDrag(self):
        self._move_drag = False
        self._corner_drag = False
        self._bottom_drag = False
        self._right_drag = False

    # 鼠标按下所执行的功能
    def mousePressEvent(self, event):
        # globalPos为鼠标位置 , pos 为窗口的位置 , m_Position 为鼠标在窗口中的位置  .x() .y() 获取事件中的坐标

        # 移动事件
        if event.button() == Qt.LeftButton and (event.globalPos() - self.pos()).x() < self.ui.frame.size().width() and (event.globalPos() - self.pos()).y() < self.ui.frame.size().height():
            self._move_drag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()

        # 右下角边界拉伸事件
        if event.button() == Qt.LeftButton and (event.globalPos() - self.pos()).x() > self.ui.frame.size().width() and (event.globalPos() - self.pos()).y() > self.ui.frame.size().height():
            self._corner_drag = True
            event.accept()

        # 下边界拉伸事件
        if event.button() == Qt.LeftButton and (event.globalPos() - self.pos()).x() < self.ui.frame.size().width() and (event.globalPos() - self.pos()).y() > self.ui.frame.size().height():
            self._bottom_drag = True
            event.accept()

        # 右边界拉伸事件
        if event.button() == Qt.LeftButton and (event.globalPos() - self.pos()).x() > self.ui.frame.size().width() and (event.globalPos() - self.pos()).y() < self.ui.frame.size().height():
            self._right_drag = True
            event.accept()

    # 鼠标移动所执行的功能
    def mouseMoveEvent(self, QMouseEvent):

        # 移动事件
        if Qt.LeftButton and self._move_drag:
            self.move(QMouseEvent.globalPos() - self.m_Position)
            QMouseEvent.accept()

        # 右下角边界拉伸事件
        if Qt.LeftButton and self._corner_drag:
            self.resize(QMouseEvent.pos().x()+10 , QMouseEvent.pos().y()+10)
            QMouseEvent.accept()

        # 下边界拉伸事件
        if Qt.LeftButton and self._bottom_drag:
            self.resize(self.width() , QMouseEvent.pos().y()+10)
            QMouseEvent.accept()

        # 右边界拉伸事件
        if Qt.LeftButton and self._right_drag:
            self.resize(QMouseEvent.pos().x()+10 , self.height())
            QMouseEvent.accept()

        # 获取鼠标在窗口中的位置来改变鼠标的图标
        # 右下角边界光标事件
        if (QMouseEvent.globalPos() - self.pos()).x() > self.ui.frame.size().width() and (QMouseEvent.globalPos() - self.pos()).y() > self.ui.frame.size().height():
            self.setCursor(Qt.SizeFDiagCursor)

        # 下边界光标事件
        elif (QMouseEvent.globalPos() - self.pos()).x() < self.ui.frame.size().width() and (QMouseEvent.globalPos() - self.pos()).y() > self.ui.frame.size().height():
            self.setCursor(Qt.SizeVerCursor)

        # 右边界光标事件
        elif (QMouseEvent.globalPos() - self.pos()).x() > self.ui.frame.size().width() and (QMouseEvent.globalPos() - self.pos()).y() < self.ui.frame.size().height():
            self.setCursor(Qt.SizeHorCursor)
        # 正常光标事件
        else:
            self.setCursor(Qt.ArrowCursor)

    # 鼠标弹起后，恢复各扳机的状态
    def mouseReleaseEvent(self, QMouseEvent):
        self._move_drag = False
        self._corner_drag = False
        self._bottom_drag = False
        self._right_drag = False


if __name__ == '__main__':
    # 每一个 PySide6 应用都必须创建一个应用对象
    app = QApplication([])

    # 设置窗口图标：按下 Alt + Tab 能够看到的图标，图片必须为正方形
    app.setWindowIcon(QIcon(r'img\logo.png'))

    # 检测当前系统是否支持托盘功能
    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(None, "系统托盘", "本系统检测不出系统托盘")
        sys.exit(1)

    # 使得程序能在后台运行，关闭最后一个窗口不退出程序
    QApplication.setQuitOnLastWindowClosed(False)

    main_win = main_win()
    main_win.show()
    sys.exit(app.exec())