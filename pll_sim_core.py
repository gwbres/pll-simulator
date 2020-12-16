import numpy as np

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

	def step (self):

		# new data
		dut_vco = []
		ref_signal = []

		# ref signal
		ref_signal = sinewave(1, 1/10, size=10)
		
		# vco sim
		for i in range (10):
			[point, self.vco_prev_acc] = dds(10, 0, self.get_quantized_sin_lut(), prev_accumulator=self.vco_prev_acc)
			dut_vco.append(point)

		return [ref_signal, dut_vco]

	def get_work_size (self):
		return self.work_size

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
		return self.get_quantized_sin_cos_lut()[0]
	
	def get_quantized_cos_lut  (self):
		return self.get_quantized_sin_cos_lut()[1]
