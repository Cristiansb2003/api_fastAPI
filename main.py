from fastapi import FastAPI
from fastapi import HTTPException

from database import database as connection
from database import User
from database import UserReview
from database import Movie
from schemas import UserBaseModel

app = FastAPI(title='Proyecto para reseñar peliculas',
              description='En este proyecto seremos capaces de reseñar peliculas.',
              version='1')
@app.on_event('startup')
def startup():
    if connection.is_closed():
        connection.connect()
        print('Conexion exitosa')
    connection.create_tables([User, Movie, UserReview])

@app.on_event('shutdown')
def shutdown():
    if not connection.is_closed():
        connection.close()
        print('Conexion cerrada')

@app.get('/')
async def index():
    return 'Hola mundo, desde un servidor en FastAPI'

@app.post('/users')
async def create_user(user:UserBaseModel):
    if User.select().where(User.username == user.username).exists():
        return HTTPException(409, 'El username ya se encuentra en uso.')
    hash_password = User.create_password(user.password)
    user = User.create(
        username = user.username,
        password = hash_password
    )
    return {
        'id': user.id,
        'username':user.username
    }
