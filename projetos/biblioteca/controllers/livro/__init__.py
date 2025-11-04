from flask import render_template, redirect, url_for, request, Blueprint, flash
from flask_login import login_required
from database import Usuario, Livro, session


livros_bp = Blueprint('livros', __name__, static_folder='static', template_folder='templates')


@livros_bp.route('/add_livro', methods=['GET', 'POST'])
@login_required
def add_livro():
    pass

@livros_bp('/view_livro')
@login_required
def view_livro():
    pass

