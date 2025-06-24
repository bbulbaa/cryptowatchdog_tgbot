class CryptoClient:
    def __init__(self, api_key: str):
        self.session = httpx.Client(base_url=BASE_URL)
        self.session.headers.update({"X-API-Key": api_key})
    
    def get_prices(self):
        return self.session.get("/prices").json()