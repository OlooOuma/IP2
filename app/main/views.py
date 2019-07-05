from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import User, Pitch, PitchCom
from .. import db,photos
from flask_login import login_required, current_user
from .forms import PitchComForm,PitchForm,UpdateProfile
# import markdown2


@main.route('/')
def index():

   return render_template('index.html')

@main.route('/blog', methods = ['GET','POST'])
@login_required
def pitch():
   form = PitchForm()
   title = 'The PITCHES'
   if form.validate_on_submit():
       new_pitch = Pitch(pitch=form.pitch.data, user_id=current_user.id)

       db.session.add(new_pitch)
       db.session.commit()
       return redirect(url_for('.allpitchs'))

   return render_template("blog.html", title = title, PitchForm= form)


@main.route('/blog/<int:id>',methods=['GET', 'POST'])
@login_required
def pitchid(id):
   form = PitchComForm()
   pitch = Pitch.query.get(id)
   if form.validate_on_submit():
       pitch = form.pitchcom.data
       new_pitchcom = PitchCom(Pitchcom=pitch, pitch_id=id, user=current_user)
       new_pitchcom.save_pitchcom()
   pitchz = PitchCom.query.filter_by(pitch_id=id).all()
   return render_template('blogs.html',PitchForm=form,comments = pitchz,pitch=pitch )

@main.route('/blogs')
@login_required
def allpitchs():
   title = 'all pitchs'
   pitch = Pitch.query.order_by(Pitch.id).all()
   return render_template("bio.html", title=title, pitch=pitch )

@main.route('/user/<uname>')
@login_required
def profile(uname):
   user = User.query.filter_by(username = uname).first()

   if user is None:
       abort(404)

   return render_template("profile/profile.html", user = user)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
   user = User.query.filter_by(username = uname).first()
   if user is None:
       abort(404)

   form = UpdateProfile()

   if form.validate_on_submit():
       user.bio = form.bio.data

       db.session.add(user)
       db.session.commit()

       return redirect(url_for('.profile',uname=user.username))

   return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
   user = User.query.filter_by(username = uname).first()
   if 'photo' in request.files:
       filename = photos.save(request.files['photo'])
       path = f'photos/{filename}'
       user.profile_pic_path = path
       db.session.commit()
   return redirect(url_for('main.profile',uname=uname))
