# Páginas:
# Comprar produtos
# Visualizar produtos
# 

from flask import render_template, redirect, url_for, request, Blueprint, flash
from flask_login import login_required
from database.database import User, session, Product

products_bp: Blueprint = Blueprint('products', __name__, static_folder='static', template_folder='templates')

@products_bp.route('/buyproducts')
@login_required
def buyproducts():
    produtos = session.query(Product).all()
    print(produtos)


@products_bp.route('/viewproducts')
@login_required
def viewproducts():
    # Aqui, o usuário poderá ver os produtos que somente ele comprou
    pass