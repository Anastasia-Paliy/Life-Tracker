import json

def add_note(notes):
    text = input()
    note = dict(text = text)
    notes.append(note)
    with open("notes.json", 'w') as file:
        json.dump(notes, file, indent = 4)

def show(notes):
    for note in notes:
        my_notes = note.values()
        for item in my_notes:
            print(item)
            print('********************************')


try:
    with open("notes.json", 'r') as file:
        notes = json.load(file)
except FileNotFoundError:
    notes = []
    
for i in range(3):
    add_note(notes)
show(notes)
