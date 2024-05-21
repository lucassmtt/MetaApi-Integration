import requests

from base import BaseMetaApi


class GraphApi(BaseMetaApi):
    def __init__(
            self,
            access_token: str = None,
    ):
        HOST = 'https://graph.facebook.com/'

        API_VERSIONS = [
            'v13.0'
            'v14.0'
            'v15.0'
            'v16.0'
            'v17.0'
            'v18.0'
            'v19.0'
        ]

        self.base_url = f'{HOST}{API_VERSIONS[-1]}/'

        if access_token is None:
            self.access_token = open('keys/access_token.txt').read().strip()
        else:
            self.access_token = access_token

    def search_me(self, params: dict = None, route: str = None):
        if params is None:
            params = {
                'access_token': self.access_token,
                'limit': 25  # Default limit from meta api doc
            }
        elif params['access_token'] is None:
            params['access_token'] = self.access_token

        if not self.base_url.endswith('/'):
            self.base_url += '/'

        if route is None:
            url = f'{self.base_url}me/adaccounts'
            route = 'adaccounts'
        else:
            url = f'{self.base_url}me/{route}'

        response = requests.get(url, params=params)

        if response.status_code == 200:
            adaccounts = response.json().get('data', [])

            if len(adaccounts) > 0:
                return [adaccount['id'] for adaccount in adaccounts]

        elif response.status_code in [400, 404, 429]:
            print(f'Error in search: {route}, error {response.status_code}')
            return []

        else:
            print(f'Unexpected error {response.status_code}')
            return []
        
