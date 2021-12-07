import sqlite3

def add_note_sql(title, text=None, start_date=None, due_date=None):
    """Takes the note from input and inserts it to the database.

    Key arguments:
    title - the title of the note
    text - the text of the note
    start_date - the start date of the note
    due_date - the due date of the note
    """
    sql = '''INSERT INTO main(title, note, start_date, due_date) VALUES (?,?,?,?)'''
    cursor.execute(sql, (title, text, start_date, due_date))
    conn.commit()


def delete_note_sql(ID):
    """Deletes the note.

    Key arguments:
    ID - the key argument of the note at the database.
    """

    sql = '''DELETE FROM main WHERE id=?'''
    cursor.execute(sql, (ID,))
    conn.commit()


def edit_note_sql(ID, new_title=None, new_text=None, new_start_date=None, new_due_date=None):
    """Updates the note.

    Key arguments:
    ID - the identificator of the note
    new_title - changed title
    new_text - changed text
    new_start_date - changed start date
    new_due_date - changed due date

    Any argument except ID may stay the same.
    """
    sql = '''UPDATE main
             SET title = ?,
                 note = ?,
                 start_date = ?,
                 due_date = ?
             WHERE id = ?'''
    cursor.execute(sql, (new_title, new_text, new_start_date, new_due_date, ID))
    conn.commit()
    

def show_notes_sql():
    """Shows all notes from the database."""
    sql = '''SELECT * FROM main'''
    print(cursor.execute(sql).fetchall())


def auto_transfer(string, length=20, rows=5):
    """Auto-transfers the string by spaces, underscores and by max length.
    
    Key arguments:
    string - the string for transferring
    length - maximal length of each row of the result (default 20)
    rows - maximal number of rows (default 5)
    """

    l = re.split(r'[_. ]+', string)
    cur_len = 0
    cur_transfer = 0
    cur_string = ""
    i = 0
    while cur_transfer + 1 < rows and i < len(l):
        # there is place left in the button

        while i < len(l) and cur_len + len(l[i]) < length:
            # current row is not full yet
            cur_len += len(l[i]) + 1
            cur_string = cur_string + l[i] + " "
            if i < len(l):
                # there are elements of string to add to the result
                i += 1

        if i >= len(l):
            break
        # current row will be full by adding the next element
        # consider several options
        if len(l[i]) > length or length - cur_len > 5:
            # option 1: the next element is too long even for the whole row
            # option 2: there are more than 5 symbols left

            # cut first length-cur_len elements from it, paste into the result
            # change current element of l to the remainder of it
            cur_part = l[i]
            cur_string = cur_string + cur_part[:length-cur_len] + "\n"
            cur_part = cur_part[length-cur_len:]
            l[i] = cur_part
        else:
            # option 3: there are less than 5 symbols left
            # transfer the element to the next row
            cur_string += "\n"

        cur_len = 0
        cur_transfer += 1

    return cur_string



conn = sqlite3.connect('notes.db')
cursor = conn.cursor()

sql = '''CREATE TABLE IF NOT EXISTS main
(id integer PRIMARY KEY AUTOINCREMENT, title text NOT NULL, note text, start_date text, due_date text)'''
cursor.execute(sql)


"""Test of adding notes and showing all notes"""
add_note_sql("how are you", "task 1", "20.07.2011")
add_note_sql("hello world")
show_notes_sql()
delete_note_sql(2)
show_notes_sql()
edit_note_sql(1, "changed title", "changed task")
show_notes_sql()
cursor.close()
conn.close()

