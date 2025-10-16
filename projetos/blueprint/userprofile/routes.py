from flask import Blueprint, render_template
from flask_login import login_required, current_user
from database import *

userprofile_bp = Blueprint('userprofile', __name__, template_folder='templates', static_folder='static')

@userprofile_bp.route('/profile')
@login_required
def profile():
    # Aqui, futuramente, o aluno pode adicionar relacionamento com posts, tarefas etc.
    user_id = current_user.id
    usuario = session.get(User, user_id)
    livros = usuario.livros
    session.close()
    print(current_user.livros)
    return render_template('profile.html', user=current_user, livros=livros)