# sdrCourse
coursework for Michael Ossman's software defined radio with Hack RF course
(Implemented with GNU Radio and GNU Radio Companion)

Listing of interesting exercises:

**sweeper_noXM.py** sweeps through a section of RF Spectrum by stepSize from minFreq to maxFreq and collects samples from each.
**lession1.py** is an FM Radio receiver with FM demodulation to audio.

**transmit_osmocom_freq_sweeper.py** will sweep through a section of RF Spectrum, transmitting a CW signal at each step. This can be used with a spectrum analyzer or other radio to check things like antenna response at a broad range of freqencies, or pre-susceptibility testing for electronics. 
