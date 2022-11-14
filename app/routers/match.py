from fastapi import APIRouter, Depends, HTTPException, Response, Path, status, Body
from fastapi_jwt_auth import AuthJWT

from app.controllers import MatchController
from app.exceptions import NotFoundError
from app.models import Match

router = APIRouter(prefix='/jogos/{game_id}/campeonatos/{champ_id}/partidas')


@router.get('/', status_code=status.HTTP_200_OK)
async def get_all_matches(
        match_controller: MatchController = Depends(MatchController)
):
    return await match_controller.get_all()


@router.post('/', status_code=status.HTTP_201_CREATED)
async def insert_match(
        champ_id=Path(...),
        match: Match = Body(...),
        match_controller: MatchController = Depends(MatchController),
        auth: AuthJWT = Depends()
):
    auth.jwt_required()
    return await match_controller.insert(champ_id, match)


@router.get('/{match_id}', status_code=status.HTTP_200_OK)
async def get_match_by_id(
        match_id=Path(...),
        match_controller: MatchController = Depends(MatchController)
):
    try:
        return await match_controller.get_by_id(match_id)
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{match_id}', status_code=status.HTTP_200_OK)
async def update_match(
        match_id=Path(...),
        match: Match = Body(...),
        match_controller: MatchController = Depends(MatchController),
        auth: AuthJWT = Depends()
):
    auth.jwt_required()
    try:
        return await match_controller.update(match_id, match)
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.delete('/{match_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_match(
        champ_id=Path(...),
        match_id=Path(...),
        match_controller: MatchController = Depends(MatchController),
        auth: AuthJWT = Depends()
):
    auth.jwt_required()
    try:
        await match_controller.delete(champ_id, match_id)
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
