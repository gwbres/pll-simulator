import numpy as np
import math

def sinewave (a, f, phase_offset=0, sample_rate=1, size=1):
	"""
	DDS at given frequency 'f' [Hz]
	and amplitude 'a' [N/A]
	
	Returns 'size' symbols

	Optionnal phase_offset [rad]
	
	Optionnal sample rate in {Hz] 
	otherwised concidered unitary in our system
	"""

	t = np.linspace(0, size-1, num=size) / sample_rate
	white_noise = np.random.normal(0, 0.5e-1, size=size)
	
	return a * np.sin(2*np.pi*f*t + phase_offset) + white_noise 

def dds (freq_offset, phase_offset, quantized_lut, prev_accumulator=0):
	# phase accumulator
	accumulator = prev_accumulator
	accumulator += freq_offset 
	# phase offset
	accumulator += phase_offset 
	accumulator = np.fmod(accumulator, 2*np.pi)
	return [quantized_lut[int(round(accumulator))], accumulator]
