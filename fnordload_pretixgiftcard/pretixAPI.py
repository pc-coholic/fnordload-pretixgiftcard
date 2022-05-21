import requests


class pretixAPI(object):
    def __init__(self, host, token, organizer, event, product):
        self.host = host
        self.token = token
        self.organizer = organizer
        self.event = event
        self.product = product
        self.client = self._setup_client()

    def _setup_client(self):
        s = requests.Session()
        s.headers = {
            "Authorization": "Token {}".format(self.token),
            "Accept": "application/json, text/javascript",
        }

        return s

    def create_order(self, value):
        resp = self.client.post(
            '{host}/api/v1/organizers/{organizer}/events/{event}/orders/'.format(
                host=self.host,
                organizer=self.organizer,
                event=self.event
            ),
            json={
                'status': 'n',
                'locale': 'en',
                'positions': [{
                    'positionid': 1,
                    'item': self.product,
                    'price': value,
                    'answers': []
                }],
                'payment_provider': 'manual'
            }
        )
        return resp.json()['code']

    def mark_order_as_paid(self, order_code):
        resp = self.client.post(
            '{host}/api/v1/organizers/{organizer}/events/{event}/orders/{code}/payments/1/confirm/'.format(
                host=self.host,
                organizer=self.organizer,
                event=self.event,
                code=order_code,
            ),
            json={
                'send_mail': False,
                'force': True,
            }
        )
        return resp.json()['state']

    def get_secret(self, order_code):
        resp = self.client.get(
            '{host}/api/v1/organizers/{organizer}/events/{event}/orders/{code}/'.format(
                host=self.host,
                organizer=self.organizer,
                event=self.event,
                code=order_code,
            ),
        )
        return resp.json()['positions'][0]['secret']
