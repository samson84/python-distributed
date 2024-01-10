from time import sleep
from celery import Celery
from . import config

worker = Celery(
  'tasks', 
  broker=config.celery_broker,
  result_backend=config.celery_backend,
)

@worker.task(name="tasks.long-add", task_started=True)
def add(x, y):
  sleep(60.0)
  return x + y

@worker.task(name="tasks.fibonacci", task_started=True)
def fibonacci(n):
  prev = 0
  current = 1
  for i in range(2, n):
    next = prev + current
    prev = current
    current = next
    
  return current
    