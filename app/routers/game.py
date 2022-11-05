from fastapi import APIRouter, Depends, Response, status

from app.models import Game
from app.controllers import GameController
from app.exceptions import NotFoundError

router = APIRouter(prefix='/jogos')


@router.get('/', status_code=status.HTTP_200_OK)
async def get_all_games(game_controller: GameController = Depends(GameController)):
    return await game_controller.get_all()


@router.post('/', status_code=status.HTTP_201_CREATED)
async def insert_game(game: Game, game_controller: GameController = Depends(GameController)):
    return await game_controller.insert(game)


@router.get('/{game_id}', status_code=status.HTTP_200_OK)
async def get_game_by_id(game_id, game_controller: GameController = Depends(GameController)):
    try:
        return await game_controller.get_by_id(game_id)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{game_id}', status_code=status.HTTP_200_OK)
async def update_game(game_id, game: Game, game_controller: GameController = Depends(GameController)):
    try:
        return await game_controller.update(game_id, game)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.delete('/{game_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_game(game_id, game_controller: GameController = Depends(GameController)):
    try:
        await game_controller.delete(game_id)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
