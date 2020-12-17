# maths
import numpy as np

# qt
import pyqtgraph as pg

# libs
from signal import sinewave, dds 

class PllSimCore (object):

	def __init__ (self, work_size=1024, sample_rate=1):
		"""
		Initializes PllSimCore object
		based on given sample rate [Hz]
		work_size: chunk size to work with
		"""
		self.work_size = work_size
		self.sample_rate = sample_rate

		# Quantized Sine/Cosine LUT
		axis = np.linspace(0, 2*np.pi, num=1024) 
		self.sine_cos_lut = [np.sin(axis), np.cos(axis)]

		# DUT VCO params
		self.vco_prev_acc = 0

		# sim time
		self.sim_start_time = pg.ptime.time()

	def step (self, open_loop=True):
		"""
		Take one step into the simulation
		Generates new Reference signal chunk
		Produces new DUT signal chunk in open or closed loop
		Deduces new phase & frequency errors
		"""

		# new data
		dut_vco = []
		ref_signal = []

		mean_freq = 10 # [Hz]

		# ref signal
		ref_signal = sinewave(1, 1/mean_freq, size=self.work_size)
		
		# generate a couple samples from the VCO
		for i in range (self.work_size):
			[point, self.vco_prev_acc] = dds(0.1, 0, self.get_quantized_sin_lut(), prev_accumulator=self.vco_prev_acc)
			dut_vco.append(point)

		# determine new phase, freq errors
		

		return [ref_signal, dut_vco]

	def get_work_size (self):
		"""
		Returns nb of samples per simulation steps
		"""
		return self.work_size

	def get_sim_step_duration (self):
		"""
		Returns time duration that a simulation step represents
		"""
		return self.work_size * 1.0/self.sample_rate

	def get_sample_rate (self):
		"""
		Returns sample rate [Hz]
		"""
		return self.sample_rate

	def get_quantized_sin_cos_lut (self):
		"""
		Returns quantized Sine/Cosine lut
		"""
		return self.sine_cos_lut

	def get_quantized_sin_lut  (self):
		"""
		Returns quantized Sin(x) lut to be used
		in this simulation,
		based on DDS implementation settings
		"""
		return self.get_quantized_sin_cos_lut()[0]
	
	def get_quantized_cos_lut  (self):
		"""
		Returns quantized Cos(x) lut to be used
		in this simulation,
		based on DDS implementation settings
		"""
		return self.get_quantized_sin_cos_lut()[1]
	
	def get_sim_start_time (self):
		"""
		Returns time where simulation was started 
		for easy plotting
		"""
		return self.sim_start_time

	def get_sim_time (self):
		"""
		Returns current 'time' in simulation
		"""
		return pg.ptime.time() - self.get_sim_start_time()
