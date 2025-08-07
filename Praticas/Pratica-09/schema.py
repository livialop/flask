from sqlalchemy import * 

engine = create_engine('sqlite:///banco.db')

meta = MetaData()

users = Table('users', meta,
    Column('id', Integer, primary_key=True),
    Column('nome', String(120), nullable=False, key='nome'),
    Column('senha', Text, nullable=False, key='senha')
)

users.create(engine)

print(engine)
print(meta)
print(users)
