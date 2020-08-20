from datetime import datetime

# Soemthing like "covid positive"
class Flag:
    def __init__(self, name, status, info):
        self.name = name # ex covid
        self.status = status # ex positive
        self.info = info # doctor's note
        
# Only uid for anomynity, reference to other systems
class Person:
    def __init__(self, uid):
        self.uid = uid
        self.flag = {}
    def diagnose(self, name, status, info):
        self.flag[datetime.now()] = Flag(name, status, info)

# Representing the movement of an item from one place to another
class Move:
    def end_move(self, final_location):
        self.end_time = datetime.now()
        self.end_place = final_location
    def __init__ (start_place, **kwargs):
        self.start_place = start_place
        if "start_time" in kwargs:
            self.start_time = kwargs.get("start_time", None)
        else:
            self.start_time = datetime.now()
        if "end_time" in kwargs:
            self.end_time = kwargs.get("end_time", None)
        if "end_place" in kwargs:
            self.end_place = kwargs.get("end_place", None)

# Range of time item is in use, who came into contact with it
class Use:
    def __init__(self, location, **kwargs):
        self.location = location
        if "start_time" in kwargs:
            self.start_time = kwargs.get("start_time", None)
        else:
            self.start_time = datetime.now()
        if "end_time" in kwargs:
            self.end_time = kwargs.get("end_time", None)
        if "people" in kwargs:
            self.people = kwargs.get("people", None)
        else:
            self.people = {}
    def end_use(self):
        self.end_time = datetime.now()
    def add_person(self, uid):
        self.people[datetime.now()] = uid

# Representing a breakage of any kind from start to finish
class Break:
    def __init__(self, note, **kwargs):
        if "start_time" in kwargs:
            self.start_time = kwargs.get("start_time", None)
        else:
            self.start_time = datetime.now()
        if "end_time" in kwargs:
            self.end_time = kwargs.get("end_time", None)
        if "info" in kwargs:
            self.info = kwargs.get("info", None)
        else:
            self.info = {}
            self.info[self.start_time] = note
    def add_info(self, info):
        self.info[datetime.now()] = info
    def fix_break(self):
        self.end_time = datetime.now()

# A piece of hospital equipment (a ventilator or stethescope)
class Item:
    def __init__(self, name, description, **kwargs):
        self.name = name
        self.description = description
        self.location = "square.oath.melt" # using what3words
        if "location" in kwargs:
            self.location = kwargs.get("location", None)
        self.history = []
        if "history" in kwargs:
            self.history = kwargs.get("history", None)
        self.notes = {}
        if "notes" in kwargs:
            self.notes = kwargs.get("notes", None)
        self.status = {datetime.now(), "unboxed"}
        if "status" in kwargs:
            self.status = kwargs.get("status", None)
    def add_note(self, note):
        self.notes[datetime.now()] = note
    def start_move(self):
        self.history.append(Move(self.location))
        self.location = "in transit"    
    def end_move(self, final_location)
        self.history[-1].end_move(final_location)
        self.location = final_location
    def start_break(self, note):
        self.history.append(Break(note))
    def end_break(self):
        self.history[-1].fix_break()
    def change_status(self, status):
        self.status[datetime.now()] = status
