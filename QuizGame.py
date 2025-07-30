from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'quiz_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(300), nullable=False)
    option1 = db.Column(db.String(100), nullable=False)
    option2 = db.Column(db.String(100), nullable=False)
    option3 = db.Column(db.String(100), nullable=False)
    option4 = db.Column(db.String(100), nullable=False)
    answer = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    session['score'] = 0
    session['qno'] = 1
    return render_template('index4.html', page='index')

@app.route('/question/<int:qno>', methods=['GET', 'POST'])
def question(qno):
    total = Question.query.count()
    if qno > total:
        return redirect(url_for('result'))

    q = Question.query.get(qno)
    if request.method == 'POST':
        selected = request.form.get('option')
        if selected == q.answer:
            session['score'] += 1
        return redirect(url_for('question', qno=qno + 1))

    return render_template('index4.html', page='question', question=q, qno=qno)

@app.route('/result')
def result():
    score = session.get('score', 0)
    total = Question.query.count()
    return render_template('index4.html', page='result', score=score, total=total)

@app.route('/add', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        q = request.form['question']
        op1 = request.form['option1']
        op2 = request.form['option2']
        op3 = request.form['option3']
        op4 = request.form['option4']
        ans = request.form['answer']

        new_q = Question(
            question=q,
            option1=op1,
            option2=op2,
            option3=op3,
            option4=op4,
            answer=ans
        )
        db.session.add(new_q)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('index4.html', page='add_question')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=9000)
