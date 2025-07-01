class Artwork_Gallery:
    def __init__(self,artwork_id='',gallery_id=''):
        self.__artwork_id=artwork_id
        self.__gallery_id=gallery_id

    # Getter
    def get_artwork_id(self):
        return self.__artwork_id
    def get_gallery_id(self):
        return self.__gallery_id

    #Setter

    def artwork_id(self,value):
        self.__artwork_id=value

    def gallery_id(self,value):
        self.__gallery_id=value


