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
        books = Book.query.all()
        print(books)
        
        # user = User.query.get_or_404(user_id)
        # book = Book.query.get_or_404(book_id)
        
        return render_template('dashboard.html', admin_status=admin_status,user=user, books=books)
    else:
        return redirect(url_for('login.login'))

@app.route('/base/<int:book_id>')
def base(book_id):
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        admin_status = request.args.get('admin_status')
        
        book = Book.query.get_or_404(book_id) 
        return render_template('base.html', book=book)
    return redirect('/')

@app.route('/blog/')
def blog():
    return render_template('blog.html')

@app.route('/create')
def create():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        admin_status = request.args.get('admin_status')
        return render_template('create.html', admin_status=admin_status,user=user)
    
    
@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/favorite')
def favorite():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get_or_404(user_id)
        favBooks = user.favorite_books
        
        return render_template('favorite.html', books=favBooks, user=user)
        
@app.route('/favorite/<int:book_id>')
def toggle_favorite(book_id):
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get_or_404(user_id)
        book = Book.query.get_or_404(book_id)
        print('got here')
        if book in user.favorite_books:
            user.favorite_books.remove(book)
            print('removed from favorite')
        else:
            user.favorite_books.append(book)
            print("added to favorites")
        db.session.commit()
        return ''
        
 

@app.route('/trigger_delay')
def trigger_delay():
    q = request.args.get('q')
    print('content of  q is: ',    q)
    if q.isspace() or len(q) <= 3 or q == '' or q == ' ':
        return ''
    
    if  (not q.isspace())  and q != '' and (len(q) != 0):
        print('q is :', q)
        results = Book.query.filter(Book.Description.ilike(f"%{q}%")).limit(5).all()
        if results:
            return render_template('results.html', results = results)
        else:
            return "<h1 style='color: rgba(233, 226, 226, 0.5)'> NO RESULTS FOUND </h1>"
    else:
        return "<h1 style='color: rgba(233, 226, 226, 0.5)'> NO RESULTS FOUND </h1>"
    
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
        description = request.form['description'] 
        coverImage = os.path.relpath(os.path.join(upload_folder, filenameX).replace('\\', '/'), upload_folder)
        filepath = os.path.relpath(os.path.join(upload_folder, filenameY).replace('\\', '/'), upload_folder)
        
        new_book = Book(bookTitle=bookTitle, bookAuthor=bookAuthor,
        coverImage=coverImage, Description=description, filepath=filepath)
        book_status = new_book
        db.session.add(new_book)
        db.session.commit()
        
        return redirect(url_for('dashboard'))
    
    return render_template('create.html')
        
        




@app.route('/books/')
def books():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        book_status = Book.query.all()
        return render_template('books.html', user_id=user_id , book_status=book_status)
    return render_template('books.html')

# @app.route('/deleteuser')
# def deleteuser():
#     user_to_delete = User.query.get_or_404(1)
#     db.session.delete(user_to_delete)
#     db.session.commit()
    
#     return 'User Deleted'


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
        

        
@app.post('/delete/<int:book_id>')
def delete(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    
    
    return render_template('base.html')

if __name__ == '__main__':
    app.run(debug=True)
