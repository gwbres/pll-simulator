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
		self.addPlot(title="Ref. signal", y=[])

		# dut (VCO) signal plot
		self.addPlot(title="DUT (VCO)", y=[])

		#self.nextRow()
		# frequency error plot
		# phase error plot

		# plot customization
		self.get_reference_plot().setClipToView(True)
		#self.get_reference_plot().setRange(xRange=[-100,0])
		#self.get_reference_plot().setLimits(xMax=0)

		# sim core env
		self.core = PllSimCore(work_size=1024, sample_rate=1)

	def get_reference_plot (self):
		return self.getItem(0, 0)

	def get_dut_plot (self):
		return self.getItem(0, 1)

	def run_step (self):
		"""
		Run a simulation step
		"""
		[ref_signal, dut_signal] = self.core.step()
		self.scroll_plot (self.get_reference_plot(), ref_signal)
		self.scroll_plot (self.get_dut_plot(), dut_signal)

	def scroll_plot (self, plot, data):
		"""
		Scrolls given plot, appends given data
		"""
		now = self.core.get_sim_time()
		start = self.core.get_sim_start_time()
		for curve in plot.curves:
			curve.setPos(-(now-start), 0)
			curve.setData(data)

if __name__ == "__main__":
	app = QtGui.QApplication([])
	pg.setConfigOptions(antialias=True)
	
	# gui
	mainWindow = MainWindow()

	# real time simulation
	timer = QtCore.QTimer()
	timer.timeout.connect(mainWindow.run_step)
	timer.start(1000)

	mainWindow.show()

	app.exec_()
