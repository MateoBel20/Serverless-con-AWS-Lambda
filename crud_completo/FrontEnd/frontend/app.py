from flask import Flask, render_template, request, redirect, url_for
import requests  # Usaremos requests para interactuar con tus endpoints
app = Flask(__name__)
@app.route("/")
def index():
    try:
        response = requests.get("https://ksg8hoz3h8.execute-api.us-east-1.amazonaws.com/tasks")
        response.raise_for_status()
        tasks = response.json().get('body', []) 
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener las tareas: {e}")
        tasks = []
    return render_template("index.html", tasks=tasks)
@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")

        print(f"Datos recibidos: Title={title}, Description={description}")

        response = requests.post(
            "https://ksg8hoz3h8.execute-api.us-east-1.amazonaws.com/tasks",
            json={"title": title, "description": description}
        )
        print(f"Respuesta del servidor: {response.status_code}, {response.text}")

        if response.status_code == 200:
            return render_template("create.html", message="Tarea creada exitosamente.")
        else:
            return render_template("create.html", message=f"Error: {response.text}")
    
    return render_template("create.html")
@app.route("/edit/<string:id>", methods=["GET", "POST"])
def edit(id):
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        done = request.form.get("done") == "on"
        requests.put(
            f"https://ksg8hoz3h8.execute-api.us-east-1.amazonaws.com/tasks/{id}",
            json={"title": title, "description": description, "done": done},
        )
        return redirect(url_for("index"))
    try:
        response = requests.get(f"https://ksg8hoz3h8.execute-api.us-east-1.amazonaws.com/tasks/{id}")
        response.raise_for_status()
        task = response.json().get('body', {})
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener la tarea: {e}")
        task = {"title": "", "description": "", "done": False}   
    return render_template("edit.html", task=task)
@app.route("/delete/<string:id>")
def delete(id):
    # Llama al endpoint para eliminar la tarea
    requests.delete(f"https://ksg8hoz3h8.execute-api.us-east-1.amazonaws.com/tasks/{id}")
    return redirect(url_for("index"))
if __name__ == "__main__":
    app.run(debug=True)
