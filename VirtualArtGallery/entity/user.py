from datetime import date

class User:
    def __init__(self,userid='',
                 username='',
                 password='',
                 email='',
                 first_name='',
                 last_name='',
                 date_of_birth='',
                 profile_picture='',
                 favorite_artworks=''):
        self.__userid=userid
        self.__username=username
        self.__password=password
        self.__email=email
        self.__first_name=first_name
        self.__last_name=last_name
        self.__date_of_birth=date_of_birth
        self.__profile_picture=profile_picture
        self.__favorite_artworks=favorite_artworks

    # Getter

    def get_userid(self):
        return self.__userid
    def get_username(self):
        return self.__username
    def get_password(self):
        return self.__password
    def get_email(self):
        return self.__email
    def get_first_name(self):
        return self.__first_name
    def get_last_name(self):
        return self.__last_name
    def get_date_of_birth(self):
        return self.__date_of_birth
    def get_profile_picture(self):
        return self.__profile_picture
    def get_favorite_artworks(self):
        return self.__favorite_artworks


    #Setter

    def userid(self,value):
        self.__userid=value

    def username(self,value):
        self.__username=value

    def password(self,value):
        self.__password=value

    def email(self,value):
        self.__email=value

    def first_name(self,value):
        self.__first_name=value

    def last_name(self,value):
        self.__last_name=value

    def date_of_birth(self,value):
        self.__date_of_birth=value

    def profile_picture(self,value):
        self.__profile_picture=value

    def favorite_artworks(self,value):
        self.__favorite_artworks=value


