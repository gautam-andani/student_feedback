from flask import Flask, request, render_template, redirect, url_for, session, flash
# from flask_mysqldb import MySQL
# import bcrypt

app = Flask(__name__)
app.secret_key = 'lali_lalo'

# MySQL
# app.config

pp = {'hod': ['hod','authority']}
@app.route('/')
def start():
    return render_template('login.html', )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if pp.get(username) and pp[username][0] == password:
            session['logged_in'] = True
            session['username'] = username
            
            if pp[username][1] == 'authority':
                return redirect(url_for('hoddashboard'))
            
        else:
            flash('Username or Password is incorrect')
            return redirect(url_for('start'))
        
    else:
        return render_template('login.html')
    
@app.route("/hoddashboard")
def hoddashboard():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        # teachers_total_feedbacks, teachers_total_positive_feedbacks, teachers_total_negative_feedbacks, teachers_total_neutral_feedbacks,ttp, ttn, ttneu, tcp, tcn, tcneu, tep, ten, teneu, tlwp, tlwn, tlwneu, tlfp, tlfn, tlfneu, tecp, tecn, tecneu = teachers_li
        return render_template('hoddashboard.html')

if __name__ == '__main__':
    app.run(debug=True)