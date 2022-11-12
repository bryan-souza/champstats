from fastapi import APIRouter, Depends, Response, status
from fastapi_jwt_auth import AuthJWT

from app.models import Championship
from app.controllers import ChampionshipController
from app.exceptions import NotFoundError

router = APIRouter(prefix='/jogos/{game_id}/campeonatos')


@router.get('/', status_code=status.HTTP_200_OK)
async def get_all_championships(
        championship_controller: ChampionshipController = Depends(ChampionshipController)
):
    return await championship_controller.get_all()


@router.post('/', status_code=status.HTTP_201_CREATED)
async def insert_championship(
        champ: Championship,
        championship_controller: ChampionshipController = Depends(ChampionshipController),
        auth: AuthJWT = Depends()
):
    auth.jwt_required()
    return await championship_controller.insert(champ)


@router.get('/{champ_id}', status_code=status.HTTP_200_OK)
async def get_championship_by_id(
        champ_id,
        championship_controller: ChampionshipController = Depends(ChampionshipController)
):
    try:
        return await championship_controller.get_by_id(champ_id)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{champ_id}', status_code=status.HTTP_200_OK)
async def update_game(
        champ_id,
        champ: Championship,
        championship_controller: ChampionshipController = Depends(ChampionshipController),
        auth: AuthJWT = Depends()
):
    auth.jwt_required()
    try:
        return await championship_controller.update(champ_id, champ)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.delete('/{champ_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_game(
        champ_id,
        championship_controller: ChampionshipController = Depends(ChampionshipController),
        auth: AuthJWT = Depends()
):
    auth.jwt_required()
    try:
        await championship_controller.delete(champ_id)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
