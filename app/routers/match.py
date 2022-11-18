from fastapi import APIRouter, Depends, HTTPException, Response, Path, status, Body
from fastapi_jwt_auth import AuthJWT

from app.controllers import MatchController
from app.exceptions import NotFoundError
from app.models import Match

router = APIRouter(prefix='/jogos/{game_id}/campeonatos/{champ_id}/partidas')


@router.get('/', status_code=status.HTTP_200_OK)
async def get_all_matches(
        game_id: int = Path(...),
        champ_id: int = Path(...),
        match_controller: MatchController = Depends(MatchController)
):
    try:
        return await match_controller.get_all(game_id, champ_id)
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def insert_match(
        game_id: int = Path(...),
        champ_id: int = Path(...),
        match: Match = Body(...),
        match_controller: MatchController = Depends(MatchController),
        auth: AuthJWT = Depends()
):
    auth.jwt_required()
    try:
        return await match_controller.insert(game_id, champ_id, match)
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get('/{match_id}', status_code=status.HTTP_200_OK)
async def get_match_by_id(
        game_id: int = Path(...),
        champ_id: int = Path(...),
        match_id: int = Path(...),
        match_controller: MatchController = Depends(MatchController)
):
    try:
        return await match_controller.get_by_id(game_id, champ_id, match_id)
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{match_id}', status_code=status.HTTP_200_OK)
async def update_match(
        game_id: int = Path(...),
        champ_id: int = Path(...),
        match_id: int = Path(...),
        match: Match = Body(...),
        match_controller: MatchController = Depends(MatchController),
        auth: AuthJWT = Depends()
):
    auth.jwt_required()
    try:
        return await match_controller.update(game_id, champ_id, match_id, match)
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.delete('/{match_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_match(
        game_id: int = Path(...),
        champ_id: int = Path(...),
        match_id: int = Path(...),
        match_controller: MatchController = Depends(MatchController),
        auth: AuthJWT = Depends()
):
    auth.jwt_required()
    try:
        await match_controller.delete(game_id, champ_id, match_id)
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
