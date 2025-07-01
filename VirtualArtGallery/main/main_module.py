from dao.virtualArtGallery_impl import VirtualArtGalleryImpl
from entity.artwork import Artwork
from entity.user import User
from entity.gallery import Gallery
from entity.artist import Artist
from entity.artwork_Gallery import Artwork_Gallery
from entity.user_Favorite_Artwork import User_Favorite_Artwork
from datetime import date
from exception.artWorkNotFoundException import ArtworkNotFoundException
from exception.userNotFoundException import UserNotFoundException
from exception.artistNotFoundException import ArtistNotFoundException
from exception.galleryNotFoundException import GalleryNotFoundException
from tabulate import tabulate
import re


def safe_int_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

def is_valid_contact(contact):
    pattern = r"^\+?\d{10,15}$"
    return re.match(pattern, contact) is not None

def is_valid_password(password):
    # At least 8 characters, 1 uppercase, 1 lowercase, 1 digit, 1 special character
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    return re.match(pattern, password) is not None

def input_valid_password(prompt="Enter password:"):
    while True:
        password = input(prompt)
        if is_valid_password(password):
            return password
        else:
            print("Invalid password. Password must have at least 8 characters, including one uppercase, one lowercase, one digit, and one special character.")

def validate_foreign_key(entity_list, id_to_check, key_method):
    return any(getattr(e, key_method)() == id_to_check for e in entity_list)

def artwork_menu(gallery):
    while True:
        print("\n=========== Artwork Menu ==========")
        print("1. Add Artwork")
        print("2. Update Artwork")
        print("3. Remove Artwork")
        print("4. Get Artwork by ID")
        print("5. Search Artworks")
        print("6. Get All Artwork")
        print("7. Back to Main Menu")

        choice = input("Enter your choice: ")
        try:

            if choice == "1":
                artist_id = safe_int_input("Enter Artist ID: ")
                if not validate_foreign_key(gallery.getAllArtist(), artist_id, "get_artist_id"):
                    print("Invalid Artist ID. Please add the artist first or choose a valid one.")
                    continue
                artwork = Artwork(
                    artwork_id=None,
                    title=(input("Enter Title: ")),
                    description=(input("Enter Description: ")),
                    creation_date=date.today(),
                    medium=input("Enter Medium: "),
                    image_url=input("Enter Image URL:"),
                    artist_id=artist_id

                )
                artwork_id = gallery.addArtwork(artwork)

                if artwork_id:
                    print(f"Artwork Added Successfully!  Artwork ID: {artwork_id}")
                else:
                    print("Failed to Add Artwork.")

            elif choice == "2":
                artist_id = safe_int_input("Enter Artist ID: ")
                if not validate_foreign_key(gallery.getAllArtist(), artist_id, "get_artist_id"):
                    print("Invalid Artist ID. Please add the artist first or choose a valid one.")
                    continue
                artwork = Artwork(
                    artwork_id=safe_int_input("Enter Artwork ID:"),
                    title=(input("Enter Title: ")),
                    description=(input("Enter Description: ")),
                    creation_date=date.today(),
                    medium=input("Enter Medium: "),
                    image_url=input("Enter Image URL:"),
                    artist_id=artist_id
                )
                if gallery.updateArtwork(artwork):
                    print("Artwork Updated Successfully!")
                else:
                    print("Failed to Update Artwork.")

            elif choice == "3":
                artwork_id = int(input("Enter Artwork ID to remove: "))
                if gallery.removeArtwork(artwork_id):
                    print("Artwork Removed Successfully!")
                else:
                    print("Failed to Remove Artwork.")

            elif choice == "4":
                artwork_id = int(input("Enter Artwork ID: "))
                try:
                    artwork = gallery.getArtworkById(artwork_id)
                    if artwork:
                        headers = ["ArtworkID", "Title", "Description", "CreationDate", "Medium", "ImageURL", "ArtistID"]
                        print(tabulate([[
                        artwork.get_artwork_id(),
                        artwork.get_title(),
                        artwork.get_description(),
                        artwork.get_creation_date(),
                        artwork.get_medium(),
                        artwork.get_image_url(),
                        artwork.get_artist_id()
                        ]], headers=headers, tablefmt="grid"))
                    else:
                        raise ArtworkNotFoundException(f"Artwork ID {artwork_id}not found.")
                except ArtworkNotFoundException as e:
                    print(f"Error:{e}")

            elif choice == "5":
                keyword = input("Enter search keyword {Title,Description}:")
                artworks = gallery.searchArtworks(keyword)
                for artwork in artworks:
                    if artwork:
                        headers = ["ArtworkID", "Title", "Description", "CreationDate", "Medium", "ImageURL", "ArtistID"]
                        print(tabulate([[
                            artwork.get_artwork_id(),
                            artwork.get_title(),
                            artwork.get_description(),
                            artwork.get_creation_date(),
                            artwork.get_medium(),
                            artwork.get_image_url(),
                            artwork.get_artist_id()
                        ]], headers=headers, tablefmt="grid"))
                    else:
                        print("Artwork not found.")

            elif choice == "6":
                artwork = gallery.getAllArtwork()
                if artwork:
                    headers = ["ArtworkID", "Title", "Description", "CreationDate", "Medium", "ImageURL", "ArtistID"]
                    rows=[]
                    for artwork in artwork:
                        rows.append([
                            artwork.get_artwork_id(),
                            artwork.get_title(),
                            artwork.get_description(),
                            artwork.get_creation_date(),
                            artwork.get_medium(),
                            artwork.get_image_url(),
                            artwork.get_artist_id()
                    ])
                    print(tabulate(rows,headers=headers, tablefmt="grid"))
                else:
                    print("Artwork not found.")

            elif choice == "7":
                break

            else:
                print("Invalid choice. Please try again.")

        except (ArtworkNotFoundException, ValueError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

def user_menu(gallery):
    while True:
        print("\n============ User Menu ===========")
        print("1. Add User")
        print("2. Update User")
        print("3. Remove User")
        print("4. Get User by ID")
        print("5. Search Users")
        print("6. Add Artwork to Favorites")
        print("7. Remove Artwork from Favorites")
        print("8. Get User Favorite Artworks")
        print("9. Get All Users")
        print("10. Back to Main Menu")

        choice =input("Enter your choice: ")

        try:
            if choice == "1":
                userid = None
                username = input("Enter username: ")
                password = input_valid_password()
                email = input("Enter Email: ")
                if not is_valid_email(email):
                    print("Invalid email format.")
                    continue
                first_name = input("Enter First Name: ")
                last_name = input("Enter Last Name: ")
                profile_picture = input("Add profile picture: ")
                favorite_artworks = safe_int_input("Enter the favorite artwork ID: ")

                user = User(userid, username, password, email, first_name, last_name, date.today(), profile_picture,
                            favorite_artworks)
                userid = gallery.addUser(user)
                if userid:
                    print(f"User Added Successfully! User ID:{userid}")
                else:
                    print("Failed to Add User.")

            elif choice=="2":
                userid = safe_int_input("Enter User ID to update: ")
                username = input("Enter username: ")
                password = input_valid_password()
                email = input("Enter Email: ")
                if not is_valid_email(email):
                    print("Invalid email format.")
                    continue
                first_name = input("Enter First Name: ")
                last_name = input("Enter Last Name: ")
                profile_picture = input("Add profile picture: ")
                favorite_artworks = safe_int_input("Enter favorite artwork ID: ")

                user = User(userid, username, password, email, first_name, last_name, date.today(), profile_picture,
                            favorite_artworks)
                if gallery.updateUser(user):
                    print("User Updated Successfully!")
                else:
                    print("Failed to Update User.")

            elif choice=="3":
                userid = int(input("Enter User ID to remove: "))
                if gallery.removeUser(userid):
                    print("User Removed Successfully!")
                else:
                    print("Failed to Remove User.")

            elif choice == "4":
                userid = int(input("Enter User ID: "))
                user = gallery.getUserById(userid)
                if user:
                    headers = ["UserID", "Username", "Password", "Email", "First Name", "Last Name", "DOB",
                               "Profile Picture", "FavoriteArtworks"]
                    print(tabulate([[
                        user.get_userid(),
                        user.get_username(),
                        user.get_password(),
                        user.get_email(),
                        user.get_first_name(),
                        user.get_last_name(),
                        user.get_date_of_birth(),
                        user.get_profile_picture(),
                        user.get_favorite_artworks()
                    ]], headers=headers, tablefmt="grid"))
                else:
                    print("User not found.")


            elif choice == "5":
                keyword = input("Enter Search keyword (Username or Email): ")
                users = gallery.searchUsers(keyword)
                if users:
                    table = []
                    headers = ["User ID", "Username", "Email", "Password", "Contact Info"]
                    for user in users:
                        table.append([
                            user.get_userid(),
                            user.get_username(),
                            user.get_email(),
                            user.get_password(),
                            user.get_date_of_birth()
                        ])
                    print(tabulate(table, headers=headers, tablefmt="grid"))
                else:
                    print("No users found.")

            elif choice =="6":
                userid = int(input("Enter User ID:"))
                artwork_id = int(input("Enter Artwork ID: "))
                if gallery.addArtworkToFavorite(userid, artwork_id):
                    print("Artwork added to favorites!")
                else:
                    print("Failed to add to favorites.")


            elif choice == "7":
                userid = int(input("Enter User ID:"))
                artwork_id = int(input("Enter Artwork ID: "))
                if gallery.removeArtworkFromFavorite(userid, artwork_id):
                    print("Artwork removed from favorites!")
                else:
                    print("Failed to remove from favorites.")

            elif choice == "8":
                userid = int(input("Enter User ID: "))
                artworks = gallery.getUserFavoriteArtworks(userid)
                if artworks:
                    headers = ["ArtworkID", "Title", "Description", "CreationDate", "Medium", "ImageURL", "ArtistID"]
                    table = [[
                        a.get_artwork_id(),
                        a.get_title(),
                        a.get_description(),
                        a.get_creation_date(),
                        a.get_medium(),
                        a.get_image_url(),
                        a.get_artist_id()
                    ] for a in artworks]
                    print(tabulate(table, headers=headers, tablefmt="grid"))
                else:
                    print("No favorite artworks found.")

            elif choice == "9":
                user = gallery.getAllUser()
                if user:
                    headers = ["UserID", "Username", "Password", "Email", "First Name", "Last Name", "DOB",
                               "Profile Picture", "FavoriteArtworks"]
                    rows=[]
                    for user in user:
                        rows.append([
                            user.get_userid(),
                            user.get_username(),
                            user.get_password(),
                            user.get_email(),
                            user.get_first_name(),
                            user.get_last_name(),
                            user.get_date_of_birth(),
                            user.get_profile_picture(),
                            user.get_favorite_artworks()
                    ])
                    print(tabulate(rows, headers=headers, tablefmt="grid"))
                else:
                    print("User not found.")


            elif choice=="10":
                break

            else:
                print("Invalid choice. Please try again.")
        except (UserNotFoundException,ValueError) as e:
            print(f"Error :{e}")
        except Exception as e:
            print(f"Unexpected error:{e}")

def gallery_menu(gallery):
    while True:
        print("\n=========== Gallery Menu ============")
        print("1. Add Gallery")
        print("2. Update Gallery")
        print("3. Remove Gallery")
        print("4. Get Gallery by ID")
        print("5. Search Galleries")
        print("6. Get All Gallery")
        print("7. Assign Artwork to Gallery")
        print("8. Remove Artwork from Gallery")
        print("9. View Artworks in Gallery")
        print("10. Back to Main Menu")

        choice = input("Enter your choice: ")
        try:
            if choice == "1":
                artist_id = safe_int_input("Enter Artist ID: ")
                if not validate_foreign_key(gallery.getAllArtist(), artist_id, "get_artist_id"):
                    print("Invalid Artist ID. Please add the artist first or choose a valid one.")
                    continue
                gal = Gallery(
                    gallery_id=None,
                    name=input("Enter Name: "),
                    description=input("Enter Description: "),
                    location=input("Enter Location: "),
                    opening_hours=input("Enter Opening Hours: "),
                    artist_id=artist_id

                )
                gallery_id=gallery.addGallery(gal)
                if gallery_id:
                    print(f"Gallery Added Successfully! Gallery ID:{gallery_id}")
                else:
                    print("Failed to Add Gallery.")

            elif choice=="2":
                gallery_id=safe_int_input("Enter Gallery ID: ")
                artist_id = safe_int_input("Enter Artist ID: ")
                if not validate_foreign_key(gallery.getAllArtist(), artist_id, "get_artist_id"):
                    print("Invalid Artist ID. Please add the artist first or choose a valid one.")
                    continue
                gal = Gallery(
                    gallery_id=gallery_id,
                    name=input("Enter Name: "),
                    description=input("Enter Description: "),
                    location=input("Enter Location: "),
                    opening_hours=input("Enter Opening Hours: "),
                    artist_id=artist_id
                )
                if gallery.updateGallery(gal):
                    print("Gallery Updated Successfully!")
                else:
                    print("Failed to Update Gallery.")

            elif choice=="3":
                gallery_id = int(input("Enter Gallery ID to remove: "))
                if gallery.removeGallery(gallery_id):
                    print("Gallery Removed Successfully!")
                else:
                    print("Failed to Remove Gallery.")

            elif choice=="4":
                gallery_id = int(input("Enter Gallery ID: "))
                gal = gallery.getGalleryById(gallery_id)
                if gal:
                    headers = ["GalleryID", "Name", "Description", "Location", "Opening Hours", "ArtistID"]
                    print(tabulate([[
                        gal.get_gallery_id(),
                        gal.get_name(),
                        gal.get_description(),
                        gal.get_location(),
                        gal.get_opening_hours(),
                        gal.get_artist_id()
                    ]], headers=headers, tablefmt="grid"))
                else:
                    print("Gallery not found.")

            elif choice=="5":
                keyword = input("Enter Search keyword (Name or Description or Location): ")
                galleries = gallery.searchGalleries(keyword)
                for gal in galleries:
                    print(gal.__dict__)

            elif choice=="6":
                gal=gallery.getAllGallery()
                if gal:
                    headers = ["GalleryID", "Name", "Description", "Location", "Opening Hours", "ArtistID"]
                    rows=[]
                    for g in gal:
                        rows.append([
                        g.get_gallery_id(),
                        g.get_name(),
                        g.get_description(),
                        g.get_location(),
                        g.get_opening_hours(),
                        g.get_artist_id()
                    ])
                    print(tabulate(rows, headers=headers, tablefmt="grid"))
                else:
                    print("Gallery not found.")

            elif choice=="7":
                artwork_id = int(input("Enter Artwork ID: "))
                gallery_id = int(input("Enter Gallery ID: "))
                if gallery.assignArtworkToGallery(artwork_id,gallery_id) :
                    print("Assigned Successfully!")
                else:
                    print("Failed to Assign.")

            elif choice == "8":
                artwork_id = int(input("Enter Artwork ID: "))
                gallery_id = int(input("Enter Gallery ID: "))
                if gallery.removeArtworkFromGallery(artwork_id,gallery_id) :
                    print("Removed Successfully!")
                else :
                    print("Failed to Remove.")

            elif choice == "9":
                gallery_id = int(input("Enter Gallery ID: "))
                artworks = gallery.getArtworksInGallery(gallery_id)
                if artworks:
                    headers = ["ArtworkID", "Title", "Medium", "CreationDate", "ImageURL", "ArtistID"]
                    table = [[
                        art['ArtworkID'],
                        art['Title'],
                        art['Medium'],
                        art['CreationDate'],
                        art['ImageURL'],
                        art['ArtistID']
                    ] for art in artworks]
                    print(tabulate(table, headers=headers, tablefmt="grid"))
                else:
                    print("No artworks found in gallery.")

            elif choice=="10":
                break

            else:
                print("Invalid choice. Please try again.")
        except (GalleryNotFoundException,ValueError)as e:
            print(f"Error:{e}")
        except Exception as e:
            print(f"Unexpected error:{e}")

def artist_menu(gallery):
    while True:
        print("\n========= Artist Menu ===========")
        print("1. Add Artist")
        print("2. Update Artist")
        print("3. Remove Artist")
        print("4. Get Artist by ID")
        print("5. Search Artists")
        print("6. Get All Artist")
        print("7. Back to Main Menu")

        choice = input("Enter your choice: ")
        try:
            if choice == "1":
                contact_info = input("Enter Contact Info: ")
                while not is_valid_contact(contact_info):
                    print("Invalid contact format. Must be 10-15 digits, optional + prefix.")
                    contact_info = input("Enter Contact Info: ")
                artist = Artist(
                    artist_id=None,
                    name=input("Enter Name: "),
                    biography=input("Enter Biography: "),
                    birthDate=input("Enter BirthDate (YYYY-MM-DD): "),
                    nationality=input("Enter Nationality: "),
                    website=input("Enter Website: "),
                    contactInformation=contact_info
                )
                artist_id = gallery.addArtist(artist)

                if artist_id:
                    print(f"Artist Added Successfully!  Artist ID: {artist_id}")
                else:
                    print("Failed to Add Artist.")

            elif choice == "2":
                artist_id=safe_int_input("Enter Artist ID:")
                contact_info = input("Enter Contact Info: ")
                while not is_valid_contact(contact_info):
                    print("Invalid contact format. Must be 10-15 digits, optional + prefix.")
                    contact_info = input("Enter Contact Info: ")
                artist = Artist(
                    artist_id=artist_id,
                    name=input("Enter Name: "),
                    biography=input("Enter Biography: "),
                    birthDate=input("Enter BirthDate (YYYY-MM-DD): "),
                    nationality=input("Enter Nationality: "),
                    website=input("Enter Website: "),
                    contactInformation=contact_info
                )
                if gallery.updateArtist(artist):
                    print("Artist Updated Successfully!")
                else:
                    print("Failed to Update Artist.")

            elif choice == "3":
                artist_id = int(input("Enter Artist ID to remove: "))
                if gallery.removeArtist(artist_id):
                    print("Artist Removed Successfully!")
                else:
                    print("Failed to Remove Artist.")

            elif choice == "4":
                artist_id = int(input("Enter Artist ID: "))
                artist = gallery.getArtistbById(artist_id)
                if artist:
                    headers = ["ArtistID", "Name", "Biography", "BirthDate", "Nationality", "Website", "ContactInfo"]
                    print(tabulate([[
                        artist.get_artist_id(),
                        artist.get_name(),
                        artist.get_biography(),
                        artist.get_birthDate(),
                        artist.get_nationality(),
                        artist.get_website(),
                        artist.get_contactInformation()
                    ]], headers=headers, tablefmt="grid"))
                else:
                    print("Artist not found.")

            elif choice == "5":
                keyword = input("Enter search keyword (Name or Biography): ")
                artists = gallery.searchArtists(keyword)
                if artists:
                    headers = ["ArtistID", "Name", "Biography", "BirthDate", "Nationality", "Website", "ContactInfo"]
                    rows = [[a.get_artist_id(), a.get_name(), a.get_biography(), a.get_birthDate(),
                             a.get_nationality(), a.get_website(), a.get_contactInformation()] for a in artists]
                    print(tabulate(rows, headers=headers, tablefmt="grid"))
                else:
                    print("No artists found.")


            elif choice == "6":
                try:
                    artists = gallery.getAllArtist()
                    if artists:
                        headers = ["ArtistID", "Name", "Biography", "BirthDate", "Nationality", "Website",
                                   "ContactInfo"]
                        rows = []
                        for a in artists:
                            rows.append([
                                a.get_artist_id(),
                                a.get_name(),
                                a.get_biography(),
                                a.get_birthDate(),
                                a.get_nationality(),
                                a.get_website(),
                                a.get_contactInformation()
                            ])
                        print(tabulate(rows, headers=headers, tablefmt="grid"))
                    else:
                        print("No artists found.")
                except Exception as e:
                    print(f"Unexpected error: {e}")


            elif choice == "7":
                break
            else:
                print("Invalid choice. Please try again.")
        except (ArtistNotFoundException,ValueError)as e:
            print(f"Error:{e}")
        except Exception as e:
            print(f"Unexpected error:{e}")

def main():
    try:
        gallery = VirtualArtGalleryImpl()
        while True:
            print("\n======== Virtual Art Gallery Main Menu ========")
            print("1. Artist Management")
            print("2. User Management")
            print("3. Artwork Management")
            print("4. Gallery Management")
            print("5. Exit")

            choice = input("Enter your choice: ")
            if choice == "1":
                artist_menu(gallery)
            elif choice == "2":
                user_menu(gallery)
            elif choice == "3":
                artwork_menu(gallery)
            elif choice == "4":
                gallery_menu(gallery)
            elif choice == "5":
                print("Exiting....")
                break
            else:
                print("Invalid choice. Please try again.")
    except Exception as e:
        print(f"Fatal error: {e}")


if __name__=="__main__":
    main()




