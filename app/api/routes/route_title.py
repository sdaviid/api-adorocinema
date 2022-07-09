import os
from typing import List
from sqlalchemy.orm import Session
from fastapi import(
    Depends,
    Response,
    status,
    APIRouter,
    File,
    UploadFile
)
from fastapi.responses import JSONResponse

from app.models.domain.title import(
    Title
)
from app.core.adorocinema import(
    adoroCinemaTitle,
    adoroCinemaMovie,
    adoroCinemaSeasonEpisode,
    adoroCinemaSeason,
    adoroCinemaSerie,
    adoroCinema,
    get_adorocinema_instance
)



from app.core.database import get_db

router = APIRouter()


@router.post(
    '/create',
    status_code=status.HTTP_200_OK
)
def upload(
    info: str,
    response: Response,
    db: Session = Depends(get_db)
):
    temp = Title.add(session=db, info=info)
    if temp:
        return temp
    else:
        return {
            "error": True,
            "message": "Failed add info"
        }


@router.get(
    '/list',
    status_code=status.HTTP_200_OK,
)
def detail(
    response: Response,
    db: Session = Depends(get_db)
):
    temp_response = Title.list_all(session=db)
    if temp_response:
        return temp_response
    else:
        return {
            "error": True,
            "message": "No results"
        }

@router.get(
    '/find/serie/{id_father}/{number_season}',
    status_code=status.HTTP_200_OK
)
def get_by_season(
    id_father: str,
    number_season: int,
    db: Session = Depends(get_db),
    adorocinema_instance: adoroCinema = Depends(get_adorocinema_instance)
):
    temp_data = adorocinema_instance.load_serie_by_id(id_father)
    if temp_data:
        temp_data.get_data()
        try:
            temp_list = list(reversed(temp_data.season))
            temp_list[int(number_season - 1)].get_data()
            response = []
            for episode in temp_list[int(number_season - 1)].episodes:
                t = {
                    'poster': episode.poster,
                    'name': episode.name,
                    'summary': episode.summary
                }
                response.append(t)
            return response
        except Exception as err:
            print(f'route_title.get_by_season exception - {err}')
            return {
                "error": True,
                "message": "No results"
            }
    else:
        return {
            "error": True,
            "message": "No results"
        }



@router.get(
    '/find/{query}',
    status_code=status.HTTP_200_OK,
)
def find_by_name(
    query: str,
    response: Response,
    db: Session = Depends(get_db),
    adorocinema_instance: adoroCinema = Depends(get_adorocinema_instance)
):
    temp_data = adorocinema_instance.find_by_name(query)
    if temp_data:
        temp_response = []
        for item in temp_data:
            item.get_data()
            temp = {
                'title': item.title_name,
                'type': item.title_type,
                'date': item.title_date,
                'id': item.title_id,
                'summary': item.summary
            }
            if(item.title_type == 'series'):
                temp_seasons = []
                for season in list(reversed(item.season)):
                    temp_season = {
                        'season_id': season.season_id,
                        'number': season.number,
                        'date': season.start_date,
                        'total_episodes': season.total_episodes,
                        'status': season.status,
                    }
                    temp_seasons.append(temp_season)
                temp.update({'season': temp_seasons})
            temp_response.append(temp)
        temp_response.sort(key=lambda item:item['date'], reverse=False)
        return temp_response
    else:
        return {
            "error": True,
            "message": "No results"
        }