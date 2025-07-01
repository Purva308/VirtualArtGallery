from dao.iVirtualArtGallery import IVirtualArtGallery
from entity.artwork import Artwork
from entity.user import User
from entity.artist import Artist
from entity.gallery import Gallery
from entity.artwork_Gallery import Artwork_Gallery
from entity.user_Favorite_Artwork import User_Favorite_Artwork
from exception.artWorkNotFoundException import ArtworkNotFoundException
from exception.userNotFoundException import UserNotFoundException
from exception.artistNotFoundException import ArtistNotFoundException
from exception.galleryNotFoundException import GalleryNotFoundException
from util.dBConnectionUtil import DBConnUtil
from util.dBPropertyUtil import DBPropertyUtil
import mysql.connector

class VirtualArtGalleryImpl(IVirtualArtGallery):
    _connection =None

    def __init__(self):
        properties_file=r"C:\Users\Raunak\PycharmProjects\VirtualArtGallery\db.properties"
        conn_string=DBPropertyUtil.get_connection_string(properties_file)
        if not conn_string:
            raise Exception("Failed to initialize database connection :Invalid connection string")
        self._connection=DBConnUtil.get_connection(conn_string)


# Artwork Management

    def addArtwork(self, artwork):
        try:
            cursor=self._connection.cursor()
            sql="""INSERT INTO Artwork
                    (ArtworkID,Title ,Description ,CreationDate,Medium ,ImageURL,ArtistID)
                    VALUES (%s,%s, %s, %s, %s, %s, %s)"""
            values=(
                artwork.get_artwork_id(),
                artwork.get_title(),
                artwork.get_description(),
                artwork.get_creation_date(),
                artwork.get_medium(),
                artwork.get_image_url(),
                artwork.get_artist_id()
            )
            cursor.execute(sql,values)
            self._connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error adding artwork:{e}")
            return False


    def updateArtwork(self, artwork):
        try:
            cursor=self._connection.cursor()
            update_str="""
                    UPDATE Artwork
            SET ArtworkID=%s,Title=%s, Description=%s, CreationDate=%s ,Medium=%s,ImageURL=%s,ArtistID=%s
            WHERE ArtworkID=%s
            """
            values= (
                artwork.get_artwork_id(),
                artwork.get_title(),
                artwork.get_description(),
                artwork.get_creation_date(),
                artwork.get_medium(),
                artwork.get_image_url(),
                artwork.get_artist_id(),
                artwork.get_artwork_id()
            )
            cursor.execute(update_str,values)
            if cursor.rowcount ==0:
                raise ArtworkNotFoundException(f"Artwork with ID {artwork.get_artwork_id()} not found")

            self._connection.commit()
            return True
        except ArtworkNotFoundException as e:
            print(str(e))
            return False
        except Exception as e:
            print(f"Error updating artwork :{e}")
            self._connection.rollback()
            return False


    def removeArtwork(self,artwork_id):
        try:
            cursor=self._connection.cursor()
            del_str="DELETE FROM Artwork WHERE ArtworkID=%s"
            cursor.execute(del_str,(artwork_id,))

            if cursor.rowcount==0:
                raise ArtworkNotFoundException(f"Artwork with ID {artwork_id} not found")
            self._connection.commit()
            return True
        except ArtworkNotFoundException as e:
            print(str(e))
            return False
        except Exception as e:
            print(f"Error removing artwork: {e}")
            return False


    def getArtworkById(self,artwork_id):
        try:
            cursor=self._connection.cursor()
            get_str="SELECT * FROM Artwork WHERE ArtworkID=%s"
            cursor.execute(get_str,(artwork_id,))
            result=cursor.fetchone()
            if not result:
                raise ArtworkNotFoundException(
                    f"Artwork with ID {artwork_id} not found"
                )
            artwork = Artwork(
                artwork_id=result[0],
                title=result[1],
                description=result[2],
                creation_date=result[3],
                medium=result[4],
                image_url=result[5],
                artist_id=result[6]
            )
            return artwork
        except ArtworkNotFoundException as e:
            print(str(e))
            return None
        except mysql.connector.Error as e:
            print(f"Error fetching artwork:{e}")
            return None


    def searchArtworks(self,keyword):
        artworks=[]
        try:
            cursor=self._connection.cursor()
            sel_str="SELECT * FROM Artwork WHERE Title  LIKE %s OR Description  LIKE %s "
            search_term=f"%{keyword}%"
            cursor.execute(sel_str,(search_term,search_term))
            results=cursor.fetchall()
            for row in results:
                artwork=Artwork(
                    artwork_id=row[0],
                    title=row[1],
                    description=row[2],
                    creation_date=row[3],
                    medium=row[4],
                    image_url=row[5],
                    artist_id=row[6]
                )
                artworks.append(artwork)
                return artworks
        except mysql.connector.Error as e:
            print(f"Error searching artworks:{e}")
            return []

    def getAllArtwork(self):
        try:
            cursor=self._connection.cursor()
            cursor.execute("SELECT * FROM Artwork")
            results = cursor.fetchall()
            return [Artwork(*row) for row in results]

        except Exception as e:
            print(f"Error :{e}")


# User Artwork Favorite

    def addArtworkToFavorite(self,userid,artwork_id):
        try:
            cursor=self._connection.cursor()
            cursor.execute("SELECT UserID FROM User WHERE UserID=%s" ,(userid,))
            if not cursor.fetchone():
                raise UserNotFoundException(f"User with ID {userid} not found")

            cursor.execute("SELECT ArtworkID FROM Artwork WHERE ArtworkID=%s" ,(artwork_id,))
            if not cursor.fetchone():
                raise ArtworkNotFoundException(f"Artwork with ID {artwork_id} not found")

            # add to favorites
            ins_str="INSERT INTO User_Favorite_Artwork( UserID,ArtworkID ) VALUES (%s,%s)"
            cursor.execute(ins_str,(userid,artwork_id))
            self._connection.commit()
            return True
        except (UserNotFoundException,ArtworkNotFoundException) as e:
            print(str(e))
            return False
        except mysql.connector.Error as e:
            print(f"Error adding to favorites:{e}")
            return False

    def removeArtworkFromFavorite(self,userid,artwork_id):
        try:
            cursor=self._connection.cursor()
            cursor.execute("SELECT UserID FROM User WHERE UserID = %s", (userid,))
            if not cursor.fetchone():
                raise UserNotFoundException(f"User with ID {userid} not found")

            # Check if artwork exists
            cursor.execute("SELECT ArtworkID FROM Artwork WHERE ArtworkID = %s", (artwork_id,))
            if not cursor.fetchone():
                raise ArtworkNotFoundException(f"Artwork with ID {artwork_id} not found")
            # Remove from favorites
            del_str="DELETE FROM User_Favorite_Artwork WHERE UserID=%s AND ArtworkID=%s"
            cursor.execute(del_str,(userid,artwork_id))
            if cursor.rowcount ==0:
                print("No favorite entry found for the given user and artwork")
                return False
            self._connection.commit()
            return True
        except (UserNotFoundException,ArtworkNotFoundException)as e:
            print(str(e))
            return False
        except mysql.connector.Error as e:
            print(f"Error removing artwork from favorites:{e}")
            return False


    def getUserFavoriteArtworks(self,userid):
        artworks=[]
        try:
            cursor=self._connection.cursor()
            cursor.execute("SELECT UserID FROM User WHERE UserID=%s",(userid,))
            if not cursor.fetchone():
                raise UserNotFoundException(f"User with ID {userid} not found")

            sql="""
                SELECT a.ArtworkID, a.Title, a.Description, a.CreationDate, a.Medium, a.ImageURL, a.ArtistID
                FROM Artwork a
                JOIN User_Favorite_Artwork ufa ON a.ArtworkID = ufa.ArtworkID
                WHERE ufa.UserID = %s
            """
            cursor.execute(sql,(userid,))
            results=cursor.fetchall()
            for row in results:
                artwork=Artwork(
                    artwork_id=row[0],
                    title=row[1],
                    description=row[2],
                    creation_date=row[3],
                    medium=row[4],
                    image_url=row[5],
                    artist_id=row[6]
                )
                artworks.append(artwork)
                return artworks
        except UserNotFoundException as e:
            print(str(e))
            return []
        except mysql.connector.Error as e:
            print(f"Error fetching favorite artworks: {e}")
            return []


# Gallery Management

    def addGallery(self, gallery):
        try:
            cursor=self._connection.cursor()
            sql="""INSERT INTO Gallery
                    (GalleryID,Name ,Description ,Location,OpeningHours,ArtistID)
                    VALUES (%s,%s, %s, %s, %s, %s)"""
            values=(
                gallery.get_gallery_id(),
                gallery.get_name(),
                gallery.get_description(),
                gallery.get_location(),
                gallery.get_opening_hours(),
                gallery.get_artist_id()
            )
            cursor.execute(sql,values)
            self._connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error adding Gallery:{e}")
            return False

    def updateGallery(self, gallery):
        try:
            cursor = self._connection.cursor()
            query = """
                UPDATE Gallery
                SET Name=%s, Description=%s, Location=%s, OpeningHours=%s, ArtistID=%s
                WHERE GalleryID=%s
            """
            values = (
                gallery.get_name(),
                gallery.get_description(),
                gallery.get_location(),
                gallery.get_opening_hours(),
                gallery.get_artist_id(),
                gallery.get_gallery_id()
            )
            cursor.execute(query, values)
            self._connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print("Error updating gallery:", e)
            return False

    def removeGallery(self, gallery_id):
        try:
            cursor = self._connection.cursor()
            cursor.execute("DELETE FROM Gallery WHERE GalleryID=%s", (gallery_id,))
            self._connection.commit()
            if cursor.rowcount == 0:
                raise GalleryNotFoundException(f"No gallery with ID {gallery_id}")
            return True
        except Exception as e:
            print("Error:", e)
            return False

    def getGalleryById(self, gallery_id):
        try:
            cursor = self._connection.cursor()
            cursor.execute("SELECT * FROM Gallery WHERE GalleryID=%s", (gallery_id,))
            result = cursor.fetchone()
            if not result:
                raise GalleryNotFoundException(f"Gallery with ID {gallery_id} not found")
            return Gallery(*result)
        except Exception as e:
            print("Error:", e)
            return None

    def searchGalleries(self, keyword):
        try:
            cursor = self._connection.cursor()
            query = """SELECT * FROM Gallery WHERE Name LIKE %s OR Description LIKE %s OR Location LIKE %s"""
            like_keyword = f"%{keyword}%"
            cursor.execute(query, (like_keyword, like_keyword, like_keyword))
            results = cursor.fetchall()
            return [Gallery(*row) for row in results]
        except Exception as e:
            print("Error:", e)
            return []

    def getAllGallery(self):
        try:
            cursor= self._connection.cursor()
            cursor.execute("SELECT * FROM Gallery")
            results = cursor.fetchall()
            return [Gallery(*row) for row in results]
        except Exception as e:
            print(f"Error :{e}")


# User Management

    def addUser(self, user):
        try:
            cursor=self._connection.cursor()
            sql="""INSERT INTO User
                    (UserID,Username,Password,Email,FirstName ,LastName ,DateOfBirth,Profile_Picture,FavoriteArtworks)
                    VALUES (%s,%s, %s, %s, %s, %s, %s,%s,%s)"""
            values=(
                user.get_userid(),
                user.get_username(),
                user.get_password(),
                user.get_email(),
                user.get_first_name(),
                user.get_last_name(),
                user.get_date_of_birth(),
                user.get_profile_picture(),
                user.get_favorite_artworks()
            )
            cursor.execute(sql,values)
            self._connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error adding user:{e}")
            return False


    def updateUser(self, user):
        try:
            cursor = self._connection.cursor()
            sql = """UPDATE User SET Username=%s, Password=%s, Email=%s, FirstName=%s,
                     LastName=%s, DateOfBirth=%s, Profile_Picture=%s WHERE UserID=%s"""
            values = (
                user.get_username(),
                user.get_password(),
                user.get_email(),
                user.get_first_name(),
                user.get_last_name(),
                user.get_date_of_birth(),
                user.get_profile_picture(),
                user.get_userid()
            )
            cursor.execute(sql, values)
            self._connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print("Error:", e)
            return False

    def removeUser(self, userid):
        try:
            cursor = self._connection.cursor()
            cursor.execute("DELETE FROM User WHERE UserID=%s", (userid,))
            self._connection.commit()
            if cursor.rowcount == 0:
                raise UserNotFoundException(f"No user with ID {userid}")
            return True
        except Exception as e:
            print("Error:", e)
            return False

    def getUserById(self, userid):
        try:
            cursor = self._connection.cursor()
            cursor.execute("SELECT * FROM User WHERE UserID=%s", (userid,))
            result = cursor.fetchone()
            if not result:
                raise UserNotFoundException(f"User with ID {userid} not found")
            return User(*result)
        except Exception as e:
            print("Error:", e)
            return None

    def searchUsers(self, keyword):
        try:
            cursor = self._connection.cursor()
            query = """SELECT * FROM User WHERE Username LIKE %s OR Email LIKE %s"""
            like_keyword = f"%{keyword}%"
            cursor.execute(query, (like_keyword, like_keyword))
            results = cursor.fetchall()
            return [User(*row) for row in results]
        except Exception as e:
            print("Error:", e)
            return []

    def getAllUser(self):
        try:
            cursor=self._connection.cursor()
            cursor.execute("SELECT * FROM User")
            results = cursor.fetchall()
            return [User(*row) for row in results]
        except Exception as e:
            print(f"Error :{e}")


# Artist Management

    def addArtist(self, artist):
        try:
            cursor = self._connection.cursor()
            sql = """INSERT INTO Artist (ArtistID, Name, Biography, BirthDate, Nationality, Website, ContactInformation)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            values = (
                    artist.get_artist_id(),
                    artist.get_name(),
                    artist.get_biography(),
                    artist.get_birthDate(),
                    artist.get_nationality(),
                    artist.get_website(),
                    artist.get_contactInformation()
                      )
            cursor.execute(sql, values)
            self._connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error:,{e}")
            return None

    def updateArtist(self, artist):
        try:
            cursor = self._connection.cursor()
            sql = """UPDATE Artist SET Name=%s, Biography=%s, BirthDate=%s, Nationality=%s,
                        Website=%s, ContactInformation=%s WHERE ArtistID=%s"""
            values = (
                      artist.get_name(),
                      artist.get_biography(),
                      artist.get_birthDate(),
                      artist.get_nationality(),
                      artist.get_website(),
                      artist.get_contactInformation(),
                      artist.get_artist_id()
                      )
            cursor.execute(sql, values)
            self._connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error:, {e}")
            return False

    def removeArtist(self, artist_id):
        try:
            cursor = self._connection.cursor()
            cursor.execute("DELETE FROM Artist WHERE ArtistID=%s", (artist_id,))
            self._connection.commit()
            if cursor.rowcount == 0:
                raise ArtistNotFoundException(f"No artist with ID {artist_id}")
            return True
        except Exception as e:
            print(f"Error:, {e}")
            return False

    def getArtistbById(self, artist_id):
        try:
            cursor = self._connection.cursor()
            cursor.execute("SELECT * FROM Artist WHERE ArtistID=%s", (artist_id,))
            result = cursor.fetchone()
            if not result:
                raise ArtistNotFoundException(f"Artist with ID {artist_id} not found")
            return Artist(*result)
        except Exception as e:
            print(f"Error:, {e}")
            return None

    def searchArtists(self, keyword):
        try:
            cursor=self._connection.cursor()
            query = """SELECT * FROM Artist WHERE Name LIKE %s OR Biography LIKE %s"""
            like_keyword = f"%{keyword}%"
            cursor.execute(query, (like_keyword, like_keyword))
            results = cursor.fetchall()
            return [Artist(*row) for row in results]
        except Exception as e:
            print("Error:", e)
            return []

    def getAllArtist(self):
        try:
            cursor=self._connection.cursor()
            cursor.execute("SELECT * FROM Artist")
            results = cursor.fetchall()
            return [Artist(*row) for row in results]
        except Exception as e:
            print(f"Error :{e}")

    def assignArtworkToGallery(self, artwork_id, gallery_id):
        try:
            cursor = self._connection.cursor()
            query = "INSERT INTO Artwork_Gallery (ArtworkID, GalleryID) VALUES (%s, %s)"
            cursor.execute(query, (artwork_id,gallery_id))
            self._connection.commit()
            return True
        except mysql.connector.Error as e:
            print(f"Error assigning artwork to gallery: {e}")
            return False

    def removeArtworkFromGallery(self, artwork_id, gallery_id):
        try:
            cursor = self._connection.cursor()
            query = "DELETE FROM Artwork_Gallery WHERE ArtworkID = %s AND GalleryID = %s"
            cursor.execute(query, (artwork_id, gallery_id))
            self._connection.commit()
            return True
        except mysql.connector.Error as e:
            print(f"Error removing artwork from gallery: {e}")
            return False

    def getArtworksInGallery(self, gallery_id):
        try:
            cursor = self._connection.cursor(dictionary=True)
            query = """
                SELECT A.ArtworkID, A.Title, A.Medium, A.CreationDate, A.ImageURL, A.ArtistID
                FROM Artwork A
                JOIN Artwork_Gallery AG ON A.ArtworkID = AG.ArtworkID
                WHERE AG.GalleryID = %s
            """
            cursor.execute(query, (gallery_id,))
            artworks = cursor.fetchall()
            return artworks  # List of dicts
        except mysql.connector.Error as e:
            print(f"Error fetching artworks for gallery: {e}")
            return []

    def __del__(self):
        if self._connection:
            self._connection.close()












