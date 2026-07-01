class Book:
    def __init__(self, title: str, author: str, isbn: str, publication_year: int, is_available: bool = True) -> None:
        self._title = title
        self._author = author
        self._isbn = isbn
        self._publication_year = publication_year
        self._is_available = is_available

    @property
    def title(self) -> str:
        return self._title

    @property
    def author(self) -> str:
        return self._author

    @property
    def isbn(self) -> str:
        return self._isbn

    @property
    def publication_year(self) -> int:
        return self._publication_year

    @property
    def is_available(self) -> bool:
        return self._is_available

    def __str__(self) -> str:
        return f"{self._title} by {self._author}"

    def __repr__(self) -> str:
        return f"Book('{self._title}', '{self._author}', '{self._isbn}', {self._publication_year}, {self._is_available})"

    def mark_available(self) -> None:
        self._is_available = True

    def mark_borrowed(self) -> None:
        self._is_available = False


class Member:
    def __init__(self, name: str, member_id: str, borrowed_books: list[Book] | None = None) -> None:
        self._name = name
        self._member_id = member_id
        self._borrowed_books = borrowed_books if borrowed_books is not None else []

    @property
    def name(self) -> str:
        return self._name

    @property
    def member_id(self) -> str:
        return self._member_id

    @property
    def borrowed_books(self) -> list[Book]:
        return self._borrowed_books

    def borrow_book(self, book: Book) -> None:
        if not book.is_available:
            raise ValueError(
                f"Book '{book.title}' is not available for borrowing")
        if book in self._borrowed_books:
            raise ValueError(f"Member already has '{book.title}' borrowed")
        self._borrowed_books.append(book)
        book.mark_borrowed()

    def return_book(self, book: Book) -> None:
        if book not in self._borrowed_books:
            raise ValueError(f"Member does not have '{book.title}' borrowed")
        self._borrowed_books.remove(book)
        book.mark_available()

    def __str__(self) -> str:
        return f"{self._name} ({self._member_id})"

    def __repr__(self) -> str:
        return f"Member('{self._name}', '{self._member_id}', {len(self._borrowed_books)} books)"


class Library:
    def __init__(self, name: str, books: dict[str, Book] | None = None, members: dict[str, Member] | None = None) -> None:
        self._name = name
        self._books = books if books is not None else {}
        self._members = members if members is not None else {}

    @property
    def name(self) -> str:
        return self._name

    @property
    def books(self) -> dict[str, Book]:
        return self._books

    @property
    def members(self) -> dict[str, Member]:
        return self._members

    def add_book(self, book: Book) -> None:
        if book.isbn in self._books:
            raise ValueError(f"Book with ISBN {book.isbn} already exists")
        self._books[book.isbn] = book

    def register_member(self, member: Member) -> None:
        if member.member_id in self._members:
            raise ValueError(
                f"Member with ID {member.member_id} already exists")
        self._members[member.member_id] = member

    def find_book_by_isbn(self, isbn: str) -> Book | None:
        return self._books.get(isbn)

    def find_member_by_id(self, member_id: str) -> Member | None:
        return self._members.get(member_id)

    def __str__(self) -> str:
        return f"Library '{self._name}' - {len(self._books)} books, {len(self._members)} members"

    def __repr__(self) -> str:
        return f"Library('{self._name}', {len(self._books)} books, {len(self._members)} members)"


class EBook(Book):
    def __init__(self, title: str, author: str, isbn: str, publication_year: int, is_available: bool = True, file_size: int = 0, format: str = "PDF") -> None:
        super().__init__(title, author, isbn, publication_year, is_available)
        self._file_size = file_size
        self._format = format

    @property
    def file_size(self) -> int:
        return self._file_size

    @property
    def format(self) -> str:
        return self._format

    def __str__(self) -> str:
        return f"{self._title} by {self._author} (EBook, {self._format}, {self._file_size}MB)"

    def __repr__(self) -> str:
        return f"EBook('{self._title}', '{self._author}', '{self._isbn}', {self._publication_year}, {self._is_available}, {self._file_size}, '{self._format}')"


class Student(Member):
    def __init__(self, name: str, member_id: str, borrowed_books: list[Book] | None = None, borrow_limit: int = 3) -> None:
        super().__init__(name, member_id, borrowed_books)
        self._borrow_limit = borrow_limit

    @property
    def borrow_limit(self) -> int:
        return self._borrow_limit

    def borrow_book(self, book: Book) -> None:
        if len(self._borrowed_books) >= self._borrow_limit:
            raise ValueError(
                f"Student has reached borrow limit of {self._borrow_limit} books")
        super().borrow_book(book)

    def __repr__(self) -> str:
        return f"Student('{self._name}', '{self._member_id}', {len(self._borrowed_books)}/{self._borrow_limit} books)"


class Faculty(Member):
    def __init__(self, name: str, member_id: str, borrowed_books: list[Book] | None = None, borrow_limit: int = 10) -> None:
        super().__init__(name, member_id, borrowed_books)
        self._borrow_limit = borrow_limit

    @property
    def borrow_limit(self) -> int:
        return self._borrow_limit

    def borrow_book(self, book: Book) -> None:
        if len(self._borrowed_books) >= self._borrow_limit:
            raise ValueError(
                f"Faculty has reached borrow limit of {self._borrow_limit} books")
        super().borrow_book(book)

    def __repr__(self) -> str:
        return f"Faculty('{self._name}', '{self._member_id}', {len(self._borrowed_books)}/{self._borrow_limit} books)"


if __name__ == "__main__":
    # Create library
    library = Library("City Library")

    # Create books
    book1 = Book("The Great Gatsby", "F. Scott Fitzgerald",
                 "978-0743273565", 1925)
    book2 = Book("To Kill a Mockingbird", "Harper Lee", "978-0061120084", 1960)
    ebook1 = EBook("Clean Code", "Robert Martin",
                   "978-0132350884", 2008, file_size=5, format="PDF")

    # Add books to library
    library.add_book(book1)
    library.add_book(book2)
    library.add_book(ebook1)

    # Create members
    student = Student("Alice Johnson", "S001", borrow_limit=2)
    faculty = Faculty("Dr. Smith", "F001", borrow_limit=5)

    # Register members
    library.register_member(student)
    library.register_member(faculty)

    # Test borrowing
    print(f"\n--- Testing Borrowing ---")
    print(f"Library: {library}")
    print(f"Book1 available: {book1.is_available}")

    student.borrow_book(book1)
    print(f"Student borrowed book1: {book1.is_available}")
    print(f"Student's books: {[str(b) for b in student.borrowed_books]}")

    # Test borrowing limits
    try:
        student.borrow_book(book2)
        student.borrow_book(ebook1)  # Should fail - limit reached
    except ValueError as e:
        print(f"Error (expected): {e}")

    # Test faculty borrowing
    faculty.borrow_book(book2)
    print(f"Faculty borrowed book2: {book2.is_available}")

    # Test returning
    print(f"\n--- Testing Returns ---")
    student.return_book(book1)
    print(f"Student returned book1: {book1.is_available}")

    # Test error cases
    try:
        student.return_book(book1)  # Should fail - not borrowed
    except ValueError as e:
        print(f"Error (expected): {e}")

    try:
        student.borrow_book(book2)  # Should fail - not available
    except ValueError as e:
        print(f"Error (expected): {e}")

    # Test finding
    print(f"\n--- Testing Find Operations ---")
    found_book = library.find_book_by_isbn("978-0743273565")
    print(f"Found book: {found_book}")

    found_member = library.find_member_by_id("S001")
    print(f"Found member: {found_member}")

    print(f"\n--- Final State ---")
    print(f"Library: {library}")
    print(f"Student: {repr(student)}")
    print(f"Faculty: {repr(faculty)}")
    print(f"EBook: {repr(ebook1)}")
