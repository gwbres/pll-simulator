#! /usr/bin/env python3

# pyqt, pyqtgraph
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

# libs
from pll_sim_core import *

class MainWindow (pg.GraphicsLayoutWidget):

	def __init__ (self):
		"""
		MainWindow widget construction method
		"""
		super().__init__(title="title")

		self.resize(1000,600)
		self.setWindowTitle("PLL Simulator")

		# ref signal plot
		self.addPlot(title="Ref. signal", y=[])

		# dut
		self.addPlot(title="DUT (VCO)", y=[])

		self.nextRow()
		# phase / freq errors
		self.addPlot(title="Phase error", y=[])
		self.addPlot(title="Frequency error", y=[])

		# plot customization
		self.get_reference_plot().setClipToView(True)
		#self.get_reference_plot().setRange(xRange=[-100,0])
		#self.get_reference_plot().setLimits(xMax=0)

		# sim core env
		self.core = PllSimCore(work_size=10, sample_rate=1

	def get_reference_plot (self):
		"""
		Returns plot for Reference signal
		"""
		return self.getItem(0, 0)

	def get_dut_plot (self):
		"""
		Returns plot for DUT signal
		"""
		return self.getItem(0, 1)

	def get_phase_error_plot (self):
		"""
		Returns plot for Phase error between DUT & Ref.
		"""
		return self.getItem(1, 0)

	def get_frequency_error_plot (self):
		"""
		Returns plot for Frequency error between DUT & Ref.
		"""
		return self.getItem(1, 1)

	def run_step (self):
		"""
		Run a simulation step
		"""
		[ref_signal, dut_signal] = self.core.step()
		self.scroll_plot (self.get_reference_plot(), ref_signal)
		self.scroll_plot (self.get_dut_plot(), dut_signal)

	def scroll_plot (self, plot, data):
		"""
		Scrolls given plot by appending given data
		""" 
		curve = plot.curves[0]
		prev_data = curve.getData()
		
		if len(prev_data[0]) > 0:
			x0 = prev_data[0][-1] +1
			x = np.concatenate((prev_data[0], range(x0,x0+self.core.get_work_size())))
			y = np.concatenate((prev_data[1], data))
			plot.curves[0].setData(x,y)
		
		else: # first plot
			plot.curves[0].setData(data)

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
