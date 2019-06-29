# Copyright (c) 2019 Heizelnut (Emanuele Lillo)
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from base64 import b64encode
from hashlib import sha224
from redis import Redis
from redis.exceptions import ConnectionError
from threading import Thread
from multiprocessing import Process
import time

from .logger import LoggerMixin

class Worker(Process, LoggerMixin):
    THREADS = 2

    def __init__(self, jobs, logging=True):
        # Initialize the 'Process' superclass
        super().__init__()

        self.jobs = jobs

        # Enables logging
        self.logging = logging

        # At startup, the worker isn't connected to anything.
        self.connected = False
        
        # Declare a threads list
        self.threads = []

        # Log the name of the worker
        self.log(f"{self.__class__.__name__} initialized.")

    def connect(self, url):
        # Try to connect to Redis via URL, 
        #  if ValueError is thrown, the URL scheme is wrong.
        try:
            self.redis = Redis.from_url(url)
        except ValueError:
            self.fail("The URL scheme is not right.")
        
        try:
            self.redis.ping()
        except ConnectionError:
            self.fail(f"Connection refused from {url}.")

        # If everything went fine, update the worker's state 
        #  to connected.
        self.connected = True
        self.log(f"Connected to {url}.")

    def threaded(self, name):
        # Cycle through jobs.
        for job in self.jobs:
            # Apply Base 64 encoding and SHA224 hashing to
            #  the job, so Redis can handle it easly as a key.
            encoded = b64encode(str(job).encode())
            hashed = sha224(encoded).hexdigest()

            """
            A Job can assume one of 3 states:
                - Untouched: the Job didn't get catched from the Worker yet
                    (code: -2);
                - Processing: the Job is being processed right now from a 
                    Worker (code: -1);
                - Done: the Job is done (code: 0);
            """

            # If the job doesn't exist yet, its value is set 
            #  to -2 (untouched). 
            if self.redis.get(hashed) is None:
                self.log("Registered state for"
                    f" {hashed[:6]}...{hashed[-6:]}")
                self.redis.set(hashed, -2)
            
            # If the job is untouched, catch it, change the state to "processing" 
            #  and work it out.
            # When the job is done, update its state to "done".
            if int(self.redis.get(hashed)) == -2:
                self.redis.incr(hashed)
                self.log(f"Doing {hashed[:6]}...{hashed[-6:]}")
                self.consume(job)
                self.redis.incr(hashed)
                self.log(f"{hashed[:6]}...{hashed[-6:]} done.")

    def run(self):
        # Check if the worker is connected before consuming the jobs.
        if not self.connected:
            self.fail("You should be connected to a Redis server first.")
        
        # Spawn the necessary amount of threads.
        self.log(f"Spawning {self.THREADS} threads...")
        for number in range(self.THREADS):
            # Create the name for the thread - it should be
            #  "<Worker name>-<thread number>" 
            name = f"{self.__class__.__name__}-{number}"
            
            # Create a thread with those properties
            #  (and pass the name too, so at the end it can tell which
            #  thread to delete to the worker).
            thread = Thread(
                name=name,
                target=self.threaded,
                args=(name,)
            )
            
            # Start the thread and add it to the threads list with its name.
            self.threads.append(thread)
            thread.start()

            # WTF/BRUH moment: leave it as it is.
            time.sleep(.1)
        
        try:
            for thread in self.threads:
                thread.join()
        except KeyboardInterrupt:
            self.log("Interrupted, shutting down...")
            self.clear()
            self.fail("Worker killed succesfully.")
        
        # Clear the DB after all threads finished.
        self.clear()

    def clear(self):
        # Cannot clear if the worker isn't connected to Redis.
        if not self.connected:
            self.fail("You should be connected to a Redis server first.")
        
        # Flush the DB - deletes all keys.
        self.log("Flushing the database...")
        self.redis.flushdb()

    # This method should be overwritten from the subclass.
    def consume(self, job):
        pass

    # This method is used with decorator-style declared workers
    def __call__(self, threads=2):
        self.THREADS = threads

        def wrapper(func):
            self.log("Registering the function...")
            self.consume = func

            return func
        
        return wrapper
