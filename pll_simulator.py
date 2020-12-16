#! /usr/bin/env python3

# pyqt, pyqtgraph
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

# libs
from pll_sim_core import *

class MainWindow (pg.GraphicsLayoutWidget):

	def __init__ (self):
		super().__init__(title="title")

		self.resize(1000,600)
		self.setWindowTitle("PLL Simulator")

		# ref signal plot
		self.addPlot(title="Ref. signal")

		# dut (VCO) signal plot
		self.addPlot(title="DUT (VCO)")

		#self.nextRow()
		# frequency error plot
		# phase error plot

		# sim core env
		self.core = PllSimCore(work_size=1024, sample_rate=1)

	def get_reference_plot (self):
		return self.getItem(0, 0)

	def get_dut_plot (self):
		return self.getItem(0, 1)

	def run_step (self):
		[ref_signal, dut_vco] = self.core.step()
		print(self.get_reference_plot().curves.getData())
		self.get_reference_plot().plot(ref_signal)
		self.get_dut_plot().plot(dut_vco)

if __name__ == "__main__":
	app = QtGui.QApplication([])
	pg.setConfigOptions(antialias=True)
	
	# gui
	mainWindow = MainWindow()

	# real time simulation
	timer = QtCore.QTimer()
	timer.timeout.connect(mainWindow.run_step)
	timer.start(50)

	mainWindow.show()

	app.exec_()
