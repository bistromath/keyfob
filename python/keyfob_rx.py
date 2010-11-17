#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Top Block
# Generated: Tue Nov 16 11:20:42 2010
##################################################

from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from optparse import OptionParser
import keyfob
import time
import gnuradio.gr.gr_threading as _threading
import virtkey

class top_block_runner(_threading.Thread):
    def __init__(self, tb):
        _threading.Thread.__init__(self)
        self.setDaemon(1)
        self.tb = tb
        self.done = False
        self.start()

    def run(self):
        self.tb.run()
        self.done = True

class top_block(gr.top_block):#(grc_wxgui.top_block_gui):

	def __init__(self, queue, options, args):
		#grc_wxgui.top_block_gui.__init__(self, title="Top Block")
		gr.top_block.__init__(self)
		##################################################
		# Variables
		##################################################
		self.samp_rate = samp_rate = 100e6/512

		##################################################
		# Blocks
		##################################################
		self.gr_complex_to_mag_squared_0 = gr.complex_to_mag_squared(1)
		self.gr_keep_one_in_n_0 = gr.keep_one_in_n(gr.sizeof_gr_complex*1, 10)
		self.keyfob_msg = keyfob.msg(queue, samp_rate/10.0, options.threshold)
		self.uhd_single_usrp_source_0 = uhd.single_usrp_source(
			device_addr="",
			io_type=uhd.io_type_t.COMPLEX_FLOAT32,
			num_channels=1,
		)
		_clk_cfg = uhd.clock_config_t()
		_clk_cfg.ref_source = uhd.clock_config_t.REF_SMA
		_clk_cfg.pps_source = uhd.clock_config_t.PPS_SMA
		_clk_cfg.pps_polarity = uhd.clock_config_t.PPS_POS
		#self.uhd_single_usrp_source_0.set_clock_config(_clk_cfg);
		self.uhd_single_usrp_source_0.set_samp_rate(samp_rate)
		self.uhd_single_usrp_source_0.set_center_freq(options.freq, 0)
		self.uhd_single_usrp_source_0.set_gain(40, 0)

		##################################################
		# Connections
		##################################################
		self.connect((self.uhd_single_usrp_source_0, 0), (self.gr_keep_one_in_n_0, 0))
		self.connect((self.gr_keep_one_in_n_0, 0), (self.gr_complex_to_mag_squared_0, 0))
		self.connect((self.gr_complex_to_mag_squared_0, 0), self.keyfob_msg)

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.uhd_single_usrp_source_0.set_samp_rate(self.samp_rate)
		
class kb_input():
	_kb = virtkey.virtkey()
	keycodes = [ 0xff51, 0xff56, 0xff53, 0xff55, 0xff0d ]
	#up: switch 3, ord(0x49) PgUp
	#down: sw 1, ord(0x51) PgDn
	#left: sw 0, ord(0x4B) L arrow
	#right: sw 2, ord(0x4D) R arrow
	#button: sw 4, ord(0x39) enter

	def press(self, mask):
		for i in range(0,5):
			if (mask & ( 1 << i )):
				self._kb.press_keysym(self.keycodes[i])
				self._kb.release_keysym(self.keycodes[i])
			

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	parser.add_option("-f", "--freq", type="eng_float", default=418e6, help="set receive frequency in Hz [default=%default]", metavar="FREQ")
	parser.add_option("-t", "--threshold", type="eng_float", default=200e-9, help="set minimum signal threshold [default=%default]", metavar="dB")
	parser.add_option("-a", "--address", type="int", default=0, help="receive packets to this address [default=%default]")
	parser.add_option("-v", "--verbose", action="store_true", default=False, help="verbose output")
	(options, args) = parser.parse_args()
	queue = gr.msg_queue()
	tb = top_block(queue, options, args)
	runner = top_block_runner(tb)
	kb = kb_input() #our keyboard input hijacker
	kb_history = list()
	
	while 1:
		try:
			if queue.empty_p() == 0:
				while queue.empty_p() == 0:
					msg = queue.delete_head().to_string()

					[ref, addr, sw] = msg.split()
					if options.verbose: print "Ref: %f Addr: %i Sw: %i" % (float(ref), int(addr), int(sw))
					
					if int(addr) == options.address:
						if kb_history.count(int(sw)) > 0:
							kb.press(int(sw))
							kb_history.remove(int(sw))
						else:
							kb_history.append(int(sw))
				
			elif runner.done:
				raise KeyboardInterrupt
				break
			else:
				time.sleep(0.2)
				
			kb_history = list()
		
		except KeyboardInterrupt:
			tb.stop()
			runner = None
			break

