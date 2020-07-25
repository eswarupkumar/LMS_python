import sqlite3

connect_lib = sqlite3.connect('library.db')
lib = connect_lib.cursor()
lib.execute('CREATE TABLE IF NOT EXISTS recordtolist(sicno INTEGER,bookname TEXT)')

#ISSUE BOOK

def issue_func():
    sicno = int(input('\nEnter SIC no.: '))
    book_name = input('Enter book name: ')
    lib.execute('SELECT bookname FROM recordtolist WHERE sicno = (?)',(sicno,))
    compare_bookname_tup = lib.fetchone()
    try:
        compare_bookname = compare_bookname_tup[0]
    except:
        compare_bookname = None
    if compare_bookname != book_name:
        lib.execute('SELECT no_of_book FROM booktolist WHERE name = (?)',(book_name,))
        modify_no_books_tup = lib.fetchone()
        try:
            modify_no_books = modify_no_books_tup[0]
        except:
            modify_no_books = None
        
        lib.execute('SELECT count FROM studenttolist WHERE sicno = (?)',(sicno,))        
        count_tup = lib.fetchone()
        try:
            count = count_tup[0]
        except:
            count = None
        print('\nNo of copies of the book available are:: ',modify_no_books)
        print('The student has issued total ',count,' books before')
        if count < 2 and modify_no_books != None and modify_no_books != 0 and count != None:
            count += 1
            modify_no_books -= 1
            lib.execute('INSERT INTO recordtolist VALUES(?,?)',(sicno,book_name))
            connect_lib.commit()
            lib.execute('UPDATE studenttolist SET count = (?) WHERE sicno = (?)',(count,sicno))
            connect_lib.commit()
            lib.execute('UPDATE booktolist SET no_of_book = (?) WHERE name = (?)',(modify_no_books,book_name))
            connect_lib.commit()
            print('\nThe book has been succesfully issued')
        elif modify_no_books == None or count == None:
            print('\nAn error occured because SIC no or book name do not exist. Please try again')
        elif modify_no_books == 0:
            print('\nNo more copies of the book are left')
        elif count >= 2:
            print('\nThe student has issued more than 2 books. Cannot issue more')
    else:
        print('You cannot issue same book more than once')

#RETURN BOOK

def return_func():
    sicno = int(input('\nEnter SIC no.: '))
    book_name = input('Enter book name: ')
    lib.execute('SELECT no_of_book FROM booktolist WHERE name = (?)',(book_name,))
    modify_no_books_tup = lib.fetchone()
    try:
        modify_no_books = modify_no_books_tup[0]
    except:
        modify_no_books = None
    lib.execute('SELECT count FROM studenttolist WHERE sicno = (?)',(sicno,))
    count_tup = lib.fetchone()
    try:
        count = count_tup[0]
    except:
        count = None
    if count > 0 and count != None:
        count -= 1
        modify_no_books += 1
        lib.execute('DELETE FROM recordtolist WHERE bookname = (?) AND sicno = (?)',(book_name,sicno))
        connect_lib.commit()
        lib.execute('UPDATE studenttolist SET count = (?) WHERE sicno = (?)',(count,sicno))
        connect_lib.commit()
        lib.execute('UPDATE booktolist SET no_of_book = (?) WHERE name = (?)',(modify_no_books,book_name))
        connect_lib.commit()
        print('The book has been successfully return')
    else:
        print('He has not issued any book from library')

#LIST OF BOOKS ISSUED BY A STUDENT

def books_by_student(student_sicno):
    print('\nList of Books issued by the student are: ')
    lib.execute('SELECT bookname FROM recordtolist WHERE sicno = (?)',(student_sicno,))
    bookname_tup = lib.fetchall()
    for i in bookname_tup:
        print(i[0])

#LIST OF STUDENTS ISSUED A BOOK

def students_fora_book(book_name):
    print('\nList of students who took the book are: ')
    lib.execute('SELECT sicno FROM recordtolist WHERE bookname = (?)',(book_name,))
    sicno_tup = lib.fetchall()
    for i in sicno_tup:
        lib.execute('SELECT name FROM studenttolist WHERE sicno = (?)',(i[0],))
        store_name = lib.fetchone()
        print('\nName of the Student: ',store_name[0],'\nSIC no.: ',i[0])

#CHOICE IN LIBRARY

def choice():

    while True:
        print('\nWelcome to Librarian portal')
        choice = input('\nChoices:\n1. Issue a book\n2. Return a book\n3. List of books\n4. List of books issued by a student\n5. List of students who took a book\n6. Back\nEnter your choice: ')
        if choice == '1':
            issue_func()
        elif choice == '2':
            return_func()
        elif choice == '3':
            print('\nList of Books are: ')
            lib.execute('SELECT * FROM booktolist')
            for row in lib.fetchall():
                print('\nBook name: ',row[0],'\nAuthor name: ',row[1],'\nNo. of copies: ',row[3])
        elif choice == '4':
            sicno = int(input('Enter the SIC no.: '))
            books_by_student(sicno)
        elif choice == '5':
            bname = input('\nName of the book: ')
            students_fora_book(bname)
        elif choice == '6':
            print('Exited Library Module')
            break
        else:
            print('Invalid choice')

#choice()