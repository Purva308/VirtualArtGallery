# 🎨 Virtual Art Gallery Management System

The **Virtual Art Gallery Management System** is a console-based Python application connected to a MySQL database. It allows administrators to manage artists, artworks, galleries, and users in a digital gallery system. It supports full CRUD operations, user-artwork interaction (like favoriting), and includes a full suite of unit tests.

---

## 🧰 Features

### 👨‍🎨 Artist Management
- Add, update, delete, and search artists.
- Store artist bio, birthdate, nationality, and website.

### 🖼️ Artwork Management
- Create and manage artworks.
- Each artwork is linked to an artist and includes a title, medium, image URL, and creation date.

### 🏛️ Gallery Management
- Manage gallery records with location, opening hours, and assigned artist.
- Assign or remove artworks from galleries.
- View artworks inside a gallery.

### 👤 User Management
- Add and manage users.
- Users can favorite/unfavorite artworks.

### 🔍 Search & Reporting
- Search across artists, artworks, and galleries by keyword.

### ✅ Unit Testing
- Tests for all major operations using `unittest`.
- Automatic test data setup and teardown for isolation.

---

## 🛠️ Technologies Used

- **Python 3.x**
- **MySQL** (Database)
- **mysql-connector-python** (for DB access)
- **OOP** principles (modular, class-based structure)
- **`unittest`** for testing
- **`tabulate`** (optional, for table display formatting)

---
