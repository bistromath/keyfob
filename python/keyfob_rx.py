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
from gnuradio.gr import firdes
from gnuradio.wxgui import scopesink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import wx
import keyfob
import time
import gnuradio.gr.gr_threading as _threading

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

	def __init__(self, queue):
		#grc_wxgui.top_block_gui.__init__(self, title="Top Block")
		gr.top_block.__init__(self)
		##################################################
		# Variables
		##################################################
		self.samp_rate = samp_rate = 100e6/512

		##################################################
		# Blocks
		##################################################
		self.const_source_x_0 = gr.sig_source_f(0, gr.GR_CONST_WAVE, 0, 0, 0.2)
		self.gr_complex_to_mag_squared_0 = gr.complex_to_mag_squared(1)
		self.gr_keep_one_in_n_0 = gr.keep_one_in_n(gr.sizeof_gr_complex*1, 10)
		self.keyfob_msg = keyfob.msg(queue, samp_rate/10.0, 200e-9)
		self.uhd_single_usrp_source_0 = uhd.single_usrp_source(
			device_addr="addr=192.168.10.2",
			io_type=uhd.io_type_t.COMPLEX_FLOAT32,
			num_channels=1,
		)
		_clk_cfg = uhd.clock_config_t()
		_clk_cfg.ref_source = uhd.clock_config_t.REF_SMA
		_clk_cfg.pps_source = uhd.clock_config_t.PPS_SMA
		_clk_cfg.pps_polarity = uhd.clock_config_t.PPS_POS
		self.uhd_single_usrp_source_0.set_clock_config(_clk_cfg);
		self.uhd_single_usrp_source_0.set_samp_rate(samp_rate)
		self.uhd_single_usrp_source_0.set_center_freq(418e6, 0)
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

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	(options, args) = parser.parse_args()
	queue = gr.msg_queue()
	tb = top_block(queue)
	runner = top_block_runner(tb)
	
	while 1:
		try:
			if queue.empty_p() == 0:
				while queue.empty_p() == 0:
					msg = queue.delete_head()
					print msg.to_string()
			elif runner.done:
				raise KeyboardInterrupt
				break
			else:
				time.sleep(0.1)
		
		except KeyboardInterrupt:
			tb.stop()
			runner = None
			break

