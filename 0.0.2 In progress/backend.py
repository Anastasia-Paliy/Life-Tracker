import json

def add_note(notes, text):
    
    note = dict(text = text)
    notes.append(note)
    
    with open("notes.json", 'w') as file:
        json.dump(notes, file, indent = 4)

    return notes


def delete_note(notes, text):
    
    note = dict(text = text)
    notes.remove(note)

    with open("notes.json", 'w') as file:
        json.dump(notes, file, indent = 4)
        
    return notes


    
