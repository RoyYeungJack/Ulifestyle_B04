from datetime import datetime
import random
from flask import render_template, flash, abort, redirect, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from flask_babel import _, get_locale
from app import app, db
from app.forms import AddCommentForm, JapanPostForm, LoginForm, RegistrationForm, EditProfileForm, PostForm, \
    ResetPasswordRequestForm, ResetPasswordForm, PostForm
from app.models import User, Post, Country, City, CityIntroduction, BlogPost, BlogType, BlogComt, JapanPost, \
UserPoints , MemberItem , PicTest, PostComment, Tag, ItemImage
from app.formblog import AddBlogPostForm, AddBlogTypeForm, EditBlogPostForm, \
    EditBlogTypeForm, AddPostComtForm,DelComtForm
from app.email import send_password_reset_email



@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index(): #Lau Mei Yan
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page, per_page=app.config["POSTS_PER_PAGE"], error_out=False)
    next_url = url_for(
        'explore', page=posts.next_num) if posts.next_num else None
    prev_url = url_for(
        'explore', page=posts.prev_num) if posts.prev_num else None
    return render_template('index.html.j2', title=_('Home'),
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)
   
#---------------------Lau Mei Yan (Mandy)-------------------------

@app.route('/posts')
def posts():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page, per_page=app.config["POSTS_PER_PAGE"], error_out=False)
    next_url = url_for(
        'explore', page=posts.next_num) if posts.next_num else None
    prev_url = url_for(
        'explore', page=posts.prev_num) if posts.prev_num else None
    return render_template('posts.html.j2', title=_('Post'),
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)

#--------------------------Mandy End------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    #locations = Location.query.all()
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password!')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
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


#-----------------------Jack Admin Page-------------------------------------

@app.route('/admin')
@login_required
def Admin():
    if current_user.is_admin == False:
        return redirect(url_for('index'))
    return render_template('admin.html.j2')

#---------------------Yeung Yau Ki(Jack) Base Page--------------------------

@app.route('/blog', methods=['GET', 'POST'])
def Blog():
    blogposts = BlogPost.query.all()
    blogtypes = BlogType.query.all()
    blogcomts = BlogComt.query.all()
    random.shuffle(blogposts)
    random_posts = blogposts[:5]        # gen random post on blogindex
    return render_template('blog.html.j2',blogposts=blogposts,blogtypes=blogtypes, blogcomts=blogcomts,random_posts=random_posts)


@app.route('/blog/<blog_type>')         # specific type page
def Blog_Type_Page(blog_type):
    blogtypes = BlogType.query.all()
    blog_type_entry = BlogType.query.filter_by(type=blog_type).first()          #BlogType.type(Pet) Object
    blog_posts = BlogPost.query.filter_by(blogtype_id=blog_type_entry.id).all() #BlogPost.byte_id=Pet.id(P1,P2) Object
    return render_template('blog_type.html.j2', blogtypes=blogtypes, blog_type_entry=blog_type_entry, blog_posts=blog_posts)

@app.route('/blog/post/<int:post_id>')  # # specific post page
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
        last_type = BlogType.query.order_by(BlogType.id.desc()).first()   # find lastest ID
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
        if form.delete.data:                                        # Del Type and sub Posts & Comts
            subposts = BlogPost.query.filter_by(blogtype_id=types.id).all()
            for i in subposts:
                BlogComt.query.filter_by(blogpost_id=i.id).delete() # sub Comts
            BlogPost.query.filter_by(blogtype_id=types.id).delete() # sub Posts
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
        last_post = BlogPost.query.order_by(BlogPost.id.desc()).first()  # find lastest ID
        blogpost = BlogPost(id=last_post.id+1, title=form.title.data,user=current_user,
                            description=form.dct.data, blogtype_id=form.type_id.data)
        db.session.add(blogpost)
        db.session.commit()
        typeid = BlogType.query.filter_by(id=form.type_id.data).first()  # fkey
        flash(_('Finish'))
        return redirect(url_for('Blog_Type_Page',blog_type=typeid.type))
    return render_template('blog.html.j2', form=form)


@app.route('/blog/editpost/<int:post_id>', methods=['GET', 'POST'])
@login_required                            # specfic post id page
def Edit_Blog_Post(post_id):
    post = BlogPost.query.get(post_id)
    if post.user_id != current_user.id:    # restrict same user
        flash('Unauthorized access.')
        return redirect(url_for('Blog'))
    form = EditBlogPostForm()

    if form.validate_on_submit():
        if form.delete.data:       # delete detect , sub comt
            BlogComt.query.filter_by(blogpost_id=post.id).delete() 
            db.session.delete(post)
            db.session.commit()
            flash('Post deleted successfully.')
            return redirect(url_for('Blog'))
        
        post.title = form.title.data      # update to db
        post.description = form.desc.data
        db.session.commit()
        flash('Post updated successfully.')
        return redirect(url_for('Blog_Post_Page', post_id=post.id))
    
    form.title.data = post.title           # show original data
    form.desc.data = post.description
    return render_template('blog.html.j2', form=form, post=post)

#-----------------------------------Jack Comt Form----------------------------------------------

@app.route('/blog/post/<int:post_id>/comt', methods=['GET', 'POST'])
@login_required
def Add_Post_Comt(post_id):
    postinf = BlogPost.query.get(post_id)
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
@login_required
def edit_city(city_name):
    if not current_user.is_admin:
        abort(404)

    # Get the section to edit from the query parameters
    section = request.args.get('section', 'introduction')

    # Find the city in the database
    city = City.query.filter_by(name=city_name).first_or_404()

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

@app.route('/guide_for_japan', methods=['GET', 'POST'])
def guide_for_japan():
    # Retrieve all posts for display
    posts = JapanPost.query.order_by(JapanPost.id.desc()).all()

    # Check if the user is logged in
    if current_user.is_authenticated:
        form = JapanPostForm()
        # If the form submission is valid, process the post save.
        if form.validate_on_submit():
            new_post = JapanPost(
                # Ensure the author is the current logged-in user.
                author_id=current_user.id,  
                title=form.title.data,
                content=form.content.data,
                location=form.location.data,
                rating=form.rating.data,
                image_url=form.image_url.data
            )
            db.session.add(new_post)
            db.session.commit()
            flash('Post has been created successfully!')
            return redirect(url_for('guide_for_japan'))
        # If the user is logged in, display the form and posts.
        return render_template('guide_for_japan.html.j2', form=form, posts=posts)
    else:
        # If the user is not logged in, do not display the form, only display the posts.
        return render_template('guide_for_japan.html.j2', posts=posts)

@app.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    if not current_user.is_admin:
        abort(404)
    post = JapanPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post has been deleted successfully.', 'success')
    return redirect(url_for('guide_for_japan'))


@app.route('/view_japan_post/<int:post_id>')
def view_japan_post(post_id):
    post = JapanPost.query.get_or_404(post_id)
    return render_template('view_japan_post.html.j2', post=post)

#---------------------------Gordy End-----------------------------------------

#------------------------Chen Cho Cham Tony part------------------------------

@app.route('/member',methods=['GET', 'POST'])
@login_required
def member():
    user_points = UserPoints.query.filter_by(user_id=current_user.id).first()
    food_items = db.session.query(MemberItem, ItemImage).filter_by(category='food').join(ItemImage).all()
    travel_items = db.session.query(MemberItem, ItemImage).filter_by(category='travel').join(ItemImage).all()
    pictests = PicTest.query.filter_by(name = "cola").all()
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

#----------------------------Lau Mei Yan (Mandy)---------------------------

@app.route('/post', methods=['GET', 'POST'])
@app.route('/post/newpost', methods=['GET', 'POST'])
@login_required
def newpost():
    form = PostForm()
    if form.validate_on_submit():
        city_id = form.city.data
        city = City.query.get(city_id)
        tag_name = form.tag.data
        tag = Tag.query.filter_by(name=tag_name).first()
        if not tag:
            max_tag_id = db.session.query(db.func.max(Tag.id)).scalar()
            if max_tag_id is None:
                max_tag_id = 0
            tag = Tag(name=tag_name, id=max_tag_id + 1)
            db.session.add(tag)
            db.session.commit()
            
        post = Post(title=form.title.data, body=form.post.data, city=city, tag=tag, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now live!'))
        return redirect(url_for('posts'))

    return render_template('newpost.html.j2', title=_('New Post'), form=form)

@app.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get(post_id)

    if not post:
        return render_template('404.html.j2')
    
    post = Post.query.get(post_id)
    comments = post.postcomment
    return render_template('post_detail.html.j2', post=post, comments=comments)

@app.route('/post/<int:post_id>/comment', methods=['GET', 'POST'])
@login_required
def add_comment(post_id):
    post = Post.query.get(post_id)

    if not post:
        return render_template('404.html.j2')

    form = AddCommentForm()

    if form.validate_on_submit():
        comment = PostComment(content=form.content.data, user_id=current_user.id, post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash('Comment added successfully.', 'success')
        return redirect(url_for('post_detail', post_id=post.id))

    return render_template('add_comment.html.j2', form=form, post=post)

@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get(post_id)

    if not post:
        return render_template('404.html.j2')

    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.post.data
        city_id = form.city.data
        city = City.query.get(city_id)
        post.city = city

        tag_name = form.tag.data
        tag = Tag.query.filter_by(name=tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            db.session.add(tag)
            db.session.commit()
        post.tag = tag

        db.session.commit()
        flash(_('Your post has been updated!'))
        return redirect(url_for('post_detail', post_id=post.id))

    elif request.method == 'GET':
        form.title.data = post.title
        form.post.data = post.body
        form.city.data = post.city_id
        form.tag.data = post.tag.name

    return render_template('edit_post.html.j2', form=form, post=post)

@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def dl_post(post_id):
    post = Post.query.get(post_id)

    if not post:
        return render_template('404.html.j2')

    db.session.delete(post)
    db.session.commit()
    flash(_('Your post has been deleted!'))
    return redirect(url_for('posts'))

@app.route('/posts/tag/<tag_id>')
def posts_by_tag(tag_id):
    tag = Tag.query.get(tag_id)

    if not tag:
        return render_template('404.html.j2')

    posts = Post.query.filter_by(tag=tag).all()
    return render_template('posts_by_tag.html.j2', tag=tag, posts=posts)

#-----------------------------Mandy End-----------------------------------