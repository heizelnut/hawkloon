<p id="header" align="center">
    <img id="logo" src="https://github.com/heizelnut/hawkloon/blob/master/assets/logo.svg" alt="Hawkloon Logo">
    <div id="shields" align="center">
        <img id="license" src="https://img.shields.io/github/license/heizelnut/hawkloon.svg">
        <img id="code-size" src="https://img.shields.io/github/languages/code-size/heizelnut/hawkloon.svg?color=success&label=size">
        <img id="bruh-moments" src="https://img.shields.io/github/search/heizelnut/hawkloon/BRUH%20moment.svg?label=BRUH%20moments"> 
    </div>
</p>

**Hawkloon** (/'hɔːkluːn/) is a Python framework to build synchronous workers running on scalable infrastructures.

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

Hawkloon uses **Redis** ([website][redis]) to keep track of the jobs' states between threads & workers (so you can start a worker on two different machines).

## Installation
To install it, clone the repo and use the `setup.py` file.
```bash
git clone https://github.com/heizelnut/hawkloon
cd hawkloon/src
python3 setup.py install
```

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

Now you can choose two ways to declare workers: with [Class Inheritance](#class-inheritance) or [Decorators](#decorator-style).

### Class Inheritance

Inherit from the `Worker` class and choose the number of threads.
```python
from hawk import Worker

class CatWorker(Worker):
    THREADS = 3 # Default is 2
    pass
```

Alright, now overwrite the `Worker.consume` method by adding the ability to actually download some images.

```python
from hawk import Worker
import random, requests

class CatWorker(Worker):
    THREADS = 3
    
    # Requests the image and saves it in binary form
    def consume(self, job):
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

### Decorator Style

Import the `Worker` class and instantiate it.

```python
from hawk import Worker

cat_worker = Worker(jobs)
```

Then, create a function that downloads cat images, and decorate it with the new instantiated object passing the amount of threads to use.

```python
@cat_worker(threads=3)
def download(job):
    img = requests.get(job, allow_redirects=True).content

    with open(f"{random.randint(0, 10000)}.jpg", "wb") as f:
        f.write(img)
```

> The decorator function must have only one argument.

After that, connect and start crunching data.

```python
worker.connect("redis://localhost:6379")

worker.start()
```

## Contributing
If you'd like to contribute, you're free to do so! Fork my project and then pull request me.

<!-- MD Links -->
[redis]: https://redis.io
