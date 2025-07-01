class ArtistNotFoundException(Exception):
    def __init__(self, message="Artist not found in database"):
        self.message = message
        super().__init__(self.message)
