import sqlalchemy as sa
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)  # This column will not allow NULL
    email = sa.Column(sa.String, nullable=True)   # This column will allow NULL (default behavior)
    bio = sa.Column(sa.Text)                      # This column will also allow NULL (default behavior)



#

from sqlalchemy import select, create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import sessionmaker

# Define table metadata (if not using ORM mapped classes)
metadata = MetaData()
user_table = Table(
    'user_account', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('fullname', String)
)

# Create an engine and session (example for SQLite)
engine = create_engine('sqlite:///example.db')
metadata.create_all(engine) # Create tables if they don't exist
Session = sessionmaker(bind=engine)
session = Session()

# Insert some data for demonstration
session.execute(user_table.insert().values(name='spongebob', fullname='Spongebob Squarepants'))
session.execute(user_table.insert().values(name='patrick', fullname='Patrick Star'))
session.commit()

# Construct and execute a SELECT statement
stmt = select(user_table).where(user_table.c.name == 'spongebob')
result = session.execute(stmt)

# Iterate through results
for row in result:
    print(f"ID: {row.id}, Name: {row.name}, Fullname: {row.fullname}")

session.close()