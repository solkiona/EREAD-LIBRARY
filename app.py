import os
from decouple import config
from flask import session, Flask , render_template, url_for, request, redirect, send_from_directory
from sqlalchemy import and_
from werkzeug.utils import secure_filename
from models import db, Book, User
from login import login_bp

upload_folder = 'static/uploads'
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder) 
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = config('SECRET_KEY')
db.init_app(app)
app.register_blueprint(login_bp)

 
with app.app_context():
    db.create_all()





@app.route('/')
def index():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        return render_template('index.html', user_id=user_id)
    return render_template('index.html')



@app.route('/dashboard/', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        admin_status = request.args.get('admin_status')
        return render_template('dashboard.html', admin_status=admin_status,user=user)
    else:
        return redirect(url_for('login.login'))

@app.route('/base/')
def base():
    return render_template('base.html')

@app.route('/blog/')
def blog():
    return render_template('blog.html')


@app.route('/favorite')
def favorite():
    fav = Book.query.get_or_404(2)
    if fav.favorite == True:
        fav.favorite = False
        print('true')
        db.session.commit()
        print(Book.query.get_or_404(2).favorite)
        return "No longer favorite"
    
    else:
        fav.favorite = True
        db.session.commit()
        print(Book.query.get_or_404(2).favorite)
        return "back to favorite"
    
 


@app.route('/fileupload/' , methods=['GET', 'POST'])
def fileupload():
    if request.method == 'POST':
    
        if 'file1' not in request.files or 'file2' not in request.files:
            alert_message = '* Required file'
            return render_template('create.html', alert_message=alert_message)
        
        fileX = request.files['file1']
        fileY = request.files['file2']

        if fileX.filename == '' or fileY.filename == '':
            alert_message = '* Required file'
            return render_template('create.html', alert_message=alert_message)
        
        filenameX = secure_filename(fileX.filename)
        filenameY = secure_filename(fileY.filename)
        
        fileX.save(os.path.join(upload_folder, filenameX))
        fileY.save(os.path.join(upload_folder, filenameY))
        
        bookTitle = request.form['bookTitle']   
        bookAuthor = request.form['bookAuthor'] 
        yearPublished = request.form['yearPublished']
        description = request.form['description'] 
        coverImage = os.path.relpath(os.path.join(upload_folder, filenameX).replace('\\', '/'), upload_folder)
        filepath = os.path.relpath(os.path.join(upload_folder, filenameY).replace('\\', '/'), upload_folder)
        
        new_book = Book(bookTitle=bookTitle, bookAuthor=bookAuthor, yearPublished=yearPublished, coverImage=coverImage, Description=description, filepath=filepath)
        book_status = new_book
        db.session.add(new_book)
        db.session.commit()
        
        return redirect(url_for('books'))
    
    return render_template('create.html')
        
        
    

@app.route('/books/')
def books():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        book_status = Book.query.all()
        return render_template('books.html', user_id=user_id , book_status=book_status)
    return render_template('books.html')

@app.route('/download/<filename>')
def download_file(filename):
    directory = 'static/uploads/'
    return send_from_directory(directory, filename)

    


@app.route('/addbooks/', methods=('GET', 'POST'))
def addbooks():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        admin_status = request.args.get('admin_status')
        return render_template('create.html', admin_status=admin_status,user=user)  
        

        
@app.post('/<int:book_id>/delete/')
def delete(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    
    return render_template('books.html')

if __name__ == '__main__':
    app.run(debug=True)
