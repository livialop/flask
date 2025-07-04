from flask import Flask, render_template, request, redirect, make_response, url_for
app = Flask(__name__)


# Página Inicial
@app.route('/')
def home():
    
    user = request.cookies.get('user')

    if user:
        return render_template('home.html', user=user)
    else:
        return render_template('home.html')


# Página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('user')
        cookie = request.form.get('cookie')

        response = make_response(redirect(url_for('home')))

        if cookie:
            response.set_cookie('user', user, max_age=7*24*60*60)
    
        return response

    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('home')))
    response.set_cookie('user', '', expires=0)
    redirect('/home')
    return response
    
@app.route('/quiz')
def quiz():
    return render_template('quiz.html')
