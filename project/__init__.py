
from fastapi import FastAPI

from project.database import database as connection
from project.database import User
from project.database import UserReview
from project.database import Movie

from .routers import user_router
from .routers import review_router


app = FastAPI(title='Proyecto para reseñar peliculas',
              description='En este proyecto seremos capaces de reseñar peliculas.',
              version='1')

app.include_router(user_router)
app.include_router(review_router)

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



