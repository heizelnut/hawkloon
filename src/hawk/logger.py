# Copyright (c) 2019 Heizelnut (Emanuele Lillo)
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import sys

class LoggerMixin:
    def log(self, message):
        # Writes a message to STDOUT.
        if self.logging:
            print(f" * {message}", flush=True)
    
    def warn(self, message):
        # Writes a message to STDERR.
        if self.logging:
            print(f" ! {message}", file=sys.stderr, flush=True)
    
    def fail(self, message):
        # Creates a warning (to STDERR) and exits 
        #  with status code 1.
        self.warn(message)
        sys.exit(1)
