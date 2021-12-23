import sqlite3
import re
import datetime
from backend import (to_datetime, to_string, parse_timedelta, to_timedelta,
                     check_date_format, auto_transfer)


class SQL():
    
    def __init__(self, filename):
        
        self.conn = sqlite3.connect(filename)
        self.cursor = self.conn.cursor()
        sql = '''CREATE TABLE IF NOT EXISTS main
        (id integer PRIMARY KEY AUTOINCREMENT,
        title text NOT NULL,
        note text,
        start_date text,
        due_date text,
        tag text)'''

        self.cursor.execute(sql)
        self.conn.commit()


        sql = '''CREATE TABLE IF NOT EXISTS statistics
        (id integer PRIMARY KEY AUTOINCREMENT,
        creation_date text,
        first_deadline_date text,
        last_editing_date text,
        closing_date text,
        changed_content_times integer,
        changed_deadline_times integer,
        closed_flag integer NOT NULL)'''

        self.cursor.execute(sql)
        self.conn.commit()


        sql = '''CREATE TABLE IF NOT EXISTS total
        (id integer,
        total_days_before_start_date integer,
        total_time_before_closed_deadline integer,
        total_content_changes integer,
        total_deadline_changes integer,
        total_deadline_difference integer,
        total_closed integer,
        total_deleted integer,
        total_opened integer)
        '''

        self.cursor.execute(sql)
        self.conn.commit()

        s = parse_timedelta(datetime.timedelta(seconds=0))
        
        sql = '''INSERT INTO total(id,
        total_days_before_start_date,
        total_time_before_closed_deadline,
        total_content_changes,
        total_deadline_changes,
        total_deadline_difference,
        total_closed,
        total_deleted,
        total_opened)
        VALUES(1,?,?,0,0,?,0,0,0)'''

        self.cursor.execute(sql, (s, s, s))
        self.conn.commit()



    def get_note(self, ID):
        """Get the note.

        Key arguments:
        ID - the identificator of the note.
        """
        sql = '''SELECT * FROM main WHERE id = ?'''
        
        return self.cursor.execute(sql, (ID,)).fetchall()[0]
        

    def add_note(self,
                 title = 'Untitled',
                 text = '',
                 start_date = '',
                 due_date = '',
                 tag = ''):
        """Takes the note from input and inserts it to the database.

        Key arguments:
        title - the title of the note
        text - the text of the note
        start_date - the start date of the note
        due_date - the due date of the note
        tag - tag of the note
        """

        
        start_date = check_date_format(start_date)
        due_date = check_date_format(due_date)
        
        sql = '''INSERT INTO main(title, note, start_date, due_date, tag)
        VALUES (?,?,?,?,?)'''
        
        self.cursor.execute(sql, (title, text, start_date, due_date, tag))
        self.conn.commit()


        sql = '''INSERT INTO statistics(creation_date, first_deadline_date,
        last_editing_date, closing_date, changed_content_times,
        changed_deadline_times, closed_flag) VALUES (?,?,?,?,?,?,?)'''
        
        self.cursor.execute(sql, (to_string(datetime.datetime.now()), due_date,
                                  to_string(datetime.datetime.now()), "",
                                  0, 0, 0))
        self.conn.commit()


        sql = '''SELECT * FROM total WHERE id = 1'''
        
        values_total = self.cursor.execute(sql).fetchall()[0]

        if start_date != "":
            datetime_before_start_date = to_datetime(start_date) - datetime.datetime.now()
            new_days_before_start_date = parse_timedelta(datetime_before_start_date + to_timedelta(values_total[1]))
        else:
            new_days_before_start_date = values_total[1]
            
        new_notes = values_total[8] + 1

        sql = '''UPDATE total
                 SET total_days_before_start_date = ?,
                     total_opened = ?
                 WHERE id = 1
                 '''
        self.cursor.execute(sql, (new_days_before_start_date, new_notes))
        self.conn.commit()


    def edit_note(self,
                  ID,
                  new_title = 'Untitled',
                  new_text = '',
                  new_start_date = '',
                  new_due_date = '',
                  new_tag = '',
                  edited = 0,
                  deadline_edited = 0):
        
        """Updates the note.

        Key arguments:
        ID - the identificator of the note
        new_title - changed title
        new_text - changed text
        new_start_date - changed start date
        new_due_date - changed due date
        new_tag - changed tag

        Any argument except ID may stay the same.
        """

        new_start_date = check_date_format(new_start_date)
        new_due_date = check_date_format(new_due_date)
        
        sql = '''UPDATE main
                 SET title = ?,
                     note = ?,
                     start_date = ?,
                     due_date = ?,
                     tag = ?
                 WHERE id = ?'''
        
        self.cursor.execute(sql, (new_title, new_text, new_start_date,
                                  new_due_date, new_tag, ID))
        self.conn.commit()


        # Getting current data from statistics
        
        sql = '''SELECT * FROM statistics WHERE id = ?'''
        
        values_stat = self.cursor.execute(sql, (ID,)).fetchall()[0]

        sql = '''UPDATE statistics
                 SET last_editing_date = ?,
                     changed_content_times = ?,
                     changed_deadline_times = ?
                 WHERE id = ?'''
        
        changed_deadline = values_stat[6]
        
        if new_due_date != "":
            changed_deadline += deadline_edited
            
        self.cursor.execute(sql, (to_string(datetime.datetime.now()),
                                  values_stat[5] + edited, changed_deadline,
                                  ID))
        self.conn.commit()


        # Getting current data from total
        
        sql = '''SELECT * FROM total WHERE id = 1'''
        
        values_total = self.cursor.execute(sql).fetchall()[0]

        sql = '''UPDATE total
                 SET total_content_changes = ?,
                     total_deadline_changes = ?
                 WHERE id = 1'''

        changed_deadline = values_total[4]
        
        if new_due_date != "":
            changed_deadline += deadline_edited
            
        self.cursor.execute(sql, (values_total[3] + edited,
                                  changed_deadline))
            


    def delete_note(self, ID):
        """Deletes the note.

        Key arguments:
        ID - the key argument of the note at the database.
        """

        sql = '''DELETE FROM main WHERE id = ?'''
        self.cursor.execute(sql, (ID,))
        self.conn.commit()

        sql = '''DELETE FROM statistics WHERE id = ?'''
        self.cursor.execute(sql, (ID,))
        self.conn.commit()

        sql = '''SELECT * FROM total WHERE id = 1'''
        values_total = self.cursor.execute(sql).fetchall()[0]

        sql = '''UPDATE total
                 SET total_deleted = ?,
                     total_opened = ?
                 WHERE id = 1'''
        self.cursor.execute(sql, (values_total[7] + 1, values_total[8] - 1))


    def close_note(self, ID):
        """Closes the task/the note.

        Key arguments:
        ID - the key argument of the note at the database.
        """

        sql = '''SELECT * FROM main WHERE id = ?'''
        values_main = self.cursor.execute(sql, (ID,)).fetchall()[0]
        
        sql = '''DELETE FROM main WHERE id = ?'''
        self.cursor.execute(sql, (ID,))
        self.conn.commit()

        sql = '''UPDATE statistics
                 SET closing_date = ?,
                     closed_flag = ?
                 WHERE id = ?'''
        
        self.cursor.execute(sql, (to_string(datetime.datetime.now()),
                                  1, ID))
        self.conn.commit()

        sql = '''SELECT * FROM statistics WHERE id = ?'''
        values_stat = self.cursor.execute(sql, (ID,)).fetchall()[0]

        sql = '''SELECT * FROM total WHERE id = 1'''
        values_total = self.cursor.execute(sql).fetchall()[0]

        sql = '''UPDATE total
                 SET total_time_before_closed_deadline = ?,
                     total_deadline_difference = ?,
                     total_closed = ?,
                     total_opened = ?
                 WHERE id = 1'''

        if values_main[4] != "":
            time_to_deadline = to_datetime(values_main[4]) - datetime.datetime.now()
        else:
            time_to_deadline = datetime.timedelta(seconds=0)
            
        total_time_to_deadline = parse_timedelta(to_timedelta(values_total[2]) + time_to_deadline)

    
        if values_main[4] != "" and values_stat[2] != "":
            deadline_diff = to_datetime(values_main[4]) - to_datetime(values_stat[2])
        else:
            deadline_diff = datetime.timedelta(seconds=0)
            
        total_deadline_diff = parse_timedelta(deadline_diff + to_timedelta(values_total[5]))

        self.cursor.execute(sql, (total_time_to_deadline,
                                  total_deadline_diff,
                                  values_total[6] + 1,
                                  values_total[8] - 1))
        self.conn.commit()
    

    def show_notes(self):
        """Shows all notes from the database."""
        sql = '''SELECT id, title FROM main'''
        return self.cursor.execute(sql).fetchall()


    def get_tags(self):
        "Returns list of all tags."
        sql = '''SELECT DISTINCT tag FROM main'''
        cur = self.cursor.execute(sql).fetchall()
        ans = []
        for elem in cur:
            ans.append(elem[0])
        return ans

        
    def select_notes_by_tag(self, tag):
        if tag == None:
            return self.show_notes()
        else:
            """Selects notes having a particular tag."""
            sql = '''SELECT * FROM main WHERE tag = ?'''
            return self.cursor.execute(sql, (tag,)).fetchall()


    def print_all(self):
        """Shows all data."""
        sql = '''SELECT * FROM main'''
        print(self.cursor.execute(sql).fetchall())
        sql = '''SELECT * FROM statistics'''
        print(self.cursor.execute(sql).fetchall())
        sql = '''SELECT * FROM total'''
        print(self.cursor.execute(sql).fetchall()[0])
        print()


    def get_total(self):
        """Returns summary statistics as a list"""

        sql = '''SELECT * FROM total WHERE id = 1'''
        values_total = self.cursor.execute(sql).fetchall()[0]

        res = []

        opened = values_total[8]
        closed = values_total[6]
        deleted = values_total[7]
        allTasks = opened + closed + deleted

        total_days_before_start_date = values_total[1]
        total_time_before_closed_deadline = values_total[2]
        total_content_changes = values_total[3]
        total_deadline_changes = values_total[4]
        total_deadline_difference = values_total[5]

        res.append(opened)
        res.append(closed)
        res.append(deleted)
        res.append(allTasks)

        if allTasks != 0:
            plan_before = parse_timedelta(to_timedelta(total_days_before_start_date) / allTasks)
        else:
            plan_before = '-'

        if closed + opened != 0:
            content_changes = round(total_content_changes / (closed + opened), 2)
            deadline_changes = round(total_deadline_changes / (closed + opened), 2)
        else:
            content_changes = deadline_changes = '-'

        if closed != 0:
            time_left = parse_timedelta(to_timedelta(total_time_before_closed_deadline) / closed)
            deadline_postponed = parse_timedelta(to_timedelta(total_deadline_difference) / closed)
        else:
            time_left = deadline_postponed = '-'

        res.append(content_changes)
        res.append(deadline_changes)
        res.append(plan_before)
        res.append(time_left)
        res.append(deadline_postponed)

        return res
        

        
