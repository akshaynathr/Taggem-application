from flask import Flask,jsonify,request,render_template,url_for, redirect,flash,session,flash
from werkzeug import secure_filename
from urlparse import urlparse
import rethinkdb as r
import json
import os
app=Flask(__name__)
app.config['SECRET_KEY']='2312ghas'
from models import dbSetUp
from extractor import extract,URL_REGEX
# starts database
dbSetUp()

conn=r.connect(host='localhost',port='28015')

@app.route('/',methods=['GET','POST'])
@app.route('/home',methods=['GET','POST'])
@app.route('/login',methods=['GET','POST'])

def login():
    if request.method=='GET':
        if 'apiKey' in session:
            return redirect(url_for('discover'))
        return render_template('login.html')
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']

        count=r.db('taggem2').table('user').filter({'username':username,'password':password}).count().run(conn)
        user=list(r.db('taggem2').table('user').filter({'username':username,'password':password}).run(conn))

        if count>0:
            session['apiKey']=user[0]['apiKey']
            return redirect(url_for('discover'))
        else :
            return "Login error"
    



@app.route('/signup',methods=['GET','POST'])
def signup_form():
    if request.method=='GET':
        return render_template('signup.html')
 
    if request.method=='POST':
        return redirect(url_for('signup'))


@app.route('/signup_form',methods=['GET','POST'])
def signup():
    if request.method=='GET':
        return render_template('signup_info.html')
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        email=request.form['email']
        dob=request.form['dob']
        name=request.form['name']



    # Get the name of the uploaded file
        file = request.files['file']
        filename=''
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            filename=username+filename.rsplit('.', 1)[1]
            # Move the file form the temporal folder to
            # the upload folder we setup
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            count=r.db('taggem2').table('user').filter({'username':username,'password':password}).count().run(conn)
        if count >0:
            result="Welcome  back "+ name 
            return result
        else :
            try:
                user=r.db('taggem2').table('user').insert({'username':username,'email':email,'dob':dob,'password':password,'name':name,'apiKey':r.random(1000000),'follow':[],'date':r.now(),'img':filename}).run(conn)
                user_data=list(r.db('taggem2').table('user').filter((r.row['username']==username) & (r.row['password']==password)).run(conn))
                session['apiKey']=user_data[0]['apiKey']
                
            except Exception as e:
                result="Error in saving data:"+str(e)
                return result
            return  redirect(url_for('connect')) 

@app.route('/receive',methods=['POST'])
def receive_content():
   # add post request check 
    uri=json.loads(request.data)
    url=uri['url']
    print url
    url_count=r.db('taggem2').table('post').filter({'url':url}).count().run(conn)
    access=authenticate(uri['apiKey'])
    if access==0:
        return "Not authenticated"
    user=list(r.db('taggem2').table('user').filter({'apiKey':uri['apiKey']}).run(conn))
    if url_count>0:
        return jsonify({"type":'success','message':"already saved"})
    data=extract(url)
    parsed_uri=urlparse(url)
    domain='{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

    if not URL_REGEX.match(url):
        return jsonify({
              'type': 'error',
              'message': 'Invalid URL'
        }), 406
    else:

        try:
            
            r.db('taggem2').table('post').insert({'domain':domain,'img_url':data['image'],'url':data['url'],'summary':data['summary'],'keywords':data['keywords'],'authors':data['authors'],'apiKey':uri['apiKey'],'title':data['title'],'text':data['text'],'html':data['html'],'date':r.now(),'views':0,'user-name':user[0]['name'],'user-img':''}).run(conn)

        except Exception as e:
            error="Database error:"+str(e)
            return jsonify({
              'type': 'error',
              'message':  error
        }), 406


    return jsonify(type='success',message=data)

@app.route('/discover_my_feed')
def discover_my_feed():
    #add session here
    if 'apiKey' in session:
        feed_url='/feed/'+str(session['apiKey'])
        profile_url='/profile/'+str(session['apiKey'])
        my_feed='/myfeed'+str(session['apiKey'])              
        return render_template('myfeed.html',myfeed=my_feed,feed=feed_url,profile=profile_url,apiKey=session['apiKey'])

    else :
        return "Not logged in"



@app.route('/discover_page')
def discover():
    #add session here
    if 'apiKey' in session:
        feed_url='/feed/'+str(session['apiKey'])
        profile_url='/profile/'+str(session['apiKey'])
        my_feed='/myfeed'+str(session['apiKey'])              
        return render_template('feed.html',myfeed=my_feed,feed=feed_url,profile=profile_url,apiKey=session['apiKey'])

    else :
        return "Not logged in"

@app.route('/feed/<apiKey>')
def feed(apiKey):
    count=r.db('taggem2').table('user').filter({'apiKey':int(apiKey)}).count().run(conn)
    if count>0:

        post_feed=list(r.db('taggem2').table('user').filter({'apiKey':int(apiKey)})['follow'][0].eq_join(lambda x:x,r.db('taggem2').table('post'),index='apiKey').run(conn))

        #post_feed=list(r.db('taggem2').table('post').filter({'apiKey':int(apiKey)}).order_by(r.desc('date')).run(conn))

        return jsonify({'feed':post_feed})
    else :
        return jsonify({'feed':'error'})

@app.route('/myfeed/<apiKey>')
def myfeed(apiKey):
    count=r.db('taggem2').table('user').filter({'apiKey':int(apiKey)}).count().run(conn)
    if count>0:

        #post_feed=list(r.db('taggem2').table('user').filter({'apiKey':int(apiKey)})['follow'][0].eq_join(lambda x:x,r.db('taggem2').table('post'),index='apiKey').run(conn))

        post_feed=list(r.db('taggem2').table('post').filter({'apiKey':int(apiKey)}).order_by(r.asc('date')).run(conn))

        return jsonify({'feed':post_feed})
    else :
        return jsonify({'feed':'error'})




@app.route('/feed_entry/<postId>/<apiKey>')
def feed_entry(postId,apiKey):
    count=r.db('taggem2').table('user').filter({'apiKey':int(apiKey)}).count().run(conn)
    if count>0:
        post_feed=list(r.db('taggem2').table('post').filter({'id':(postId)}).run(conn))

        return jsonify({'feed':post_feed})
    else :
        return jsonify({'feed':'error'})




def authenticate(apiKey):
    count=(r.db('taggem2').table('user').filter({'apiKey':int(apiKey)}).count().run(conn))
    if count>0:
        return 1
    else :
        return 0

@app.route('/profile/<apiKey>')
def profile(apiKey):
    print apiKey
    access=authenticate(apiKey)
    if access ==1:
        user=list(r.db('taggem2').table('user').filter({'apiKey':int(apiKey)}).run(conn))
        print user
        img='uploads/'+user[0]['img']
        return render_template('profile.html',img=img,user=user[0])
    else:
        return "Not logged in "

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out")
    return redirect(url_for('login'))


@app.route('/followers/<int:apiKey>')
def followers(apiKey):
    access=authenticate(apiKey)
    if access==1:
        followers=r.db('taggem2').table('user').filter({'apiKey':apiKey})['follow'][0].eq_join(lambda x: x,r.db('taggem2').table('user'),index='apiKey').zip().run(conn)
        count=len(followers)
        return jsonify({'followers':followers,'count':count})
    else:
        return 0


@app.route('/connect',methods=['GET','POST'])
def connect():
    if request.method=='GET': 
        return render_template('connect.html',user=None,msg='')
    if request.method=='POST':
        email=request.form['search']
        count=r.db('taggem2').table('user').filter({'email':email}).count().run(conn)
        if count >0:
            user=list(r.db('taggem2').table('user').filter({'email':email}).run(conn))
            img='uploads/'+user[0]['img']
            return render_template('connect.html',user=user[0],msg='',img=img)
        else :
            return render_template('connect.html',user=None,msg="No user found")


#footer links ################################################################################
@app.route('/about')
def about():
    return render_template('footer/about.html')

@app.route('/jobs')
def jobs():
    return render_template("footer/jobs.html")

@app.route('/ads')
def  ads():
    return render_template('footer/ads.html')




#######################plugin login ##################
@app.route('/oauth')
def auth():
    return render_template('auth.html')

@app.route('/authentication',methods=['POST'])
def authentication():
    if request.method=='POST':
        data=json.loads(request.data)
        print (data)
        #print (data.password)
        user=list(r.db('taggem2').table('user').filter({'username':data['username'], 'password':data['password']}).run(conn))
        return  jsonify({'result':user[0]['apiKey']})


############################################################################
########## image upload ##############################################

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set([ 'png', 'jpg', 'jpeg'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and  filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

