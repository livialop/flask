from sqlalchemy import *

import schema

# Essa query está criando novamente o banco de dados, por isso está tendo erro no app.py
# Corrigir depois -> Tem que fazer conexão com a tabela sem criar o banco.
print(select(schema.users).filter_by(nome='nome').scalar_subquery())