#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Top Block
# Generated: Wed Mar 30 10:43:12 2011
##################################################

from PyQt4 import Qt
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.gr import firdes
from gnuradio.qtgui import qtgui
from optparse import OptionParser
import sip
import sys

class top_block(gr.top_block, Qt.QWidget):

	def __init__(self):
		gr.top_block.__init__(self, "Top Block")
		Qt.QWidget.__init__(self)
		self.setWindowTitle("Top Block")
		self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
		self.top_layout = Qt.QVBoxLayout(self)
		self.top_grid_layout = Qt.QGridLayout()
		self.top_layout.addLayout(self.top_grid_layout)

		##################################################
		# Variables
		##################################################
		self.samp_rate = samp_rate = 100e6/512

		##################################################
		# Blocks
		##################################################
		self.uhd_usrp_source_0 = uhd.usrp_source(
			device_addr="",
			io_type=uhd.io_type.COMPLEX_FLOAT32,
			num_channels=1,
		)
		self.uhd_usrp_source_0.set_samp_rate(samp_rate)
		self.uhd_usrp_source_0.set_center_freq(418e6, 0)
		self.uhd_usrp_source_0.set_gain(40, 0)
		self.qtgui_sink_x_0 = qtgui.sink_f(
			1024, #fftsize
			firdes.WIN_BLACKMAN_hARRIS, #wintype
			0, #fc
			samp_rate, #bw
			"QT GUI Plot", #name
			True, #plotfreq
			True, #plotwaterfall
			True, #plotwaterfall3d
			True, #plottime
			True, #plotconst
		)
		self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)
		self.top_layout.addWidget(self._qtgui_sink_x_0_win)
		self.gr_complex_to_mag_0 = gr.complex_to_mag(1)

		##################################################
		# Connections
		##################################################
		self.connect((self.uhd_usrp_source_0, 0), (self.gr_complex_to_mag_0, 0))
		self.connect((self.gr_complex_to_mag_0, 0), (self.qtgui_sink_x_0, 0))

	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
		self.qtgui_sink_x_0.set_frequency_range(0, self.samp_rate)

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	(options, args) = parser.parse_args()
	qapp = Qt.QApplication(sys.argv)
	tb = top_block()
	tb.start()
	tb.show()
	qapp.exec_()

