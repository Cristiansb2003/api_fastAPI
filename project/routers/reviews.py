from typing import List

from fastapi import APIRouter
from fastapi import HTTPException

from ..database import User
from ..database import Movie
from ..database import UserReview

from ..schemas import ReviewRequestModel
from ..schemas import ReviewResponseModel
from ..schemas import ReviewRequestPutModel

router = APIRouter(prefix='/reviews')

@router.post('', response_model= ReviewResponseModel)
async def create_review(user_review: ReviewRequestModel):

    if User.select().where(User.id == user_review.user_id).first() is None:
        raise HTTPException(status_code=404, detail="User not found")

    if Movie.select().where(Movie.id == user_review.movie_id).first() is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    user_review = UserReview.create(
        user_id = user_review.user_id,
        movie_id = user_review.movie_id,
        review = user_review.review,
        score= user_review.score
    )

    return user_review

@router.get('', response_model=List[ReviewResponseModel])
async def get_reviews(page:int = 1, limit:int = 10):
    #el primer argumento(page) hace referencia a la pagina actual
    #el segundo argumento hace referencia a la capacitad maxima
    reviews = UserReview.select().paginate(page,limit)#SELECT * FROM user_reviews;

    return [user_review for user_review in reviews]

@router.get('/{review_id}', response_model=ReviewResponseModel)
async def get_review(review_id:int):
    user_review = UserReview.select().where(UserReview.id == review_id).first()

    if user_review is None:
        raise HTTPException(status_code=404, detail= 'Review Not found')
    return user_review

@router.put('/{review_id}', response_model=ReviewResponseModel)
async def update_review(review_id:int, review_request: ReviewRequestPutModel):
    user_review = UserReview.select().where(UserReview.id == review_id).first()

    if user_review is None:
        raise HTTPException(status_code=404, detail= 'Review Not found')
    
    user_review.review = review_request.review
    user_review.score = review_request.score

    user_review.save()

    return user_review

@router.delete('/{review_id}', response_model=ReviewResponseModel)
async def delete_review(review_id:int):
    user_review = UserReview.select().where(UserReview.id == review_id).first()
    if user_review is None:
        raise HTTPException(status_code=404, detail= 'Review Not found')

    user_review.delete_instance()

    return user_review