from flask import Flask, request
from .worker import add, fibonacci, worker

app = Flask(__name__)

@app.post("/api/tasks/long-add")
def post_tasks_long_add():
    body = request.get_json()
    a = body.get("a")
    b = body.get("b")
    result = add.delay(a, b)
    return {
      "id": result.task_id,
      "args": {
          "a": a,
          "b": b
      }
    }

@app.post("/api/tasks/fibonacci")
def post_tasks_fibonacci():
  body = request.get_json()
  n = body.get("n")
  result = fibonacci.delay(n)
  return {
    "id": result.task_id,
    "args": {
        "n": n
    }
  }

@app.get("/api/tasks/<id>")
def get_tasks_id(id):
  inspector = worker.control.inspect()
  task = inspector.query_task(id)
  return {
     "task": task
  }



