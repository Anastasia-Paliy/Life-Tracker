import sqlite3

def add_note_sql():
    """Takes the note from input and inserts it to the database."""
    text = input()
    sql = '''INSERT INTO main(note) VALUES (?)'''
    cursor.execute(sql, (text,))
    conn.commit()


def delete_note_sql(note_id):
    """Deletes the note.

    Key arguments:
    note_id - the key argument of the note at the database.
    """

    sql = '''DELETE FROM main WHERE note=?'''
    cursor.execute(sql, (note_id,))
    conn.commit()

<<<<<<< HEAD

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
(note text)'''
cursor.execute(sql)
=======
def edit_note(notes, prev_text, new_text):
    
    new_note = dict(text = new_text)
    prev_note = dict(text = prev_text)
    notes.remove(prev_note)
    notes.append(new_note)
>>>>>>> 4847452f1121230dc478af9537287f29279fb14c

"""Test of adding k notes and showing all notes"""
k = 3
for i in range(k):
    add_note_sql()
delete_note_sql("note 1")
show_notes_sql()
cursor.close()
conn.close()

