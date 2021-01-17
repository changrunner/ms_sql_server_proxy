class ApiReponse:
    def __init__(self, response):
        self.response = response

    @property
    def status_code(self):
        return self.response.status_code

    @property
    def content(self):
        return self.response.data.decode().replace('\n', '').replace(' ', '')
