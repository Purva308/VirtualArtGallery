class ArtworkNotFoundException(Exception):
    """Custom exception for when an artwork is not found."""
    def __init__(self, message="Artwork not found in database"):
        self.message = message
        super().__init__(self.message)