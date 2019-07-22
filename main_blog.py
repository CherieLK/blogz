from models import User, Blog
from app import db, app, flash, request, session, redirect, render_template


@app.before_request  #special decorator before a request is made
def require_login(): #not a request handler, we want every user to hit this
    allowed_functions = ['get_username', 'get_new_username', 'index'] #does not check for email (keeps endless loop (302) from happening)
    if request.endpoint not in allowed_functions and 'username' not in session:
        return redirect('/login')

        

@app.route('/')
def index():
        
    username_list = User.query.all()
    return render_template('index.html', title="List of Blog Authors", list_of_users=username_list)



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

        logged_in_username = session['username'] 	
        owner = User.query.filter_by(username=logged_in_username).first()

        if blogtitle_error != "":
            return render_template('new_post.html', title="Build A Blog", blogtitle_error=blogtitle_error, blog_message = blog_message)   
        elif blogbody_error != "":
            return render_template('new_post.html', title="Build A Blog", blogbody_error=blogbody_error, blog_title = blog_title) 
        else:    
            new_blog = Blog(blog_title, blog_message, owner)
            db.session.add(new_blog)
            db.session.commit()
            return render_template('ind_blog.html', title="Individual Blog", ind_blog=new_blog)
    else:
        return render_template('new_post.html', title="Build A Blog")


@app.route('/blog_list', methods=['GET', 'POST'])
def get_blogs():

    id = request.args.get('id')
    if id :
        get_blog_entry = Blog.query.get(id)
        return render_template('ind_blog.html', title="New Blog", ind_blog=get_blog_entry(id))

    authorid = request.args.get('authorid') #when click on title from blog list page
    if authorid :
        id = int(authorid)        
        get_auth_blogs = Blog.query.filter_by(owner_id=id).order_by(Blog.id.desc()).all()
        return render_template('blog_list.html', title="Author Blog List", bloglist=get_auth_blogs)

    get_bloglist= Blog.query.order_by(Blog.id.desc()).all()
    return render_template('blog_list.html', title="All Blogs", bloglist=get_bloglist)
    
@app.route('/ind_blog', methods=['GET'])
def get_ind_blog():

    blog_id = request.args.get('id')
    ind_blog = Blog.query.get(blog_id)

    return render_template('ind_blog.html', title="Individual Blog", ind_blog=ind_blog)
    
@app.route('/author_blogs', methods=['GET'])
def get_auth_blog():

    user_id = request.args.get('id')
    blogs_by_user = Blog.query.filter_by (owner_id=user_id).all()
        
    return render_template('author_blogs.html', title="Blogs by Author", blogs_by_user=blogs_by_user)  

@app.route('/login', methods=['GET', 'POST'])
def get_username():

    if request.method == 'POST':
        old_user = request.form['ex-user'] 
        password = request.form['password']
        user = User.query.filter_by(username=old_user).first()
        if old_user and user and user.password == password: #checks for null in old user and user
            # session saves info so i will know later person is already logged and save
            # the info so user wont have to log in again
            session['username'] = old_user
            flash("Logged in") # this accesses base template
            return redirect('/')
        else:
            flash("User password incorrect or user does not exist", 'error') # error is a category (can name it anything), this is located on the base html

        
    return render_template('login.html', title="Login to Blogz")

@app.route('/signup', methods=['GET', 'POST'])
def get_new_username():

    if request.method == 'POST':
        username_new = request.form['get-user'] 
        password = request.form['password']
        verify = request.form['verify']

        existing_user = User.query.filter_by(username=username_new).first()

        username_error = ""
        password_error = ""
        verify_error = ""

        if not username_new :
            username_error += "Must enter a User Name, Cannot be Blank. "
        else:
            if len(username_new) > 20 or len(username_new) < 3 :
                username_error += "User Name must be at least 3 characters and no more than 20 characters long. "
            if " " in username_new :
                username_error += "User Name must not have any spaces. "
            if existing_user :
                username_error += "User already exists."
        

        if not password :
            password_error += "Must enter a Password, Cannot be Blank. "
        else:
            if len(password) > 20 or len(password) < 3 :
                password_error += "Password must be at least 3 characters and no more than 20 characters long. "
            if " " in password :
                password_error += "Password must not have any spaces. "

        if not verify :
            verify_error += "Must enter Verify Password, Cannot be Blank. "
        else:
            if len(verify) > 20 or len(verify) < 3 :
                verify_error += "Verify Password must be at least 3 characters and no more than 20 characters long. "
            if " " in verify :
                verify_error += "Verify Password must not have any spaces. "

        if verify not in password :
            password_error += "Password and Verify Password do not match. "

        if any(username_error) or any(password_error) or any(verify_error) :   
            return render_template('signup.html', username = username_new, username_error=username_error, pswd_error=password_error, verify_error=verify_error)
        else:
            new_user = User(username_new, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username_new
            flash_string = "New user: " + username_new + " was sucessfully created!"
            flash(flash_string)
            return redirect('/')
    

@app.route('/logout') #only a GET method
def logout(): 

    del session['username']
    return redirect('/')

if __name__ == '__main__':
    app.run()