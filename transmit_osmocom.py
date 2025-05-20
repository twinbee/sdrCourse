#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: RF TX Sweep
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
import osmosdr
import time
import sip
import threading
import transmit_osmocom_freq_sweeper as freq_sweeper  # embedded python module



class transmit_osmocom(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "RF TX Sweep", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("RF TX Sweep")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "transmit_osmocom")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.freq = freq = 915e6
        self.step_size = step_size = 1e6
        self.samp_rate = samp_rate = 10e6
        self.rf_gain = rf_gain = 0
        self.mult = mult = 1
        self.if_gain = if_gain = 10
        self.fun_prob = fun_prob = 0
        self.frequency = frequency = freq
        self.f_min = f_min = 900e6
        self.f_max = f_max = 927.5e6

        ##################################################
        # Blocks
        ##################################################

        self.probSign = blocks.probe_signal_c()
        self._rf_gain_range = qtgui.Range(0, 20, 1, 0, 200)
        self._rf_gain_win = qtgui.RangeWidget(self._rf_gain_range, self.set_rf_gain, "RF Gain", "dial", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._rf_gain_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._mult_range = qtgui.Range(0, 100, 1, 1, 200)
        self._mult_win = qtgui.RangeWidget(self._mult_range, self.set_mult, "SW Gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._mult_win, 3, 0, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._if_gain_range = qtgui.Range(0, 47, 1, 10, 200)
        self._if_gain_win = qtgui.RangeWidget(self._if_gain_range, self.set_if_gain, "IF", "dial", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._if_gain_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        def _fun_prob_probe():
          self.flowgraph_started.wait()
          while True:

            val = self.probSign.level()
            try:
              try:
                self.doc.add_next_tick_callback(functools.partial(self.set_fun_prob,val))
              except AttributeError:
                self.set_fun_prob(val)
            except AttributeError:
              pass
            time.sleep(1.0 / (10))
        _fun_prob_thread = threading.Thread(target=_fun_prob_probe)
        _fun_prob_thread.daemon = True
        _fun_prob_thread.start()
        self.qtgui_sink_x_0 = qtgui.sink_c(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            (((f_max-f_min)/2+f_min)), #fc
            samp_rate, #bw
            'GUI Sink', #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            False, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(True)

        self.top_layout.addWidget(self._qtgui_sink_x_0_win)
        self.osmosdr_sink_0 = osmosdr.sink(
            args="numchan=" + str(1) + " " + ""
        )
        self.osmosdr_sink_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_sink_0.set_sample_rate(samp_rate)
        self.osmosdr_sink_0.set_center_freq(freq, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(rf_gain, 0)
        self.osmosdr_sink_0.set_if_gain(if_gain, 0)
        self.osmosdr_sink_0.set_bb_gain(0, 0)
        self.osmosdr_sink_0.set_antenna('', 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)
        self._frequency_tool_bar = Qt.QToolBar(self)

        if None:
            self._frequency_formatter = None
        else:
            self._frequency_formatter = lambda x: eng_notation.num_to_str(x)

        self._frequency_tool_bar.addWidget(Qt.QLabel("frequency"))
        self._frequency_label = Qt.QLabel(str(self._frequency_formatter(self.frequency)))
        self._frequency_tool_bar.addWidget(self._frequency_label)
        self.top_grid_layout.addWidget(self._frequency_tool_bar, 1, 1, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(mult)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, freq_sweeper.sweeper(fun_prob, f_min, f_max, step_size), 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.osmosdr_sink_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.probSign, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.qtgui_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "transmit_osmocom")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.set_frequency(self.freq)
        self.osmosdr_sink_0.set_center_freq(self.freq, 0)

    def get_step_size(self):
        return self.step_size

    def set_step_size(self, step_size):
        self.step_size = step_size
        self.analog_sig_source_x_0.set_frequency(freq_sweeper.sweeper(self.fun_prob, self.f_min, self.f_max, self.step_size))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.osmosdr_sink_0.set_sample_rate(self.samp_rate)
        self.qtgui_sink_x_0.set_frequency_range((((self.f_max-self.f_min)/2+self.f_min)), self.samp_rate)

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self.osmosdr_sink_0.set_gain(self.rf_gain, 0)

    def get_mult(self):
        return self.mult

    def set_mult(self, mult):
        self.mult = mult
        self.blocks_multiply_const_vxx_0.set_k(self.mult)

    def get_if_gain(self):
        return self.if_gain

    def set_if_gain(self, if_gain):
        self.if_gain = if_gain
        self.osmosdr_sink_0.set_if_gain(self.if_gain, 0)

    def get_fun_prob(self):
        return self.fun_prob

    def set_fun_prob(self, fun_prob):
        self.fun_prob = fun_prob
        self.analog_sig_source_x_0.set_frequency(freq_sweeper.sweeper(self.fun_prob, self.f_min, self.f_max, self.step_size))

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency
        Qt.QMetaObject.invokeMethod(self._frequency_label, "setText", Qt.Q_ARG("QString", str(self._frequency_formatter(self.frequency))))

    def get_f_min(self):
        return self.f_min

    def set_f_min(self, f_min):
        self.f_min = f_min
        self.analog_sig_source_x_0.set_frequency(freq_sweeper.sweeper(self.fun_prob, self.f_min, self.f_max, self.step_size))
        self.qtgui_sink_x_0.set_frequency_range((((self.f_max-self.f_min)/2+self.f_min)), self.samp_rate)

    def get_f_max(self):
        return self.f_max

    def set_f_max(self, f_max):
        self.f_max = f_max
        self.analog_sig_source_x_0.set_frequency(freq_sweeper.sweeper(self.fun_prob, self.f_min, self.f_max, self.step_size))
        self.qtgui_sink_x_0.set_frequency_range((((self.f_max-self.f_min)/2+self.f_min)), self.samp_rate)




def main(top_block_cls=transmit_osmocom, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
