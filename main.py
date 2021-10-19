import json, re, sqlite3

def add_note(notes):
    """Takes the note from input and adds it to the program local copy, then dumps it into JSON file.

    Key argument: notes (default [])
    """
    text = input()
    note = dict(text = text)
    notes.append(note)
    with open("notes.json", 'w') as file:
        json.dump(notes, file, indent = 4)

def add_note_sql():
    """Takes the note from input and inserts it to the database."""
    text = input()
    sql = '''INSERT INTO main(note) VALUES (?)'''
    cursor.execute(sql, (text,))
    conn.commit()

def show(notes):
    """Prints all notes by taking their values from the program local copy.

    Key argument: notes (default [])
    """
    for note in notes:
        my_notes = note.values()
        for item in my_notes:
            item = auto_transfer(item)
            print(item)
            print('********************************')

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


"""Loads notes to the program local copy from JSON file."""
'''
try:
    with open("notes.json", 'r') as file:
        notes = json.load(file)
except FileNotFoundError:
    notes = []
'''


conn = sqlite3.connect('notes.db')
cursor = conn.cursor()
sql = '''CREATE TABLE IF NOT EXISTS main
(note text)'''
cursor.execute(sql)

"""Test of adding k notes and showing all notes"""
k = 2
for i in range(k):
    add_note_sql()
show_notes_sql()
cursor.close()
conn.close()
