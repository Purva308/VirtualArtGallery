class User_Favorite_Artwork:
    def __init__(self,userid='',artwork_id=''):

        self.__userid=userid
        self.__artwork_id=artwork_id

    # Getter
    def get_userid(self):
        return self.__userid
    def get_artwork_id(self):
        return self.__artwork_id

    #Setter
    def userid(self,value):
        self.__userid=value

    def artwork_id(self,value):
        self.__artwork_id=value

