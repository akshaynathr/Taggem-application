from flask import Flask,jsonify,request,render_template,url_for, redirect,flash,session,flash
from werkzeug import secure_filename
from urlparse import urlparse
import rethinkdb as r
import json
import sys
import os
app=Flask(__name__)
app.config['SECRET_KEY']='2312ghas'
from models import dbSetUp
from extractor import extract,URL_REGEX
# starts database
dbSetUp()
sys.stdout=open('info.log','w')
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
            flash("Login error")
            return render_template('login.html')
    



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
            filename=username+'.'+filename.rsplit('.', 1)[1]
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
            return  redirect(url_for('discover')) 

@app.route('/receive',methods=['POST'])
def receive_content():
   # add post request check 
    try:
    	uri=json.loads(request.data)
    	url=uri['url']
    	print url
        url_count=r.db('taggem2').table('post').filter((r.row['apiKey']==uri['apiKey']) & (r.row['url']==url)).count().run(conn)
    	access=authenticate(uri['apiKey'])
    	if access==0:
		return "Not authenticated"
    	user=list(r.db('taggem2').table('user').filter({'apiKey':uri['apiKey']}).run(conn))
    	if url_count>0:
		print "Already posted "+url
		return "Already posted"
		return jsonify({"type":'success','message':"already saved"})

    	data=extract(url)
    	parsed_uri=urlparse(url)
    	domain='{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    except Exception as e:
	result="Error:"+str(e)
	return jsonify({'result':result})

    if not URL_REGEX.match(url):
        print "hello"
        return jsonify({
              'type': 'error',
              'message': 'Invalid URL'
        }), 406
    else:

        try:


            r.db('taggem2').table('post').insert({'domain':domain,'img_url':data['image'],'url':data['url'],'summary':data['summary'],'keywords':data['keywords'],'authors':data['authors'],'apiKey':uri['apiKey'],'title':data['title'],'text':data['text'],'html':data['html'],'date':r.now(),'views':0,'user-name':user[0]['name'],'user-img':user[0]['img']}).run(conn)

        except Exception as e:
            error="Database error:"+str(e)
            return jsonify({
              'type': 'error',
              'message':  error
        }), 406
    print "Sucess "+url

    return jsonify(type='success',message=data)

@app.route('/discover_my_feed')
def discover_my_feed():
    #add session here
    if 'apiKey' in session:
        feed_url='/feed/'+str(session['apiKey'])
        profile_url='/profile/'+str(session['apiKey'])
        my_feed='/myfeed/'+str(session['apiKey'])              
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
	try:
		post_feed=list(r.db('taggem2').table('user').filter({'apiKey':int(apiKey)})['follow'][0].eq_join(lambda x:x,r.db('taggem2').table('post'),index='apiKey').limit(12).order_by('date').run(conn))


        #post_feed=list(r.db('taggem2').table('post').filter({'apiKey':int(apiKey)}).order_by(r.desc('date')).run(conn))

		return jsonify({'feed':post_feed})
	except Exception as e:
		return jsonify({'feed':str(e)}),400
    else :
        return jsonify({'feed':'error'}),400

@app.route('/myfeed/<apiKey>/<int:no>')
def myfeed(apiKey,no):
    try:
	    count=r.db('taggem2').table('user').filter({'apiKey':int(apiKey)}).count().run(conn)
	    if count>0:

		#post_feed=list(r.db('taggem2').table('user').filter({'apiKey':int(apiKey)})['follow'][0].eq_join(lambda x:x,r.db('taggem2').table('post'),index='apiKey').run(conn))
		skip_no=no*8	
		post_feed=list(r.db('taggem2').table('post').filter({'apiKey':int(apiKey)}).order_by(r.asc('date')).skip(skip_no).limit(8).run(conn))

		return jsonify({'feed':post_feed})
	    else :
		return jsonify({'feed':'not authenticated'}),400
    except Exception as e:
	    return jsonify({'error':str(e)}),406



@app.route('/feed_entry/<postId>/<apiKey>')
def feed_entry(postId,apiKey):
    count=r.db('taggem2').table('user').filter({'apiKey':int(apiKey)}).count().run(conn)
    if count>0:
        post_feed=list(r.db('taggem2').table('post').filter({'id':(postId)}).run(conn))
        post_count=r.db('taggem2').table('post').filter({'id':(postId)}).update({'views':r.row['views']+1}).run(conn)

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
    if 'apiKey' in session:
        print apiKey
        access=authenticate(apiKey)
        if access ==1:
            user=list(r.db('taggem2').table('user').filter({'apiKey':int(apiKey)}).run(conn))
            print user
            img='uploads/'+user[0]['img']
            return render_template('profile.html',img=img,user=user[0])
        else:
            return "Not logged in "
    else:
        return "Not logged in"


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
    if 'apiKey' in session:
        if request.method=='GET': 
            profile='/profile/'+str(session['apiKey'])
            return render_template('connect.html',user=None,msg='',profile=profile)
        if request.method=='POST':
            apiKey=session['apiKey']
            
            profile='/profile/'+str(session['apiKey'])
            name=request.form['search']
            matchkey="(?i)^"+name+"$"
            count=r.db('taggem2').table('user').filter((lambda doc:(doc['name'].match(name)) & (doc['apiKey']!=apiKey))).count().run(conn) 
            #count=r.db('taggem2').table('user').filter({'email':email}).count().run(conn)
            if count >0:
                print "Entered"
                user=list(r.db('taggem2').table('user').filter(lambda doc:(doc['name'].match(name)) & (doc['apiKey']!=apiKey)).run(conn) )
                #user=list(r.db('taggem2').table('user').filter({'name':name}).run(conn))
                msg=str(count)+' users found'
                profile='/profile/'+str(session['apiKey'])
                return render_template('connect.html',user=user,msg='',profile=profile,apiKey=session['apiKey'])

            else :
                return render_template('connect.html',user=None,msg="No user found",profile=profile,apiKey=session['apiKey'])
    else:
        return "Not logged in"



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
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set([ 'png', 'jpg', 'jpeg'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and  filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

####################### follower################################

@app.route('/addFollowers/<int:apiKey1>/<int:apiKey2>',methods=['POST'])
def addFollower(apiKey1,apiKey2):
    access=authenticate(apiKey1)
    if access==1:
        access2=authenticate(apiKey2)
        if access2==1:
            user=list(r.db('taggem2').table('user').filter({'apiKey':apiKey1}).update({'follow':r.row['follow'].append(apiKey2)}).run(conn))
            return jsonify({'result':'success'})
        else:
            return 0
    else:
        return 0

'''
@app.route('/unFollow/<int:apiKey1>/<int:apiKey2>')
def unfollow(apiKey1,apiKey2):
    access=authenticate(apiKey1)
    if access==1:
        access2=authenticate(apiKey2)
        if access2==1:
'''

############################search###########################
@app.route('/search/<int:apiKey>',methods=['POST'])
def search(apiKey):
    data=json.loads(request.data)
    key=data['key']
    print key
    access=authenticate(apiKey)
    if access==1:
        try:
            post=list(r.db('taggem2').table('post').filter(lambda post: post['keywords'].contains(key)).run(conn))
            return jsonify({'feed':post})
        except Exception as e:
            return jsonify({'error':str(e)})

    else :
        return "No access"


###################################################################

########################users list ##################################
@app.route('/allusers/<int:apiKey>')
def allusers(apiKey):
    users=list(r.db('taggem2').table('user').filter(r.row['apiKey']!=apiKey).run(conn))
    return jsonify({'users':users})

#####################################################################
