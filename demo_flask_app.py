from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:12345@localhost:5432/example"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'\n<Person with ID: {self.id}, name: {self.name}>\n'


db.create_all()


@app.route('/')
def index():
    name = Person.query.first()
    return f"<h1>Hello {name.name}!</h1>"

#
# if __name__ == '__main__':
#     app.run(host="0.0.0.0")
