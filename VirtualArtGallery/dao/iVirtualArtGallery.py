from abc import ABC,abstractmethod

class IVirtualArtGallery(ABC):

    #Artwork Management

    @abstractmethod
    def addArtwork(self, artwork):
        pass

    @abstractmethod
    def updateArtwork(self, artwork):
        pass

    @abstractmethod
    def removeArtwork(self,artwork_id):
        pass

    @abstractmethod
    def getArtworkById(self,artwork_id):
        pass

    @abstractmethod
    def searchArtworks(self,keyword):
        pass

    @abstractmethod
    def getAllArtwork(self):
        pass

    #Artist Management

    @abstractmethod
    def addArtist(self, artist):
        pass

    @abstractmethod
    def updateArtist(self, artist):
        pass

    @abstractmethod
    def removeArtist(self, artist_id):
        pass

    @abstractmethod
    def getArtistbById(self, artist_id):
        pass

    @abstractmethod
    def searchArtists(self, keyword):
        pass

    @abstractmethod
    def getAllArtist(self):
        pass

    #User Management
    @abstractmethod
    def addUser(self, user):
        pass

    @abstractmethod
    def updateUser(self, user):
        pass

    @abstractmethod
    def removeUser(self, userid):
        pass

    @abstractmethod
    def getUserById(self, userid):
        pass

    @abstractmethod
    def searchUsers(self, keyword):
        pass
    @abstractmethod
    def getAllUser(self):
        pass

    #Gallery Management

    @abstractmethod
    def addGallery(self, gallery):
        pass
    @abstractmethod
    def updateGallery(self, gallery):
        pass

    @abstractmethod
    def removeGallery(self, gallery_id):
        pass

    @abstractmethod
    def getGalleryById(self, gallery_id):
        pass

    @abstractmethod
    def searchGalleries(self, keyword):
        pass
    @abstractmethod
    def getAllGallery(self):
        pass

    #Artwork_to_Gallery

    @abstractmethod
    def assignArtworkToGallery(self, artwork_id, gallery_id):
        pass

    @abstractmethod
    def removeArtworkFromGallery(self, artwork_id, gallery_id):
        pass

    @abstractmethod
    def getArtworksInGallery(self, gallery_id):
        pass

    #User_Favorites

    @abstractmethod
    def addArtworkToFavorite(self,userid,artwork_id):
        pass

    def updateArtworkToFavorite(self,userid,artwork_id,new_artwork_id):
        pass

    @abstractmethod
    def removeArtworkFromFavorite(self,userid,artwork_id):
        pass

    @abstractmethod
    def getUserFavoriteArtworks(self,userid):
        pass




