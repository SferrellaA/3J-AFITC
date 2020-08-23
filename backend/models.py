from django.db import models

# A note about a thing
class Note(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    info = models.TextField()
    def dict(self):
        return {
            'time': str(self.time),
            'info': self.info
        }

# A piece of hospital equipment (a ventilator or stethescope)
class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    notes = models.ManyToManyField(Note)
    status = models.CharField(max_length=100)
    def dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'location': self.location,
            'status': self.status
        }

# Only uid for anomynity, refrence to other systems
class Person(models.Model):
    uid = models.IntegerField(unique=True)
    notes = models.ManyToManyField(Note)
    def dict(self):
        return {
            'uid': self.uid
        }

# Something like "covid positive"
class Flag(Note):
    diagnosis = models.CharField(max_length=100)
    patient = models.ForeignKey(Person, on_delete=models.CASCADE)
    def dict(self):
        return {
            'flag': self.diagnosis,
            'uid': self.patient.uid
        }

# Common fields in each type of history item
class HistoryItem(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    notes = models.ManyToManyField(Note)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    class Meta:
        abstract = True

# Representing the movement of an item from one place to another
class Move(HistoryItem):
    start_place = models.CharField(max_length=100)
    end_place = models.CharField(max_length=100)
    def dict(self):
        return {
            'start_time': self.start_time,
            'end_time': self.end_time,
            'start_place': self.start_place,
            'end_place': self.end_place
        }

# Range of time item is in use, who came into contact with it
class Use(HistoryItem):
    location = models.CharField(max_length=100)
    people = models.ManyToManyField(Person)
    def dict(self):
        return {
            'start_time': self.start_time,
            'end_time': self.end_time,
            'location': self.location,
            'people': self.people
        }

# Representing a breakage of any kind from start to finish
class Break(HistoryItem):
    pass
    def dict(self):
        return {
            'start_time': self.start_time,
            'end_time': self.end_time
        }

