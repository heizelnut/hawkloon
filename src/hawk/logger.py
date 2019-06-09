# Copyright (c) 2019 Monolix
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import sys

class Logger:
    def log(self, message):
        # Writes a message to STDOUT.
        print(f" * {message}", flush=True)
    
    def warn(self, message):
        # Writes a message to STDERR.
        print(f" ! {message}", file=sys.stderr, flush=True)
    
    def fail(self, message):
        # Creates a warning (to STDERR) and exits 
        #  with status code 1.
        self.warn(message)
        sys.exit(1)
