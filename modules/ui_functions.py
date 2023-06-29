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
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

from modules.app_settings import Settings
from widgets import CustomGrip

# GLOBALS
# ///////////////////////////////////////////////////////////////
GLOBAL_STATE = False
GLOBAL_TITLE_BAR = True

class UIFunctions(QMainWindow):
	# MAXIMIZE/RESTORE
	# ///////////////////////////////////////////////////////////////

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

	# TOGGLE LEFT BOX
	# ///////////////////////////////////////////////////////////////
	def toggleLeftBox(self, enable):
		if enable:
			# GET WIDTH
			width = self.extraLeftBox.width()
			widthRightBox = self.extraRightBox.width()
			color = Settings.BTN_LEFT_BOX_COLOR

			# GET BTN STYLE
			style = self.toggleLeftBox.styleSheet()

			# SET MAX WIDTH
			if width == 0:
				# SELECT BTN
				self.toggleLeftBox.setStyleSheet(style + color)
				if widthRightBox != 0:
					style = self.settingsTopBtn.styleSheet()
					self.settingsTopBtn.setStyleSheet(style.replace(Settings.BTN_RIGHT_BOX_COLOR, ''))
			else:
				# RESET BTN
				self.toggleLeftBox.setStyleSheet(style.replace(color, ''))
				
		UIFunctions.start_box_animation(self, width, widthRightBox, "left")

	# TOGGLE RIGHT BOX
	# ///////////////////////////////////////////////////////////////
	def toggleRightBox(self, enable):
		if enable:
			# GET WIDTH
			width = self.extraRightBox.width()
			widthLeftBox = self.extraLeftBox.width()
			color = Settings.BTN_RIGHT_BOX_COLOR

			# GET BTN STYLE
			style = self.settingsTopBtn.styleSheet()

			# SET MAX WIDTH
			if width == 0:
				# SELECT BTN
				self.settingsTopBtn.setStyleSheet(style + color)
				if widthLeftBox != 0:
					style = self.toggleLeftBox.styleSheet()
					self.toggleLeftBox.setStyleSheet(style.replace(Settings.BTN_LEFT_BOX_COLOR, ''))
			else:
				# RESET BTN
				self.settingsTopBtn.setStyleSheet(style.replace(color, ''))

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
		self.left_box = QPropertyAnimation(self.extraLeftBox, b"minimumWidth")
		self.left_box.setDuration(Settings.TIME_ANIMATION)
		self.left_box.setStartValue(left_box_width)
		self.left_box.setEndValue(left_width)
		self.left_box.setEasingCurve(QEasingCurve.InOutQuart)

		# ANIMATION RIGHT BOX		
		self.right_box = QPropertyAnimation(self.extraRightBox, b"minimumWidth")
		self.right_box.setDuration(Settings.TIME_ANIMATION)
		self.right_box.setStartValue(right_box_width)
		self.right_box.setEndValue(right_width)
		self.right_box.setEasingCurve(QEasingCurve.InOutQuart)

		# GROUP ANIMATION
		self.group = QParallelAnimationGroup()
		self.group.addAnimation(self.left_box)
		self.group.addAnimation(self.right_box)
		self.group.start()


	# IMPORT THEMES FILES QSS/CSS
	# ///////////////////////////////////////////////////////////////
	def theme(self, file, useCustomTheme):
		if useCustomTheme:
			str = open(file, 'r').read()
			self.styleSheet.setStyleSheet(str)

	# START - GUI DEFINITIONS
	# ///////////////////////////////////////////////////////////////

	def resize_grips(self):
		 # if Settings.ENABLE_CUSTOM_TITLE_BAR:


	# ///////////////////////////////////////////////////////////////
	# END - GUI DEFINITIONS
