<p align="center">
    <img src="assets/logo.png" width=350>
</p>

**Hawkloon** (/'hɔːkluːn/) is a framework to build syncronous workers running on scalable infrastructures.

### How it works
To understand how it works, you should understand the concepts of _Worker_ and _Job_ first.

#### Worker
A Worker is a piece of code that runs and completes a task, kinda like a school kid doing his homework.

#### Job
A Job is a resource, a piece of data given to the Worker. This is the homework I said before.

#### The procedure
 - You write a list of Jobs, and this is given to every Worker.
 - A Worker can split the tasks between some threads.
 - When a Job ends, the thread tells to the others, so they can skip it.

Hawkloon uses **Redis** ([website](https://redis.io)) to keep track of the jobs' states between threads & workers (so you can start a worker on two different machines).

## Example
Let's write a dead simple program that downloads cat images from the internet.

First, write a list of links (**jobs**) the Worker will have to consume.
```python
jobs = (
    "https://i.imgur.com/uvFEcJN.jpg",
    "https://i.imgur.com/6qL2HSN.jpg",
    "https://i.imgur.com/dRxnay8.jpg",
    "https://i.imgur.com/aAuTHLe.jpg",
    "https://i.imgur.com/SpCbHBI.jpg"
)
```

Then, declare the worker and choose the number of threads.
```python
from hawk import Worker

class CatWorker(Worker):
    THREADS = 3 # Default is 2
    pass
```

Alright, now overwrite the `Worker.run` method by adding the ability to actually download some images.

```python
from hawk import Worker
import random, requests

class CatWorker(Worker):
    THREADS = 3
    
    # Requests the image and saves it in binary form
    def run(self, job):
        img = requests.get(job, allow_redirects=True).content

        with open(f"{random.randint(0, 10000)}.jpg", "wb") as f:
            f.write(img)
```

Then, instiantiate the worker and connect it to a Redis server.

```python
worker = CatWorker(jobs)

worker.connect("redis://localhost:6379")
```

After that, start it!

```python
worker.start()
```

At the end, it should look something like this:

```python
import requests, random
from hawk import Worker # Import the Worker class

jobs = (
    "https://i.imgur.com/uvFEcJN.jpg",
    "https://i.imgur.com/6qL2HSN.jpg",
    "https://i.imgur.com/dRxnay8.jpg",
    "https://i.imgur.com/aAuTHLe.jpg",
    "https://i.imgur.com/SpCbHBI.jpg"
)

class CatWorker(Worker): # Make your own worker
    THREADS = 4 # Default is 2
    
    # Requests the image and saves it in binary form
    def run(self, job):
        img = requests.get(job, allow_redirects=True).content

        with open(f"{random.randint(0, 10000)}.jpg", "wb") as f:
            f.write(img)

worker = CatWorker(jobs) # Instantiate the Worker

worker.connect("redis://localhost:6379/0") # Connect it to the redis server
 
worker.consume() # Start working on it...
```