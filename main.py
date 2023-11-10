
from flask import Flask, redirect, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

from datetime import datetime
main = Flask(__name__)

main.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/solkiona/Documents/EliteDev Specialization/Todo.db'

db = SQLAlchemy(main)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    
    def __repr__(self):
        return '<Todo %r >' %self.id


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
@main.route('/demo/', methods=['GET', 'POST'])
def demo():
    # if request.method == "POST":
    #     search_term =  request.form['content']
        # results = Todo.query.filter(Todo.content.ilike(f"%{search_term}%")).all()
        # return render_template('task.html', results=results)
    # else:
    #     return render_template('task.html')
    return render_template('task.html')

@main.route('/search/', methods=['GET'])
def search():
    content = request.args.get('content')
    print(content)
    
    if content:
        
        results = Todo.query.filter(Todo.content.ilike(f"%{content}%")).limit(2).all()
    else:
        results = []
    return render_template('task.html', results=results)
        
@main.route('/learn', methods=['POST', 'GET'])
def learn():
    return render_template('learnhtmx.html')

@main.route('/trigger_delay')
def trigger_delay():
    q = request.args.get('q')
    print(q)
    
    results = Todo.query.filter(Todo.content.ilike(f"%{q}%")).limit(2).all()
    
    
    return render_template('task.html', results=results)


if __name__ == '__main__':
    main.run(debug=True)
    
    




