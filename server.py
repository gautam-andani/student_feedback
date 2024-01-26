from flask import Flask, render_template, request, redirect, url_for, session
import os
import pickle
import pandas as pd
from flask import Flask, request, render_template, flash, redirect, session, abort, jsonify
from datetime import datetime
from analytics import write_to_csv_departments, write_to_csv_teachers
# from models import StemmedCountVectorizer
from analytics import get_counts, get_tables, get_titles
from teacherdashboard import get_feedback_counts
from access_user import verify
import excel_fill

app = Flask(__name__)
app.secret_key = os.urandom(12) # for session creation and management security
UPLOAD_FOLDER = 'uploads'  # folder to store uploaded files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def start():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def do_admin_login():
    
    username = request.form['username']
    password = request.form['password']
    role = verify(username=username, password=password)
    if not role:
        return redirect(url_for('login'))
    session['username'] = username
    session['logged_in'] = True
    if role == 'hod':
        return hoddashboard()
    elif role == 'admin':
        return root()
    elif role == 'teacher':
        return teacherdashboard(username[7:])
    else:
        return render_template('index.html', name = username)


def teacherdashboard(teachernumber):
    if not session.get('logged_in'):
        return render_template('login.html')
    ttf, teachers_total_positive_feedbacks, teachers_total_negative_feedbacks, teachers_total_neutral_feedbacks, teachers_li = get_feedback_counts()
    ttp, ttn, ttneu, tcp, tcn, tcneu, tep, ten, teneu, tlwp, tlwn, tlwneu, tlfp, tlfn, tlfneu, tecp, tecn, tecneu = teachers_li

    ttp = int(round(ttp/ttf * 100))
    ttn = int(round(ttn/ttf * 100))
    ttneu = int(round(ttneu/ttf * 100))
    tcp = int(round(tcp / ttf * 100))
    tcn = int(round(tcn/ttf * 100))
    tcneu = int(round(tcneu/ttf * 100))
    tep = int(round(tep / ttf * 100))
    ten = int(round(ten/ttf * 100))
    teneu = int(round(teneu/ttf * 100))
    tlwp = int(round(tlwp / ttf * 100))
    tlwn = int(round(tlwn/ttf * 100))
    tlwneu = int(round(tlwneu/ttf * 100))
    tlfp = int(round(tlfp / ttf * 100))
    tlfn = int(round(tlfn/ttf * 100))
    tlfneu = int(round(tlfneu/ttf * 100))
    tecp = int(round(tecp / ttf * 100))
    tecn = int(round(tecn/ttf * 100))
    tecneu = int(round(tecneu/ttf * 100))
    
    data = [ttp, ttn, ttneu, tcp, tcn, tcneu, tep, ten, teneu, tlwp, tlwn, tlwneu,  tlfp, tlfn, tlfneu, tecp, tecn, tecneu]
    role = f'teacher{teachernumber}'
    
    if teachernumber == 1:
        ttp, ttn, ttneu = data[0:3]
        return render_template('teacherdashboard.html', role=role, ttf=ttf, ttp=ttp, ttn=ttn, ttneu=ttneu)
    elif teachernumber == 2:
        ttp, ttn, ttneu = data[3:6]
        return render_template('teacherdashboard.html', role=role, ttf=ttf, ttp=ttp, ttn=ttn, ttneu=ttneu)
    elif teachernumber == 3:
        ttp, ttn, ttneu = data[6:9]
        return render_template('teacherdashboard.html', role=role, ttf=ttf, ttp=ttp, ttn=ttn, ttneu=ttneu)
    elif teachernumber == 4:
        ttp, ttn, ttneu = data[9:12]
        return render_template('teacherdashboard.html', role=role, ttf=ttf, ttp=ttp, ttn=ttn, ttneu=ttneu)
    elif teachernumber == 5:
        ttp, ttn, ttneu = data[12:15]
        return render_template('teacherdashboard.html', role=role, ttf=ttf, ttp=ttp, ttn=ttn, ttneu=ttneu)
    else:
        ttp, ttn, ttneu = data[15:18]
        return render_template('teacherdashboard.html', role=role, ttf=ttf, ttp=ttp, ttn=ttn, ttneu=ttneu)

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return render_template('login.html')


@app.route("/predict", methods=['POST'])
def predict():
    if not session.get('logged_in'):
        return render_template('login.html')
    
    username = session.get('username')

    teaching = request.form['teaching']
    courseContent = request.form['coursecontent']
    examination = request.form['examination']
    labWork = request.form['labwork']
    libraryFacilities = request.form['libraryfacilities']
    extraCurricular = request.form['extracurricular']

    teacher1 = request.form['teacher1']
    teacher2 = request.form['teacher2']
    teacher3 = request.form['teacher3']
    teacher4 = request.form['teacher4']
    teacher5 = request.form['teacher5']
    teacher6 = request.form['teacher6']

    model = pickle.load(open('SVM classifier.pkl', 'rb'))
    teachingscore = model.predict(pd.array([teaching]))
    courseContentscore = model.predict(pd.array([courseContent]))
    examinationscore = model.predict(pd.array([examination]))
    labWorkscore = model.predict(pd.array([labWork]))
    libraryFacilitiesscore = model.predict(pd.array([libraryFacilities]))
    extraCurricularscore = model.predict(pd.array([extraCurricular]))
    time = datetime.now().strftime("%m/%d/%Y (%H:%M:%S)")

    teacher1score = model.predict(pd.array([teacher1]))
    teacher2score = model.predict(pd.array([teacher2]))
    teacher3score = model.predict(pd.array([teacher3]))
    teacher4score = model.predict(pd.array([teacher4]))
    teacher5score = model.predict(pd.array([teacher5]))
    teacher6score = model.predict(pd.array([teacher6]))

    write_to_csv_departments(time, teachingscore[0], teaching, courseContentscore[0], courseContent,
                             examinationscore[0], examination, labWorkscore[0], labWork, libraryFacilitiesscore[0],
                             libraryFacilities, extraCurricularscore[0], extraCurricular, username)

    write_to_csv_teachers(teacher1, teacher1score[0], teacher2, teacher2score[0], teacher3, teacher3score[0],
                          teacher4, teacher4score[0], teacher5, teacher5score[0], teacher6, teacher6score[0])

    return render_template('thankyoupage.html')


@app.route('/admin')
def root():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        total_feedbacks, total_positive_feedbacks, total_negative_feedbacks, total_neutral_feedbacks, li = get_counts()
        tp, tn, tneu, cp, cn, cneu, ep, en, eneu, lwp, lwn, lwneu, lfp, lfn, lfneu, ecp, ecn, ecneu = li
        teachers_total_feedbacks, teachers_total_positive_feedbacks, teachers_total_negative_feedbacks, teachers_total_neutral_feedbacks, teachers_li = get_feedback_counts()
        ttp, ttn, ttneu, tcp, tcn, tcneu, tep, ten, teneu, tlwp, tlwn, tlwneu, tlfp, tlfn, tlfneu, tecp, tecn, tecneu = teachers_li

        return render_template('admin.html', tf=total_feedbacks, tpf=total_positive_feedbacks, tnegf=total_negative_feedbacks, tneuf=total_neutral_feedbacks,
                               tp=tp, tn=tn, tneu=tneu, cp=cp, cn=cn, cneu=cneu, ep=ep, en=en, eneu=eneu,
                               lwp=lwp, lwn=lwn, lwneu=lwneu, lfp=lfp, lfn=lfn, lfneu=lfneu, ecp=ecp,
                               ecn=ecn, ecneu=ecneu,
                               ttf=teachers_total_feedbacks, ttpf=teachers_total_positive_feedbacks, ttnegf=teachers_total_negative_feedbacks,
                               ttneuf=teachers_total_neutral_feedbacks, ttp=ttp, ttn=ttn, ttneu=ttneu, tcp=tcp, tcn=tcn,
                               tcneu=tcneu, tep=tep, ten=ten, teneu=teneu, tlwp=tlwp, tlwn=tlwn,
                               tlwneu=tlwneu, tlfp=tlfp, tlfn=tlfn, tlfneu=tlfneu, tecp=tecp, tecn=tecn, tecneu=tecneu
                               )

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the 'file' key is in the request.files dictionary
    if 'file' not in request.files:
        return 'No file selected'

    uploaded_file = request.files['file']

    # Check if the file has a filename
    if uploaded_file.filename == '':
        return 'No file selected'

    try:
        # Save the uploaded file to the designated folder
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(file_path)

        # Call the enter_through_excel function with the correct path
        successful, errors = excel_fill.enter_through_excel(path=file_path)

        # Provide a response with information about successful queries and errors
        response_data = {
            'message': 'File uploaded and processed successfully',
            'successful_queries': successful,
            'errors': errors
        }

        return jsonify(response_data)
    except Exception as e:
        # Handle any errors and provide an appropriate response
        response_data = {'error': f'Error: {str(e)}'}
        return jsonify(response_data)

@app.route("/hoddashboard")
def hoddashboard():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        teachers_total_feedbacks, teachers_total_positive_feedbacks, teachers_total_negative_feedbacks, teachers_total_neutral_feedbacks, teachers_li = get_feedback_counts()
        ttp, ttn, ttneu, tcp, tcn, tcneu, tep, ten, teneu, tlwp, tlwn, tlwneu, tlfp, tlfn, tlfneu, tecp, tecn, tecneu = teachers_li
        return render_template('hoddashboard.html',
                               ttf=teachers_total_feedbacks, ttpf=teachers_total_positive_feedbacks,
                               ttnegf=teachers_total_negative_feedbacks,
                               ttneuf=teachers_total_neutral_feedbacks, ttp=ttp, ttn=ttn, ttneu=ttneu, tcp=tcp, tcn=tcn,
                               tcneu=tcneu, tep=tep, ten=ten, teneu=teneu, tlwp=tlwp, tlwn=tlwn,
                               tlwneu=tlwneu, tlfp=tlfp, tlfn=tlfn, tlfneu=tlfneu, tecp=tecp, tecn=tecn, tecneu=tecneu
                               )


@app.route("/displayteacherfeedbacks")
def displayteacherfeedbacks():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        df1 = pd.read_csv('dataset/teacherdb.csv')
        return render_template('teacherfeedbacks.html', tables=[df1.to_html(classes='data', header="true")])


@app.route("/display")
def display():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        df = pd.read_csv('dataset/database.csv')
        return render_template('feedbacks.html', tables=[df.to_html(classes='data', header="true")])


app.run(port=5978, host='0.0.0.0', debug=True)