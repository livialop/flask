# Páginas:
# Comprar produtos
# Visualizar produtos
# 

from flask import render_template, redirect, url_for, request, Blueprint, flash
from flask_login import login_required, current_user
from models.database import User, session, Product

products_bp: Blueprint = Blueprint('products', __name__, static_folder='static', template_folder='templates')

@products_bp.route('/buyproducts')
@login_required
def buyproducts():
    produtos: Product = session.query(Product).all()
    return render_template('buyproducts.html', produtos=produtos)


@products_bp.route('/viewproducts/<int:user_id>')
@login_required
def viewproducts(user_id):
    # Aqui, o usuário poderá ver os produtos que somente ele comprou
    # Buscar todos os produtos cujo user_id seja o id informado
    produtos = session.query(Product).filter_by(user_id=user_id).all()
    return render_template('viewproducts.html', produtos=produtos)
    
    

@products_bp.route('/insertproduct', methods=['GET', 'POST'])
@login_required
def insertproduct():
    if request.method == "POST":
        nome: str = request.form.get('nome') 
        descricao: str = request.form.get('descricao')
        preco: float = request.form.get('preco')
                
        try:
            preco: float = float(preco)
        except (TypeError, ValueError):
            flash('Preço inválido', category='error')
            return render_template('insertproduct.html')

        # associar o produto ao usuário logado
        user_id = getattr(current_user, 'id', None)
        novo_produto: Product = Product(nome=nome, descricao=descricao, preco=preco, user_id=user_id)
        novo_produto: Product = Product(nome=nome, descricao=descricao, preco=preco)
        session.add(novo_produto)
        session.commit()
        session.close()
        flash('Produto cadastrado', category='success')
        return redirect(url_for('products.buyproducts'))
    
    return render_template('insertproduct.html')