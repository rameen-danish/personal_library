import json
import streamlit as st
import time  # Import time module for delays

# Class to manage the library
class PersonalLibraryManager:
    def __init__(self, filename="library.json"):
        """Initialize the library and load books."""
        self.filename = filename
        self.backup_filename = "library_backup.json"
        self.library = self.load_library()

    def load_library(self):
        """Load books from JSON file, return an empty list if file is missing or corrupted."""
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_library(self):
        """Save books to JSON file and create a backup."""
        with open(self.filename, "w") as file:
            json.dump(self.library, file, indent=4)
        with open(self.backup_filename, "w") as backup_file:
            json.dump(self.library, backup_file, indent=4)

    def add_book(self, title, author, year, genre, read_status):
        """Add a new book to the library."""
        self.library.append({"title": title, "author": author, "year": year, "genre": genre, "read": read_status})
        self.save_library()

    def remove_book(self, title):
        """Remove a book from the library."""
        matching_books = [book for book in self.library if book["title"].lower() == title.lower()]
        if matching_books:
            self.library = [book for book in self.library if book["title"].lower() != title.lower()]
            self.save_library()
            return True
        return False

    def search_book(self, query):
        """Search for books by title or author (case-insensitive)."""
        return [book for book in self.library if query.lower() in book["title"].lower() or query.lower() in book["author"].lower()]

    def mark_as_read_unread(self, title):
        """Toggle read/unread status for a book."""
        for book in self.library:
            if book["title"].lower() == title.lower():
                book["read"] = not book["read"]
                self.save_library()
                return book
        return None

    def get_statistics(self):
        """Get statistics of books in the library."""
        total_books = len(self.library)
        read_books = sum(book["read"] for book in self.library)
        percentage_read = (read_books / total_books * 100) if total_books else 0
        return total_books, read_books, percentage_read


# Initialize library manager
manager = PersonalLibraryManager()

# Set page config
st.set_page_config(page_title="📚 Personal Library Manager", layout="wide")

# Display title
st.title("📚 Personal Library Manager")

# Tabs for Navigation
tabs = st.tabs(["🏠 Home", "➕ Add Book", "🔍 Search Book", "❌ Remove Book", "📊 Statistics", "🚪 Exit"])

# 🏠 Home Tab
with tabs[0]:
    st.subheader("Your Library 📖")
    books = manager.library
    if books:
        for idx, book in enumerate(books, start=1):
            col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])
            with col1:
                st.write(f"📖 **{book['title']}**")
            with col2:
                st.write(f"✍️ {book['author']}")
            with col3:
                st.write(f"📅 {book['year']}")
            with col4:
                st.write(f"🏷️ {book['genre']}")
            with col5:
                if st.button(f"✅ {'Read' if book['read'] else 'Unread'}", key=idx):
                    manager.mark_as_read_unread(book["title"])
                    st.rerun()
    else:
        st.write("📌 No books in your library. Add some!")

# ➕ Add Book Tab
with tabs[1]:
    st.subheader("➕ Add a New Book")

    title = st.text_input("📖 Book Title")
    author = st.text_input("✍️ Author")
    year = st.number_input("📅 Year (4-digit)", min_value=1000, max_value=9999, step=1)
    genre = st.text_input("🏷️ Genre")
    read_status = st.checkbox("✅ Read")

    if st.button("Add Book"):
        if title and author and genre and 1000 <= year <= 9999:
            manager.add_book(title, author, year, genre, read_status)
            st.success(f"✅ '{title}' added successfully!")

            time.sleep(2)  # Wait for 2 seconds so the user sees the success message
            st.rerun()  # Refresh the UI
        else:
            st.error("❌ Please fill all fields correctly!")

# 🔍 Search Book Tab
with tabs[2]:
    st.subheader("🔍 Search for a Book")
    query = st.text_input("Enter title or author")

    if query:
        results = manager.search_book(query)
        if results:
            for book in results:
                st.write(f"📖 **{book['title']}** | ✍️ {book['author']} | 📅 {book['year']} | 🏷️ {book['genre']} | ✅ {'Read' if book['read'] else 'Unread'}")
        else:
            st.warning("❌ No matching books found.")

# ❌ Remove Book Tab
with tabs[3]:
    st.subheader("❌ Remove a Book")
    title = st.text_input("Enter book title to remove")

    if st.button("Remove Book"):
        if title:
            book_removed = manager.remove_book(title)  # Check if book exists
            if book_removed:
                st.success(f"✅ '{title}' has been removed successfully!")
                time.sleep(2)  # Wait for 2 seconds
                st.rerun()  # Refresh UI
            else:
                st.error("❌ Book not found! Please enter a valid title.")
        else:
            st.error("❌ Please enter a valid title.")

# 📊 Statistics Tab
with tabs[4]:
    st.subheader("📊 Library Statistics")
    total_books, read_books, percentage_read = manager.get_statistics()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📚 Total Books", total_books)
    with col2:
        st.metric("✅ Read Books", read_books)
    with col3:
        st.metric("📖 Completion Rate", f"{percentage_read:.1f}%")

    st.progress(percentage_read / 100)

# 🚪 Exit Tab
with tabs[5]:
    st.subheader("🚪 Exit the Application")

    if st.button("Exit"):
        st.warning("✅ Exiting application... Please close the browser tab.")
        st.stop()  # Stop the app execution
# Footer
st.markdown("<br><hr><center>Made with ❤️ by Rameen Rashid</center>", unsafe_allow_html=True)