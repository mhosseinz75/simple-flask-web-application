from flask import Flask , render_template , request , redirect , url_for
from flask_sqlalchemy import SQLAlchemy


# a simple web application create by mohammad hossein zadeh abbas with flask - bootstrap 
# configsjg ---------------------------------------------------------------

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zdata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# configsjg ---------------------------------------------------------------


# database ---------------------------------------------------------------

class Note(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    notecontent = db.Column(db.Text)
    
    def __init__(self , notecontent):
        self.notecontent = notecontent
    
    def __repr__(self):
        return '<Notecontent %s>' % self.notecontent


class Task(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    content = db.Column(db.Text)
    done = db.Column(db.Boolean , default=False)

    def __init__(self , content):
        self.content = content
        self.done = False
    def __repr__(self):
        return '<Content %s>' % self.content

db.drop_all()
db.create_all()

# database ---------------------------------------------------------------


# home ---------------------------------------------------------------

@app.route('/')
def home():
    return render_template('index.html')


# home ---------------------------------------------------------------



# note ---------------------------------------------------------------

@app.route('/note')
def note():
    notes = Note.query.all()
    return render_template('note.html', notes = notes)


@app.route('/addnote' , methods=['POST'])
def add_note():
    notecontent = request.form['notecontent']
    
    if not notecontent:
        return 'Error'
    
    note = Note(notecontent)
    db.session.add(note)
    db.session.commit()
    return redirect('/note')

@app.route('/deletenote/<int:note_id>')
def delete_note(note_id):
    note = Note.query.get(note_id)
    
    if not note:
        return redirect('/note')
    db.session.delete(note)
    db.session.commit()
    return redirect('/note')

# note ---------------------------------------------------------------




# about ---------------------------------------------------------------

@app.route('/about')
def about():
    render_template('about.html')

# about ---------------------------------------------------------------



# todo list ---------------------------------------------------------------

@app.route('/todolist')
def task_list():
    tasks = Task.query.all()
    return render_template('todolist.html' , tasks=tasks)
    



@app.route('/task' , methods=['POST'])
def add_task():
    content = request.form['content']
    if not content:
        return 'Error'

    task = Task(content)
    db.session.add(task)
    db.session.commit()
    return redirect('/todolist')




@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return redirect('/todolist')
    db.session.delete(task)
    db.session.commit()
    return redirect('/todolist')

@app.route('/done/<int:task_id>')
def resolve_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return redirect('/todolist')
    if task.done:
        task.done = False
    else:
        task.done = True
    
    db.session.commit()
    return redirect('/todolist')


# todo list ---------------------------------------------------------------




if __name__ == '__main__':
    app.run()
