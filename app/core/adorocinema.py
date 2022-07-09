import requests
import lxml
import lxml.html
import urllib.parse
import base64

class adoroCinemaTitle(object):
    def __init__(self,
        title_type,
        title_name,
        title_id,
        title_date=None,
        title_genre=[]
    ):
        self.title_type = title_type
        self.title_name = title_name
        self.title_id = title_id
        self.title_date = title_date
        self.title_genre = title_genre
        self.summary = False
        self.source_page = False
    def get_data(self):
        self.get_source_page_title()
        self.get_summary()
        self.get_detail()
    def get_source_page_title(self):
        type_title_principal = 'filmes' if self.title_type == 'movie' else 'series'
        type_title_second = 'filme' if self.title_type == 'movie' else 'serie'
        url = f'https://www.adorocinema.com/{type_title_principal}/{type_title_second}-{self.title_id}/'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                self.source_page = response
        except Exception as err:
            print('adoroCinemaTitle.get_source_page_title exception - {err}')
        return False
    def get_summary(self):
        if self.source_page:
            response_xml = lxml.html.fromstring(self.source_page.text)
            elem_temp = response_xml.xpath('//section[@id="synopsis-details"]')
            if elem_temp:
                elem_synopsis = elem_temp[0]
                data_synopsis = elem_synopsis.xpath('./div[@class="content-txt "]')
                if data_synopsis:
                    self.summary = data_synopsis[0].text_content().strip()
    def get_detail(self):
        pass


class adoroCinemaMovie(adoroCinemaTitle):
    def __init__(self,
        title_type,
        title_name,
        title_id,
        title_date=None,
        title_genre=[]
    ):
        adoroCinemaTitle.__init__(
            self,
            title_type=title_type,
            title_name=title_name,
            title_id=title_id,
            title_date=title_date,
            title_genre=title_genre
        )


class adoroCinemaSeasonEpisode(object):
    def __init__(self,
        poster,
        name,
        summary
    ):
        self.poster = poster
        self.name = name
        self.summary = summary



class adoroCinemaSeason(object):
    def __init__(self,
        number,
        status,
        start_date,
        total_episodes,
        title_id,
        season_id
    ):
        self.number = number
        self.status = status
        self.start_date = start_date
        self.total_episodes = total_episodes
        self.title_id = title_id
        self.season_id = season_id
        self.episodes = []
    def get_data(self):
        url = f'https://www.adorocinema.com/series/serie-{self.title_id}/temporada-{self.season_id}/'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                body_xml = lxml.html.fromstring(response.text)
                ep_elem = body_xml.xpath('//div[@class="entity-card episode-card entity-card-list cf hred"]')
                for episode in ep_elem:
                    try:
                        poster_ep = episode.xpath('./figure/div/img')[0]
                    except Exception as err_poster:
                        print(f'adoroCinemaSeason.get_data.poster exception {err_poster}')
                        poster_ep = ''
                    try:
                        summary = episode.xpath('./div[@class="content-txt synopsis"]')[0].text_content().strip()
                    except Exception as err1:
                        print(f'adoroCinemaSeason.get_data.summary exception {err1}')
                        summary = ''
                    try:
                        name = episode.xpath('./div/div/span')[0].text_content().strip()
                    except Exception as err_name:
                        print(f'adoroCinemaSeason.get_data.name exception {err_name}')
                        try:
                            name = episode.xpath('./div/div/a')[0].text_content().strip()
                        except Exception as err_name:
                            print(f'adoroCinemaSeason.get_data.name2 exception {err_name}')
                            name = ''
                    data = adoroCinemaSeasonEpisode(poster=poster_ep, name=name, summary=summary)
                    self.episodes.append(data)
        except Exception as err:
            print(f'adoroCinemaSeason.get_data exception - {err}')




class adoroCinemaSerie(adoroCinemaTitle):
    def __init__(self,
        title_type,
        title_name,
        title_id,
        title_date=None,
        title_genre=[]
    ):
        adoroCinemaTitle.__init__(
            self,
            title_type=title_type,
            title_name=title_name,
            title_id=title_id,
            title_date=title_date,
            title_genre=title_genre
        )
        self.season = []
    def get_season(self):
        url = 'https://graph.adorocinema.com/v1/mobile/'
        headers = {
            'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1NzE4NDY2MzYsInVzZXJuYW1lIjoiYW5vbnltb3VzIiwiYXBwbGljYXRpb25fbmFtZSI6Im1vYmlsZSIsInV1aWQiOiI5YzNjYThmMS0xYjdlLTQ4OWQtOGZkYS1jNGM3ODZjNWFhMjgiLCJzY29wZSI6bnVsbCwiZXhwIjoxNjg2NzAwNzk5fQ.bCQXh2gdyUcD8OYHE3HKmuADzPtAw-7gGi_A2UcpmnZVZigpTJewbe2ubfjGBgEcEODrp5or7vVMQAcGQC1LIWuWC061OZAP9hRoFA6sCA36eFYlTmrY8t_h_QGpqQcNqpkESOU1kZLntPZrdA5JhzZ_F1AtiP0rxpv5tx3qpzfv1JZacl4kP3DZR7uTR6lx_duggkfOGMzwzFqwU_Q1yVLbKdHVpQu6_H4Zb_-es25g2eD-8sUjYit__DPJjT4Z1DPq_IfMJdO4h3gptQQpys8Ggke5jHtcRhEZJ0vsGBbzdb-ijCgWxC2Jb3O9joK7MI5vgeMGXbdvtytN4rgyPePlnVTyDYsaYvX7FQ-agEnXcT8GbHIU9TfnuhzG4oHYQjDcj0TK-C3hV2L9kVhC6ZcGpJLb8R9FBh9M1UmAOjkLdE4-fww-RNr_befVW-7xS5sJGRll6KKJv6CxXW0jn5nlzxPeTpOSIwfCDEqtedQw5CHsmDRCzvMlZmwwtDwqDL3pE5fBk_hvZinbsdY2hlLY8-6JPafOYarjJKDYV--rGiTAH1QuHaJ1ENz44vMw-wCc_tSuii79wVxbeLI-rRuvzWNqxZZdTOT4vL5l67cOC2ZbCOe2AsmqdMoXk2BZxyhILnUUtK1ol8s13X5stfvkvWQhY-DhbFBi1i2eDQc',
            'User-Agent': 'androidapp/0.0.1',
            'Accept-Encoding': 'gzip',
            'AC-Auth-Token': 'c0sQHsxHjVc:APA91bGuxQEP17duEKuftmpZd19xFNS7RJxwN-LV8ptoDdzPuvlt_TknGpCtB-aSmEGJ-zi962l9KzfY5zDCqFaRIodK6MAcn73HFCy3oTHHEGqzdOXeJQux6ILxoz-4d3_jfgcYxPU7',
            'Content-Type': 'application/json; charset=utf-8',
            'Host': 'graph.adorocinema.com'
        }
        id = f'Series:{self.title_id}'
        id_b64 = base64.b64encode(id.encode()).decode()
        payload = {
            "query": "query SeriesSeasonList($id: String, $after: String, $count: Int) { series(id: $id) { __typename id title seasons(after: $after, first: $count, order: [NUMBER_DESC]) { __typename totalCount pageInfo { __typename hasNextPage endCursor } edges { __typename node { __typename ...SeasonFragmentLight } } } } } fragment SeasonFragmentLight on Season { __typename id series { __typename id poster { __typename url } } status number startsAt episodes { __typename totalCount } stats { __typename userRating { __typename score(base: 5) } } videos(order: [LATEST], type: [TRAILER, TEASER], first: 1) { __typename id internalId } poster { __typename url } }",
            "variables": {
                "id": id_b64
            }
        }
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                for season in response.json().get('data', {}).get('series', {}) \
                            .get('seasons', {}).get('edges', []):
                    season_id_temp = base64.b64decode(season.get('node', {}).get('id', False)).decode()
                    season_id = season_id_temp.split(':')[1].strip()
                    data = adoroCinemaSeason(
                        number=season.get('node', {}).get('number', False),
                        status=season.get('node', {}).get('status', False),
                        start_date=season.get('node', {}).get('startsAt', False),
                        total_episodes=season.get('node', {}).get('episodes', {}).get('totalCount', False),
                        title_id=self.title_id,
                        season_id=season_id
                    )
                    self.season.append(data)
        except Exception as err:
            print('adoroCinemaSerie.get_season exception - {err}')
    def get_detail(self):
        self.get_season()





class adoroCinema(object):
    def find_by_name(self, name):
        name_encoded = urllib.parse.quote(name)
        url = f'https://www.adorocinema.com/_/autocomplete/{name_encoded}'
        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
        }
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                if response.json().get('error', True) == False:
                    list_titles = []
                    for title in response.json().get('results', []):
                        if title.get('entity_type', False) in ('movie', 'series'):
                            if title.get('entity_type', False) == 'series':
                                data = adoroCinemaSerie(
                                    title_type=title.get('entity_type', False),
                                    title_name=title.get('original_label', False),
                                    title_id=title.get('entity_id', False),
                                    title_date=title.get('data', {}).get('year', False),
                                    title_genre=title.get('genres', [])
                                )
                            elif title.get('entity_type', False) == 'movie':
                                data = adoroCinemaMovie(
                                    title_type=title.get('entity_type', False),
                                    title_name=title.get('original_label', False),
                                    title_id=title.get('entity_id', False),
                                    title_date=title.get('data', {}).get('year', False),
                                    title_genre=title.get('genres', [])
                                )
                            list_titles.append(data)
                    return list_titles
        except Exception as err:
            print(f'adoroCinema.find_by_name exception - {err}')
        return False
    def load_serie_by_id(self, id):
        url = f'https://www.adorocinema.com/series/serie-{id}'
        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
        }
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                xml = lxml.html.fromstring(response.text)
                data = adoroCinemaSerie(
                    title_type='series',
                    title_name='kkkk',
                    title_id=id,
                    title_date=None,
                    title_genre=None
                )
                return data
        except Exception as err:
            print(f'adoroCinema.load_serie_by_id exception - {err}')
        return False



adorocinema_instance = adoroCinema()

def get_adorocinema_instance():
    return adorocinema_instance