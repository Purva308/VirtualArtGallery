from datetime import date

class Artist:
    def __init__(self,artist_id='',
                 name='',
                 biography='',
                 birthDate='',
                 nationality='',
                 website='',
                 contactInformation=''):
        self.__artist_id=artist_id
        self.__name=name
        self.__biography=biography
        self.__birthDate=birthDate
        self.__nationality=nationality
        self.__website=website
        self.__contactInformation=contactInformation

    # Getter

    def get_artist_id(self):
        return self.__artist_id
    def get_name(self):
        return self.__name
    def get_biography(self):
        return self.__biography
    def get_birthDate(self):
        return self.__birthDate
    def get_nationality(self):
        return self.__nationality
    def get_website(self):
        return self.__website
    def get_contactInformation(self):
        return self.__contactInformation

    #Setter

    def artist_id (self,value):
        self.__artist_id=value

    def name(self,value):
        self.__name=value

    def biography(self,value):
        self.__biography=value

    def birthDate(self,value):
        self.__birthDate=value

    def nationality(self,value):
        self.__nationality=value

    def website(self,value):
        self.__website=value

    def contactInformation(self,value):
        self.__contactInformation=value




