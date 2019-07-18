from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:123@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(300))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model): 

    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(120), unique=True)  
    password = db.Column(db.String(120))
    tasks = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.route('/', methods=['GET'])
def index():
        
        return render_template('base.html')


@app.route('/new_post', methods=['POST', 'GET'])
def add_blog():

    blogtitle_error = ""
    blogbody_error = ""

    if request.method == 'POST':
        blog_title = request.form['blog-title']
        if (not blog_title) or ( blog_title.strip() == ""):
            blogtitle_error = "Please enter a blog title. "
            
        blog_message = request.form['blog-message']
        if (not blog_message) or ( blog_message.strip() == ""):
            blogbody_error = "Please enter a blog message. "

        logged_in_username = session['user'] 	
        owner = User.query.filter_by(username=logged_in_username).first()

        if blogtitle_error != "":
            return render_template('new_post.html', title="Build A Blog", blogtitle_error=blogtitle_error, blog_message = blog_message)   
        elif blogbody_error != "":
            return render_template('new_post.html', title="Build A Blog", blogbody_error=blogbody_error, blog_title = blog_title) 
        else:    
            new_blog = Blog(blog_title, blog_message)
            db.session.add(new_blog)
            db.session.commit()
            return render_template('ind_blog.html', title="Individual Blog", ind_blog=new_blog)
    else:
        return render_template('new_post.html', title="Build A Blog")


@app.route('/blog_list', methods=['GET', 'POST'])
def get_blogs():

    blogs = Blog.query.all()
    return render_template('blog_list.html', title="Build A Blog", blogs=blogs)

@app.route('/ind_blog', methods=['GET'])
def get_ind_blog():

    blog_id = request.args.get('id')
    ind_blog = Blog.query.get(blog_id)
    return render_template('ind_blog.html', title="Individual Blog", ind_blog=ind_blog)

@app.route('/login', methods=['GET', 'POST'])
def get_username():

    
    return render_template('login.html', title="Login to Blogz")

@app.route('/signup', methods=['GET', 'POST'])
def get_new_username():

     return render_template('signup.html', title="Signup for Blogz")



if __name__ == '__main__':
    app.run()