import json

def add_note(notes, text):
    
    note = dict(text = text)
    notes.append(note)
    
    with open("notes.json", 'w') as file:
        json.dump(notes, file, indent = 4)

    return notes


def edit_note(notes, prev_text, new_text):
    
    new_note = dict(text = new_text)
    prev_note = dict(text = prev_text)
    notes.remove(prev_note)
    notes.append(new_note)

    with open("notes.json", 'w') as file:
        json.dump(notes, file, indent = 4)
        
    return notes

