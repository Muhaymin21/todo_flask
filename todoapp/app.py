import sys
from flask import Flask, render_template, request, jsonify, abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost:5432/example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Todos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)

    def __repr__(self):
        return f'\n<Todo ID: {self.id}, Description: {self.description}>\n'


class TodoLists(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todos', backref='list', lazy=True, cascade="all, delete-orphan")


@app.route('/todos/<whattoadd>/add', methods=['post'])
def add_todo(whattoadd):
    error = False
    body = {}
    try:
        data = request.get_json()['data']
        if whattoadd == 'list':
            new_item = TodoLists(name=data)
        else:
            list_id = request.get_json()['list_id']
            new_item = Todos(description=data, completed=False, list_id=list_id)
        db.session.add(new_item)
        db.session.commit()
        body = {
            'id': new_item.id
        }
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify(body)


@app.route('/todos/update', methods=['put'])
def update_todo():
    body = {}
    try:
        item_id = request.get_json()['id']
        item_new_state = request.get_json()['completed']
        Todos.query.get(item_id).completed = item_new_state
        db.session.commit()
        body['success'] = True
    except:
        body['success'] = False
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        return jsonify(body)


@app.route('/todos/<whattodelete>/delete', methods=['delete'])
def delete_todo(whattodelete):
    body = {}
    try:
        item_id = request.get_json()['id']
        if whattodelete == 'list':
            item = TodoLists.query.get(item_id)
        else:
            item = Todos.query.get(item_id)
        db.session.delete(item)
        db.session.commit()
        body['success'] = True
    except:
        body['success'] = False
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        return jsonify(body)


@app.route('/list/<list_id>')
def get_todos(list_id):
    return render_template('index.html', todos=Todos.query.filter_by(list_id=list_id).order_by('id').all(),
                           data=TodoLists.query.order_by('id').all(), active_id=int(list_id))


@app.route('/')
def index():
    data = TodoLists.query.order_by('id').all()
    return redirect(url_for("get_todos", list_id=data[0].id))
