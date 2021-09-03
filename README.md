# LibraryApp
##Library App for students using Python Tkinter and MySQL
-> Connected to localhost mysql server through mysql.connector package
-> Library database created in mysql

* Library app for students to explore, issue and return books.
* Library database contains 4 tables: students, section, issues, books. 
* When the app starts, the student has to login by providing userid and password. When the login button is clicked a query will be sent to the database which retrieves the password for the given userid. If the password retrieved from the database and the one provided by the student matches the main window opens else the password has to be entered again.
* In the main window student information will be displayed on the top and below it four buttons are available: explore, book issues, issue book, return book.
* When the explore button is clicked, a query is sent to the database which fetches all the rows from the books table and each row is displayed separately inside a frame.
* When the book issues button is clicked, a query is sent to the database which fetches rows from the issues table corresponding to the student id and it shows the books issued to the particular student id, issue date and the return date.
* When the issue book button is clicked, an entry asks the id of the book to be issued. When that entry is filled and submitted, a query is sent to the database which inserts the details of book issue in the issues table.
* When the return book button is clicked, an entry asks the id of the book to be returned. When that entry is filled and submitted, a query is sent to the database which deletes the row corresponding to the student id and the book id in the issues table.
