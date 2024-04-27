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
from app.models import User, Post, Country, City, CityIntroduction, BlogPost, BlogType, BlogComt, \
UserPoints , MemberItem , PicTest
from app.formblog import AddBlogPostForm, AddBlogTypeForm, EditBlogPostForm, \
    EditBlogTypeForm, AddPostComtForm,DelComtForm




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
    #locations = Location.query.all()
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
    #,locations=locations

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
        userq = User.query.order_by(User.id.desc()).first()
        user = User(username=form.username.data, email=form.email.data,id=userq.id+1)
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


#----------------------------Admin Page-------------------------------------

@app.route('/admin')
@login_required
def Admin():
    if current_user.is_admin == False:
        return redirect(url_for('index'))
    return render_template('admin.html.j2')


#---------------------Yeung Yau Ki(Jack) Base Page--------------------------------------

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

#----------------------------------Jack Type Form----------------------------------------------

@app.route('/admin/addtype', methods=['GET', 'POST'])
@login_required
def Add_Blog_Type_Admin():
    if current_user.is_admin == False:
        return redirect(url_for('index'))
    form = AddBlogTypeForm()
    if form.validate_on_submit():
        last_type = BlogType.query.order_by(BlogType.id.desc()).first()
        blogtype = BlogType(id=last_type.id +1 , type=form.addtype.data)
        db.session.add(blogtype)
        db.session.commit()
        flash(_('Finish Add Type'))
        return redirect(url_for('Admin'))
    return render_template('blog.html.j2', form=form)

@app.route('/admin/edittype', methods=['GET', 'POST'])
@login_required
def Edit_Blog_Type_Admin():
    if current_user.is_admin == False:
        return redirect(url_for('index'))
    form = EditBlogTypeForm()
    if form.validate_on_submit():
        types = BlogType.query.get(form.type_id.data)
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
        return redirect(url_for('Admin'))
    return render_template('blog.html.j2', form=form)

#----------------------------------Jack Post Form----------------------------------------------

@app.route('/blog/addpost', methods=['GET', 'POST'])
@login_required
def Add_Blog_Post():
    form = AddBlogPostForm()
    if form.validate_on_submit():
        last_post = BlogPost.query.order_by(BlogPost.id.desc()).first()
        blogpost = BlogPost(id=last_post.id+1, title=form.title.data,user=current_user,
                            description=form.dct.data, blogtype_id=form.type_id.data)
        db.session.add(blogpost)
        db.session.commit()
        typeid = BlogType.query.filter_by(id=form.type_id.data).first()
        flash(_('Finish'))
        return redirect(url_for('Blog_Type_Page',blog_type=typeid.type))
    return render_template('blog.html.j2', form=form)


@app.route('/blog/editpost/<int:post_id>', methods=['GET', 'POST'])
@login_required
def Edit_Blog_Post(post_id):
    post = BlogPost.query.get(post_id)
    if post.user_id != current_user.id:
        flash('Unauthorized access.')
        return redirect(url_for('Blog'))

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

#-----------------------------------Jack Comt Form----------------------------------------------

@app.route('/blog/post/<int:post_id>/comt', methods=['GET', 'POST'])
@login_required
def Add_Post_Comt(post_id):
    postinf = BlogPost.query.get(post_id) # P1(1)
    form = AddPostComtForm()

    if form.validate_on_submit():
        last_comt = BlogComt.query.order_by(BlogComt.id.desc()).first()
        comt = BlogComt(id=last_comt.id+1 ,blogpost_id=post_id, 
                        content=form.content.data,user=current_user)
        
        db.session.add(comt)
        db.session.commit()
        flash(_('Finish'))
        return redirect(url_for('Blog_Post_Page',post_id=post_id))
    return render_template('blog_post.html.j2', form=form,postinf=postinf)



@app.route('/admin/editcomt', methods=['GET', 'POST'])
@login_required
def Del_Post_Comt_Admin():
    if current_user.is_admin == False:
        return redirect(url_for('index'))
    form = DelComtForm()
    if form.validate_on_submit():
        if form.delete.data:
            delcomt = BlogComt.query.get(form.comts.data)
            db.session.delete(delcomt)
            db.session.commit()
            flash('Comt deleted successfully.')
            return redirect(url_for('Admin'))
    return render_template('blog.html.j2', form=form)

#---------------------------Jack End-----------------------------------------

#---------------------------Mak Chun Kit(gordy) Part-------------------------
    
@app.route('/travel')
def travel():
    countries = Country.query.all()
    return render_template('travel.html.j2', countries=countries)

@app.route('/city/<city_name>')
def city(city_name):
    # Find the city in the database
    city = City.query.filter_by(name=city_name).first_or_404()
    # Find the intro in the database
    intro = CityIntroduction.query.filter_by(city_name=city_name).first()
    return render_template('city.html.j2', city=city, intro=intro)

@app.route('/update_introduction/<city_name>', methods=['POST'])
def update_introduction(city_name):
    # Get the new introduction from the form data
    new_introduction = request.form.get('introduction')

    # Find the city in the database
    city = City.query.filter_by(name=city_name).first()

    # If the city is found
    if city:
        # Update the city's introduction
        city.introduction.introduction = new_introduction

        # Commit the changes to the database
        db.session.commit()

    # Redirect the user back to the city page
    return redirect(url_for('city', city_name=city_name))

@app.route('/edit_city/<city_name>')
def edit_city(city_name):
    # Get the section to edit from the query parameters
    section = request.args.get('section', 'introduction')

    # Find the city in the database
    city = City.query.filter_by(name=city_name).first()

    # Render the edit page
    return render_template('edit_city.html.j2', city=city, intro=city.introduction, section=section)


@app.route('/update_city/<city_name>', methods=['POST'])
def update_city(city_name):
    # Get the new data from the form
    new_introduction = request.form.get('introduction')
    new_useful_links = request.form.get('useful_links')
    new_emergency_help = request.form.get('emergency_help')
    new_transportation_info = request.form.get('transportation_info')


    # Find the city in the database
    city = City.query.filter_by(name=city_name).first()

    # If the city is found
    if city:
        # Check if the introduction has changed
        if new_introduction and new_introduction != city.introduction.introduction:
            # Update the city's introduction
            city.introduction.introduction = new_introduction

        # Check if the useful_links has changed
        if new_useful_links and new_useful_links != city.introduction.useful_links:
            # Update the city's useful_links
            city.introduction.useful_links = new_useful_links
        
        # Check if the emergency_help has changed
        if new_emergency_help and new_emergency_help != city.introduction.emergency_help:
            # Update the city's emergency_help
            city.introduction.emergency_help = new_emergency_help

        # Check if the transportation_info has changed
        if new_transportation_info and new_transportation_info != city.introduction.transportation_info:
            # Update the city's transportation_info
            city.introduction.transportation_info = new_transportation_info

        # Commit the changes to the database
        db.session.commit()

    # Redirect the user back to the city page
    return redirect(url_for('city', city_name=city_name))
#---------------------------Gordy End-----------------------------------------

#------------------------Chen Cho Cham Tony part-----------------------------------------

@app.route('/member',methods=['GET', 'POST'])
@login_required
def member():
    user_points = UserPoints.query.filter_by(user_id=current_user.id).first()
    food_items = MemberItem.query.filter_by(category='food').all()
    travel_items = MemberItem.query.filter_by(category='travel').all()
    pictests = PicTest.query.all()
    if user_points is not None:
        return render_template('member.html.j2', points=user_points.points, food_items=food_items, travel_items=travel_items, pictests=pictests)
    else:
        new_user_points = UserPoints(user_id=current_user.id, points=0)
        db.session.add(new_user_points)
        db.session.commit()
        return render_template('member.html.j2', points=new_user_points.points, food_items=food_items, travel_items=travel_items, pictests=pictests)
    
    
@app.route('/add_points', methods=['GET', 'POST'])
@login_required
def add_points():
    user_id = request.form.get('user_id')
    points = int(request.form.get('points'))
    UserPoints.add_points(user_id, points)
    return redirect(url_for('member'))

@app.route('/subtract_points', methods=['GET', 'POST'])
@login_required
def subtract_points():
    user_id = request.form.get('user_id')
    points = int(request.form.get('points'))
    UserPoints.subtract_points(user_id, points)
    return redirect(url_for('member'))

@app.route('/loginjump', methods=['GET', 'POST'])
def loginjump():
    return render_template('loginjump.html.j2')

@app.route('/purchase_item', methods=['GET','POST'])
@login_required
def purchase_item():
    user_id = request.form.get('user_id')
    item_id = request.form.get('item_id')
    item = MemberItem.query.get(item_id)
    user_points = UserPoints.query.filter_by(user_id=user_id).first()
    if user_points.points >= item.points:
        user_points.points -= item.points
        db.session.commit()
        flash('You have successfully purchased the item!', 'success')
    else:
        flash('You do not have enough points to purchase this item.', 'error')
    return redirect(url_for('member'))

  
 #------------------------end part-----------------------------------------
