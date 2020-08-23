from django.http import HttpResponse
from django.conf.urls import url
from django.urls import path

from . import models

import json
from random import choice as random
from faker import Faker
fake = Faker()

equipment = ['table', 'chair', 'seat', 'stethescope', 'ventillator', 'mri', 'hammer', 'screwdriver', 'drill']

def populate(request):
    p = models.Person.objects.create(uid=fake.random_int(1000, 9999))
    p.notes.add(models.Note.objects.create(info=fake.sentence()))
    p.notes.add(models.Note.objects.create(info=fake.sentence()))
    p.notes.add(models.Note.objects.create(info=fake.sentence()))
    models.Flag.objects.create(diagnosis=fake.domain_name(), patient=p)

    i = models.Item.objects.create(name=random(equipment), description=fake.sentence(), location=fake.address(), status=fake.sentence())
    i.notes.add(models.Note.objects.create(info=fake.sentence()))
    
    m = models.Move.objects.create(
        start_time=fake.past_datetime(), 
        end_time=fake.past_datetime(), 
        start_place=fake.address(), 
        end_place=fake.address(), 
        item=i
    )
    m.notes.add(models.Note.objects.create(info=fake.sentence()))
        
    u = models.Use.objects.create(
        start_time=fake.past_datetime(), 
        end_time=fake.past_datetime(), 
        location=fake.address(),
        item=i
    )
    u.people.add(p)
    u.notes.add(models.Note.objects.create(info=fake.sentence()))

    b = models.Break.objects.create(
        start_time=fake.past_datetime(),
        end_time=fake.past_datetime(),
        item=i
    )
    b.notes.add(models.Note.objects.create(info=fake.sentence()))
    return HttpResponse("done")

def get_item(request, iid):
    i = models.Item.objects.get(id=iid)
    item = json.dumps(i.dict())
    return HttpResponse(item)

def get_item_notes(request, iid):
    item = models.Item.objects.get(id=iid)
    notes = json.dumps([n.dict() for n in item.notes.all()])
    return HttpResponse(notes)

def get_item_history(request, iid):
    item = models.Item.objects.get(id=iid)
    return HttpResponse(iid + "history")

def get_person(request, uid):
    p = models.Person.objects.get(id=uid)
    person = json.dumps(p.dict())
    return HttpResponse(person)

def get_person_notes(request, uid):
    person = models.Person.objects.get(id=uid)
    notes = json.dumps([n.dict() for n in person.notes.all()])
    return HttpResponse(notes)

def get_person_flags(request, uid):
    person = models.Person.objects.get(id=uid)
    flags = models.Flag.objects.filter(patient=person)
    flag_list = json.dumps([f.dict() for f in flags])
    return HttpResponse(flag_list)

def index(request):
    return HttpResponse("API page")

urlpatterns = [
    path('populate', populate),
    path('item/<iid>', get_item),
    path('item/<iid>/notes', get_item_notes),
    path('item/<iid>/history', get_item_history),
    path('person/<uid>', get_person),
    path('person/<uid>/notes', get_person_notes),
    path('person/<uid>/flags', get_person_flags),
    url('', index),
]
