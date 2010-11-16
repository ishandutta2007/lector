""" Lector: scannerthread.py

    Copyright (C) 2008 Davide Setti

    This program is released under the GNU GPLv2
""" 

## PyQt
from PyQt4.QtCore import QThread, SIGNAL
## SANE
# import sane

class ScannerThread(QThread):
    def __init__(self, parent=None, selectedScanner=None):
        QThread.__init__(self, parent)
        self.selectedScanner = selectedScanner
        self.im = None
        
    def run(self):
        s = sane.open(self.selectedScanner)

        s.mode = 'color'
        
        ## BOTTOM RIGHT POS
        s.br_x = 300.
        s.br_y = 300.
        s.resolution = 300

        #print 'Device parameters:', s.get_parameters()

        # Initiate the scan
        s.start()

        # Get an Image object
        self.im = s.snap()
        self.emit(SIGNAL("scannedImage()"))