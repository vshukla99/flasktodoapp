from flask import Flask, render_template, request,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.id} - {self.title}"

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method=='POST':
        title = request.form['title']
        description= request.form['description']
        print("POST")
        todo = Todo(title=title,desc=description)
        db.session.add(todo)
        db.session.commit()
    
    alltodo = Todo.query.all()

    return render_template('index.html', alltodo=alltodo)


@app.route("/edit/<int:id>",  methods=['GET', 'POST'])
def edit(id):
    if request.method=='POST':
        title = request.form['title']
        description= request.form['description']
        todo =  Todo.query.filter_by(id=id).first()

        todo.title = title
        todo.desc = description
        db.session.add(todo )
        db.session.commit()
        return redirect("/")
    edittodo = Todo.query.filter_by(id=id).first()
    return render_template('edit.html', edittodo=edittodo)

@app.route("/delete/<int:id>")
def delete(id):
    deletetodo = Todo.query.filter_by(id=id).first()
    db.session.delete(deletetodo)
    db.session.commit() 
    return redirect(url_for("home"))
# redirect("/") we can use this also  


# Ensure database tables are created within an application context
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
