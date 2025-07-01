class UserNotFoundException(Exception):
    """Custom exception for when a user is not found"""
    def __init__(self,message="User not found in the database"):
        self.message=message
        super().__init__(self.message)
