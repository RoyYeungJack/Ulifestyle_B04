from datetime import datetime
import random
from flask import render_template, flash, redirect, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from flask_babel import _, get_locale
from app import app, db
from app.email import send_password_reset_email
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm, \
    ResetPasswordRequestForm, ResetPasswordForm
from app.models import User, Post, BlogPost, BlogType, BlogComt
from app.formblog import AddBlogPostForm, AddBlogTypeForm, EditBlogPostForm, EditBlogTypeForm, AddPostComtForm



@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now live!'))
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page=page, per_page=app.config["POSTS_PER_PAGE"], error_out=False)
    next_url = url_for(
        'index', page=posts.next_num) if posts.next_num else None
    prev_url = url_for(
        'index', page=posts.prev_num) if posts.prev_num else None
    return render_template('index.html.j2', title=_('Home'), form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page, per_page=app.config["POSTS_PER_PAGE"], error_out=False)
    next_url = url_for(
        'explore', page=posts.next_num) if posts.next_num else None
    prev_url = url_for(
        'explore', page=posts.prev_num) if posts.prev_num else None
    return render_template('index.html.j2', title=_('Explore'),
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'))
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html.j2', title=_('Sign In'), form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('Congratulations, you are now a registered user!'))
        return redirect(url_for('login'))
    return render_template('register.html.j2', title=_('Register'), form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(
            _('Check your email for the instructions to reset your password'))
        return redirect(url_for('login'))
    return render_template('reset_password_request.html.j2',
                           title=_('Reset Password'), form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if user is None:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('login'))
    return render_template('reset_password.html.j2', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.followed_posts().paginate(
        page=page, per_page=app.config["POSTS_PER_PAGE"], error_out=False)
    next_url = url_for(
        'index', page=posts.next_num) if posts.next_num else None
    prev_url = url_for(
        'index', page=posts.prev_num) if posts.prev_num else None
    return render_template('user.html.j2', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html.j2', title=_('Edit Profile'),
                           form=form)


@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('index'))
    if user == current_user:
        flash(_('You cannot follow yourself!'))
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(_('You are following %(username)s!', username=username))
    return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('index'))
    if user == current_user:
        flash(_('You cannot unfollow yourself!'))
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(_('You are not following %(username)s.', username=username))
    return redirect(url_for('user', username=username))

#--------------------------jack base page----------------------------

@app.route('/blog', methods=['GET', 'POST'])
def Blog():
    blogposts = BlogPost.query.all()
    blogtypes = BlogType.query.all()
    blogcomts = BlogComt.query.all()
    random.shuffle(blogposts)
    random_posts = blogposts[:5]
    return render_template('blog.html.j2',blogposts=blogposts,blogtypes=blogtypes, blogcomts=blogcomts,random_posts=random_posts)


@app.route('/blog/<blog_type>')
def Blog_Type_Page(blog_type):
    blogtypes = BlogType.query.all()
    blog_type_entry = BlogType.query.filter_by(type=blog_type).first() #BlogType.type(Pet) Object
    blog_posts = BlogPost.query.filter_by(blogtype_id=blog_type_entry.id).all() #BP.btid=Pet.id(P1,P2) Object
    return render_template('blog_type.html.j2', blogtypes=blogtypes, blog_type_entry=blog_type_entry, blog_posts=blog_posts)

@app.route('/blog/post/<int:post_id>')
def Blog_Post_Page(post_id):
    blogtypes = BlogType.query.all()
    postinf = BlogPost.query.get(post_id)
    comments = postinf.blog_comts
    return render_template('blog_post.html.j2', postinf=postinf, blogtypes=blogtypes, comments=comments)

#--------------------------jack form--------------------

@app.route('/blog/addtype', methods=['GET', 'POST'])
def Add_Blog_Type():
    form = AddBlogTypeForm()
    if form.validate_on_submit():
        count_id = BlogType.query.count()
        blogtype = BlogType(id=count_id + 1, type=form.addtype.data)
        db.session.add(blogtype)
        db.session.commit()
        flash(_('Finish Add Type'))
        return redirect(url_for('Blog'))
    return render_template('blog.html.j2', form=form)


@app.route('/blog/edittype/<int:types_id>', methods=['GET', 'POST'])
def Edit_Blog_Type(types_id):
    types = BlogType.query.get(types_id)
    form = EditBlogTypeForm()

    if form.validate_on_submit():
        if form.delete.data:
            subposts = BlogPost.query.filter_by(blogtype_id=types.id).all()
            for i in subposts:
                BlogComt.query.filter_by(blogpost_id=i.id).delete()

            BlogPost.query.filter_by(blogtype_id=types.id).delete()
            db.session.delete(types)
            db.session.commit()
            flash('Type deleted successfully.')
        else:
            types.type = form.updtype.data
            db.session.commit()
            flash('Type updated successfully.')
        return redirect(url_for('Blog'))
    form.updtype.data = types.type
    return render_template('blog_type.html.j2', form=form, types=types)

#-------------------------------------------------------------------------

@app.route('/blog/addpost', methods=['GET', 'POST'])
def Add_Blog_Post():
    allpost = BlogPost.query.count()
    form = AddBlogPostForm()
    if form.validate_on_submit():
        blogpost = BlogPost(id=allpost +1, title=form.title.data, 
                            description=form.dct.data, blogtype_id=form.type_id.data)
        db.session.add(blogpost)
        db.session.commit()
        typeid = BlogType.query.filter_by(id=form.type_id.data).first()
        flash(_('Finish'))
        return redirect(url_for('Blog_Type_Page',blog_type=typeid.type))
    return render_template('blog.html.j2', form=form,allpost=allpost)


@app.route('/blog/editpost/<int:post_id>', methods=['GET', 'POST'])
def Edit_Blog_Post(post_id):
    post = BlogPost.query.get(post_id)
    form = EditBlogPostForm()

    if form.validate_on_submit():
        if form.delete.data:  # delete detect
            BlogComt.query.filter_by(blogpost_id=post.id).delete() 
            db.session.delete(post)
            db.session.commit()
            flash('Post deleted successfully.')
            return redirect(url_for('Blog'))
        
        post.title = form.title.data
        post.description = form.desc.data
        db.session.commit()
        flash('Post updated successfully.')
        return redirect(url_for('Blog_Post_Page', post_id=post.id))
    form.title.data = post.title
    form.desc.data = post.description
    return render_template('blog.html.j2', form=form, post=post)

#-------------------------------------------------------------------------

@app.route('/blog/post/<int:post_id>/comt', methods=['GET', 'POST'])
def Add_Post_Comt(post_id):
    postinf = BlogPost.query.get(post_id) # P1(1)

    form = AddPostComtForm()
    if form.validate_on_submit():
        count_id_num = BlogComt.query.count()
        comt = BlogComt(id=count_id_num + 1, blogpost_id=post_id, content=form.content.data )
        
        db.session.add(comt)
        db.session.commit()
        flash(_('Finish'))
        return redirect(url_for('Blog_Post_Page',post_id=post_id))
    return render_template('blog_post.html.j2', form=form,postinf=postinf)
