# Páginas:
# Comprar produtos
# Visualizar produtos
# 

from flask import render_template, redirect, url_for, request, Blueprint, flash
from flask_login import login_required, current_user
from models.database import User, session, Product

products_bp: Blueprint = Blueprint('products', __name__, static_folder='static', template_folder='templates')

@products_bp.route('/buyproducts', methods=['GET', 'POST'])
def buyproducts():
    produtos: Product = session.query(Product).where(Product.disponivel==True).all()
    
    if request.method == 'POST':
        id_produto = request.form.get('id')
        produto_usuario = session.get(Product, id_produto)
        produto_usuario.user_id = current_user.id 
        produto_usuario.disponivel = False
        return redirect(url_for('products.viewproducts'))

    return render_template('buyproducts.html', produtos=produtos)


@products_bp.route('/viewproducts')
@login_required
def viewproducts():
    # Aqui, o usuário poderá ver os produtos que somente ele comprou
    produtos = session.query(Product).filter_by(user_id=current_user.id).where(Product.disponivel==False).all()
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
        user_id = current_user.id
        novo_produto: Product = Product(nome=nome, descricao=descricao, preco=preco, user_id=user_id)
        session.add(novo_produto)
        session.commit()
        session.close()
        flash('Produto cadastrado', category='success')
        return redirect(url_for('products.buyproducts'))
    
    return render_template('insertproduct.html')