#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Keyfob Rx
# Generated: Wed Mar 30 13:50:16 2011
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

class keyfob_rx(grc_wxgui.top_block_gui):

	def __init__(self):
		grc_wxgui.top_block_gui.__init__(self, title="Keyfob Rx")

		##################################################
		# Variables
		##################################################
		self.samp_rate = samp_rate = 100e6/512

		##################################################
		# Blocks
		##################################################
		self.wxgui_scopesink2_0 = scopesink2.scope_sink_f(
			self.GetWin(),
			title="Scope Plot",
			sample_rate=samp_rate/10,
			v_scale=0,
			v_offset=0,
			t_scale=0,
			ac_couple=False,
			xy_mode=False,
			num_inputs=1,
			trig_mode=gr.gr_TRIG_MODE_AUTO,
			y_axis_label="Counts",
		)
		self.Add(self.wxgui_scopesink2_0.win)
		self.uhd_usrp_source_0 = uhd.usrp_source(
			device_addr="",
			io_type=uhd.io_type.COMPLEX_FLOAT32,
			num_channels=1,
		)
		self.uhd_usrp_source_0.set_samp_rate(samp_rate)
		self.uhd_usrp_source_0.set_center_freq(418e6, 0)
		self.uhd_usrp_source_0.set_gain(40, 0)
		self.low_pass_filter_0 = gr.fir_filter_ccf(10, firdes.low_pass(
			1, samp_rate, 6e4, 6e3, firdes.WIN_HAMMING, 6.76))
		self.gr_complex_to_mag_0 = gr.complex_to_mag(1)

		##################################################
		# Connections
		##################################################
		self.connect((self.gr_complex_to_mag_0, 0), (self.wxgui_scopesink2_0, 0))
		self.connect((self.uhd_usrp_source_0, 0), (self.low_pass_filter_0, 0))
		self.connect((self.low_pass_filter_0, 0), (self.gr_complex_to_mag_0, 0))

	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
		self.wxgui_scopesink2_0.set_sample_rate(self.samp_rate/10)
		self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 6e4, 6e3, firdes.WIN_HAMMING, 6.76))

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	(options, args) = parser.parse_args()
	tb = keyfob_rx()
	tb.Run(True)

