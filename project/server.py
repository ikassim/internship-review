import hashlib
import psycopg2
import psycopg2.extras
import os
import sys 
from flask import Flask, session, redirect, url_for, request, render_template,escape
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.secret_key= os.urandom(24).encode('hex')



def connectToDB():
    connectionString='dbname=internship user=postgres password=imad1234 host=localhost'
    print connectionString
    try:
        return psycopg2.connect(connectionString)
    except:
        print ("Can't connect to database")

@app.route('/', methods=['GET', 'POST'])
def mainIndex():
    conn=connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    print "we here"
    if 'username' in session:
        print "we here 3"
        #session.pop('username', None)
        #username_session = escape(session['username']).capitalize()
        return redirect(url_for('homePage',session_user_name=session['username']))
    if request.method == 'POST':
        print "we here test",request.form['username'],request.form['password']
        if 'submit' in request.form:
            print "we here 2"
            username = request.form['username']
            currentUser = username
            pw = request.form['password']
            print pw
            query = "select * from users WHERE username = '%s' AND password = '%s'" % (username, pw)
            print query
            cur.execute(query)
            r=cur.fetchall()
            if not r:
                return render_template('index.html')
                
            if r:
                session['username'] = request.form['username']
                for n in r:
                    zipmain= n['zipcode']
                session['zipm']=zipmain
            return redirect(url_for('homePage',session_user_name=session['username']))
           
         #return redirect(url_for('mainIndex',user=currentUser,c=ch))
        if 'register' in request.form:
            print "register"
    
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    conn=connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    isactive=False
    # if user typed in a post ...
    #error = None
    if 'username' in session:
        isactive=True
        #print "The error is here!!!!!!!"
        username_session = escape(session['username']).capitalize()
        return redirect(url_for('mainIndex',session_user_name=username_session,isactive=isactive))
    if request.method == 'POST':
      print "HI"
      username = request.form['username']
      currentUser = username
        
      pw = request.form['pw']
      print pw
      query = "select * from users WHERE username = '%s' AND password = '%s'" % (username, pw)
      print query
      ch=False
      cur.execute(query)
      r=cur.fetchall()
      if r:
         isactive=True
         session['username'] = request.form['username']
         
         
         return render_template('index.html', selectedMenu='Home',session_user_name=session['username'] ,isactive=isactive)
         #return redirect(url_for('mainIndex',user=currentUser,c=ch))
    return render_template('login.html', selectedMenu='Login' ,isactive=isactive)



@app.route('/mapPage', methods=['GET', 'POST'])
def mapPage():
    conn=connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    ##if 'username' in session:
    query = "select * from inernships"
    cur.execute(query)
    res=cur.fetchall()
    return render_template('mapPage.html',res=res)
   ## return render_template('mapPage.html')
    
    
    
@app.route('/adminPage', methods=['GET', 'POST'])
def adminPage():
    conn=connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if 'username' in session:
        
        if request.method=='POST':
            if('publish' in request.form ):
             selected_reviews = request.form.getlist("selectedReviews")
             for i in selected_reviews:
                query = "UPDATE reviews SET status = 1 WHERE id = '%s'" % (i) 
                cur.execute(query)
                conn.commit()
                print (i)
            if('delete' in request.form ):
             selected_reviews = request.form.getlist("selectedReviews")
             for i in selected_reviews:
                query = "DELETE FROM reviews WHERE id = '%s'" % (i) 
                cur.execute(query)
                conn.commit()
                print (i)
            if('add' in request.form ):
                
                title = request.form['title']
                address=request.form['address']
                description=request.form['description']
             
                query = "INSERT INTO inernships VALUES (default, '%s', '%s', '%s')" % (title,address,description) 
                try:
                    cur.execute(query)
                except psycopg2.DatabaseError, e:
                    print 'Error %s' % e 
                #print ("INSERT INTO users VALUES (default,'%s','%s',%s);"%(request.form['username'],passw,request.form['zipcode']), )
                conn.commit()
            
            if('deleteInt' in request.form ):
             selected_internships = request.form.getlist("selectedInternships")
             for i in selected_internships:
                query = "DELETE FROM reviews WHERE inernship_id = '%s'" % (i) 
                cur.execute(query)
                conn.commit()
                query = "DELETE FROM inernships WHERE id = '%s'" % (i) 
                cur.execute(query)
                conn.commit()
                
            
                
        #return redirect(url_for('adminPage',res=st))
        query = "select * from reviews ORDER BY id"
        cur.execute(query)
        res=cur.fetchall()
        
        query = "select * from inernships ORDER BY id"
        cur.execute(query)
        internshipsList=cur.fetchall()
        
        return render_template('adminPage.html',res=res,internshipsList=internshipsList)
    return render_template('adminPage.html')    


@app.route('/submitReviewPage', methods=['GET', 'POST'])
def submitReviewPage():
    conn=connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #if 'username' in session:
    
    if request.method=='POST':
        name=request.form['fname']+" "+request.form['lname']
        email=request.form['email']
        q1=""
        if (request.form['yname']=="yes"):
            q1=True
        else: 
            q1=False
        if (request.form['nemail']=="yes"):
            q2=True
        else:
            q2=False
            
        inernship=request.form['option']
        q3=request.form['q3']
        q4=request.form['q4']
        q5=request.form['q5']
        q6=request.form['q6']
        query = "INSERT INTO reviews VALUES (default,'%s','null',0,'%s','%s','%s','%s','%s','%s','%s','%s')" % (name,email,inernship,q3,q4,q5,q6,q1,q2)
        try:
            cur.execute(query)
        except psycopg2.DatabaseError, e:
            print 'Error %s' % e 
            #print ("INSERT INTO users VALUES (default,'%s','%s',%s);"%(request.form['username'],passw,request.form['zipcode']), )
        conn.commit()
        
        return redirect(url_for('mainIndex'))
    
    query = "select * from inernships"
    cur.execute(query)
    res=cur.fetchall()
    
    return render_template('submitReviewPage.html',res=res)
    #return render_template('submitReviewPage.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method=='POST':
        session.pop('username', None)
        return redirect(url_for('mainIndex'))
    else:
        session.pop('username', None)
        return redirect(url_for('mainIndex'))
    
    return redirect(url_for('mainIndex'))

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route('/HomePage')
def homePage():
    ##if "username" in session:
        ##return render_template('home.html')
    return render_template('index.html')
        

if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=8080)