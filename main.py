from flask import Flask, request, redirect, render_template, sessions, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))


    def __init__(self, title, body):
        self.title = title
        self.body = body
blog = []

@app.route('/', methods=['POST', 'GET'])
def index():
    return redirect('/blog') 

@app.route('/single_entry')
def single_entry():
        blog_id = request.args.get('id')
        blog = Blog.query.get(blog_id)
        return render_template('single_entry.html', blog=blog)
   

    # return redirect('/blog?id={}'.format(new_entry.id, 'single_entry.html'))
    #blog_id = request.args.get('id')
    #blog_id = Blog.query.get(blog_id)
   # return render_template('single_entry.html', blog_id=blog_id, title=blog_entry)

@app.route('/blog', methods=['POST','GET'])
def blog():
    if request.method == 'GET':
        blogs = Blog.query.all()
        return render_template('blog.html', blogs=blogs)
    if request.method == 'POST':
        blogs = Blog.query.all()
        return render_template('blog.html', blogs=blogs, title='Build-a-blog')
    

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    if request.method == 'GET':
        return render_template('newpost.html')

    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']
        title_error =''
        body_error =''

        if len(blog_title) == 0:
            title_error = "You Must Enter a Title For Your Post!"
        if len(blog_body) == 0:
            body_error = "You Must Enter A Body For Your Entry!"
        if title_error or body_error:
            return render_template('newpost.html', blog_title="New Entry", title_error = title_error, body_error = body_error)

        else:
           if len(blog_title) and len(blog_body) > 0:
               new_entry = Blog(blog_title, blog_body)
               db.session.add(new_entry)
               db.session.commit()
               return redirect('/blog?id={}'.format(new_entry.id))
    
           else:
               return render_template('newpost.html', title='New_Entry', title_error=title_error, body_error=body_error,
               blog_title=blog_title, blog_body=blog_body)
            
            
    return render_template('newpost.html', title='New Entry')
                





if __name__ == '__main__':
   app.run()