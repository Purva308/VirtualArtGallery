from datetime import date


class Artwork:
    def __init__(self,artwork_id='',
                 title='',
                 description ='',
                 creation_date ='',
                 medium ='',
                 image_url='',
                 artist_id=''):
        self.__artwork_id=artwork_id
        self.__title=title
        self.__description=description
        self.__creation_date=creation_date or date.today()
        self.__medium=medium
        self.__image_url=image_url
        self.__artist_id=artist_id


    #Getters
    def get_artwork_id(self):
        return self.__artwork_id
    def get_title(self):
        return self.__title
    def get_description(self):
        return self.__description
    def get_creation_date(self):
        return self.__creation_date
    def get_medium(self):
        return self.__medium
    def get_image_url(self):
        return self.__image_url
    def get_artist_id(self):
        return self.__artist_id

    #Setter
    def artwork_id(self, value):
        self.__artwork_id = value

    def title(self, value):
        self.__title = value

    def description(self,value):
        self.__description=value

    def creation_date(self,value):
        self.__creation_date=value

    def medium(self,value):
        self.__medium=value

    def image_url(self,value):
        self.__image_url=value

    def artist_id(self,value):
        self.__artist_id=value

