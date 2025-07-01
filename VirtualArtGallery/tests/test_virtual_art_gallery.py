import unittest
from datetime import date
from dao.virtualArtGallery_impl import VirtualArtGalleryImpl
from entity.artwork import Artwork
from entity.gallery import Gallery

class TestVirtualArtGallery(unittest.TestCase):
    def setUp(self):
        self.gallery = VirtualArtGalleryImpl()
        cursor = self.gallery._connection.cursor()
        try:
            # Clean old test data
            cursor.execute("DELETE FROM User_Favorite_Artwork")
            cursor.execute("DELETE FROM Artwork")
            cursor.execute("DELETE FROM Gallery")
            cursor.execute("DELETE FROM User")
            cursor.execute("DELETE FROM Artist")

            # Insert required User
            cursor.execute("INSERT INTO User (UserID, Username, Password, Email) VALUES (%s, %s, %s, %s)",
                           (1, "testuser", "password123", "test@example.com"))

            # Insert Artist (used by Artwork and Gallery)
            cursor.execute("INSERT INTO Artist (ArtistID, Name, Biography, BirthDate, Nationality, Website) VALUES (%s, %s, %s, %s, %s, %s)",
                           (1, "Test Artist", "Bio", "1990-01-01", "India", "http://artist.com"))

            # Insert Artwork
            cursor.execute("""
                INSERT INTO Artwork (ArtworkID, Title, Description, CreationDate, Medium, ImageURL, ArtistID)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (1, "Test Artwork", "A test piece", date(2023, 1, 1), "Oil", "http://test.com", 1))

            # Insert Gallery
            test_gallery = Gallery(1, "Test Gallery", "A test gallery", "Delhi", "9AM-5PM", 1)
            self.gallery.addGallery(test_gallery)

            self.gallery._connection.commit()
        except Exception as e:
            print(f"Error setting up test data: {e}")
            self.gallery._connection.rollback()
        finally:
            cursor.close()

    # Artwork Management Tests
    def test_add_artwork(self):
        new_artwork = Artwork(2, "New Artwork", "A new piece", date(2024, 1, 1), "Watercolor", "http://newart.com", 1)
        self.assertTrue(self.gallery.addArtwork(new_artwork))

    def test_update_artwork(self):
        artwork = Artwork(1, "Updated Artwork", "Updated description", date.today(), "Oil", "http://updated.com", 1)
        self.assertTrue(self.gallery.updateArtwork(artwork))

    def test_remove_artwork(self):
        self.assertTrue(self.gallery.removeArtwork(1))

    def test_get_artwork_by_id(self):
        artwork = self.gallery.getArtworkById(1)
        self.assertIsNotNone(artwork)
        self.assertEqual(artwork.get_artwork_id(), 1)

    def test_search_artworks(self):
        artworks = self.gallery.searchArtworks("Test")
        self.assertGreaterEqual(len(artworks), 1)
        self.assertTrue(any(a.get_title() == "Test Artwork" for a in artworks))

    # User Favorites Tests
    def test_add_artwork_to_favorite(self):
        self.assertTrue(self.gallery.addArtworkToFavorite(1, 1))

    def test_remove_artwork_from_favorite(self):
        self.gallery.addArtworkToFavorite(1, 1)
        self.assertTrue(self.gallery.removeArtworkFromFavorite(1, 1))

    def test_get_user_favorite_artworks(self):
        self.gallery.addArtworkToFavorite(1, 1)
        favorites = self.gallery.getUserFavoriteArtworks(1)
        self.assertGreaterEqual(len(favorites), 1)
        self.assertTrue(any(a.get_artwork_id() == 1 for a in favorites))

    # Gallery Management
    def test_add_gallery(self):
        new_gallery = Gallery(2, 'AddGallery', 'A new gallery', 'Gondia', '9AM-4PM', 1)
        self.assertTrue(self.gallery.addGallery(new_gallery))

    def test_update_gallery(self):
        gallery = Gallery(1, 'Updated Gallery', 'Updated description', 'Mumbai', '9AM-4PM', 1)
        self.assertTrue(self.gallery.updateGallery(gallery))

    def test_search_gallery(self):
        galleries = self.gallery.searchGalleries("Test")
        self.assertGreaterEqual(len(galleries), 1)
        self.assertTrue(any(a.get_name() == "Test Gallery" for a in galleries))

    def test_remove_gallery(self):
        self.assertTrue(self.gallery.removeGallery(1))

    def tearDown(self):
        cursor = self.gallery._connection.cursor()
        try:
            cursor.execute("DELETE FROM User_Favorite_Artwork")
            cursor.execute("DELETE FROM Artwork_Gallery")
            cursor.execute("DELETE FROM Artwork")
            cursor.execute("DELETE FROM Gallery")
            cursor.execute("DELETE FROM User")
            cursor.execute("DELETE FROM Artist")
            self.gallery._connection.commit()
        except Exception as e:
            print(f"Error cleaning up test data: {e}")
            self.gallery._connection.rollback()
        finally:
            cursor.close()
            if self.gallery._connection.is_connected():
                self.gallery._connection.close()

if __name__ == "__main__":
    unittest.main()