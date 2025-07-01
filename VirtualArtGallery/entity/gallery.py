class Gallery:
    def __init__(self,gallery_id='',
                 name='',
                 description='',
                 location='',
                 opening_hours='',
                 artist_id=''):
        self.__gallery_id=gallery_id
        self.__name=name
        self.__description=description
        self.__location=location
        self.__opening_hours=opening_hours
        self.__artist_id=artist_id

    # Getter
    def get_gallery_id(self):
        return self.__gallery_id
    def get_name(self):
        return self.__name
    def get_description(self):
        return self.__description
    def get_location(self):
        return self.__location
    def get_opening_hours(self):
        return self.__opening_hours
    def get_artist_id(self):
        return self.__artist_id

    #Setter

    def gallery_id(self,value):
        self.__gallery_id=value

    def name(self,value):
        self.__name=value

    def description(self,value):
        self.__description=value

    def location(self,value):
        self.__location=value

    def opening_hours(self,value):
        self.__opening_hours=value

    def artist_id(self,value):
        self.__artist_id=value



