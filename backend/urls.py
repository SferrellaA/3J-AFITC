from django.http import HttpResponse
from django.urls import path

from . import models

from datetime import datetime
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

def jerror(text):
    return json.dumps({"error": text})

def get_item_count(request):
    return HttpResponse(models.Item.objects.count())

def new_item(request):
    name = request.GET.get("name")
    if name == "" or name == None:
        return HttpResponse(jerror("new items need a name"))
    description = request.GET.get("description")
    if description == "" or description == None:
        return HttpResponse(jerror("new items need a description"))
    location = request.GET.get("location")
    if location == "" or location == None:
        location = "unknown"
    status = request.GET.get("")
    if status == "" or status == None:
        status = "unknown"
    item = models.Item.objects.create(
        name=name,
        description=description,
        location=location,
        status=status,
    )
    return HttpResponse(json.dumps(item.dict()))

def item_add_note(request, iid):
    try:
        item = models.Item.objects.get(id=iid)
    except:
        return HttpResponse(jerror("invalid item"))
    text = request.GET.get("note")
    if text == "" or text == None:
        return HttpResponse(jerror("no note listed"))
    item.notes.add(models.Note.objects.create(info=text))
    item.save()
    return HttpResponse(json.dumps([n.dict() for n in item.notes.all()]))

def item_change_status(request, iid):
    try:
        item = models.Item.objects.get(id=iid)
    except:
        return HttpResponse(jerror("invalid item"))
    status = request.GET.get("status")
    if status == "" or status == None:
        return HttpResponse(jerror("no status listed"))
    item.status = status
    item.save()
    return HttpResponse(json.dumps(item.dict()))

def item_start_move(request, iid):
    try:
        item = models.Item.objects.get(id=iid)
    except:
        return HttpResponse(jerror("invalid item"))
    start_place = request.GET.get("start_place")
    if start_place == "" or start_place == None:
        return HttpResponse(jerror("invalid start place"))
    move = models.Move.objects.create(
        start_time = datetime.now(),
        start_place = start_place,
        end_time = datetime.now(),
        item = item
    )
    note = request.GET.get("note")
    if note != "" and note != None:
        move.notes.add(models.Note.objects.create(info=note))
    move.save()
    return HttpResponse(json.dumps(move.dict()))

def item_end_move(request, iid):
    try:
        item = models.Item.objects.get(id=iid)
    except:
        return HttpResponse(jerror("invalid item"))
    try:
        moves = models.Move.objects.filter(item=item)
    except:
        return HttpResponse(jerror("no move history for item"))
    move = moves[len(moves)-1]
    end_place = request.GET.get("end_place")
    if end_place == "" or end_place == None:
        return HttpResponse(jerror("invalid end place"))
    move.end_place = end_place
    move.end_time = datetime.now()
    note = request.GET.get("note")
    if note != "" and note != None:
        move.notes.add(models.Note.objects.create(info=note))
    move.save()
    return HttpResponse(json.dumps(move.dict()))
    
def item_start_use(request, iid):
    try:
        item = models.Item.objects.get(id=iid)
    except:
        return HttpResponse(jerror("invalid item"))
    location = request.GET.get("location")
    if location == "" or location == None:
        return HttpResponse(jerror("invalid location"))
    use = models.Use.objects.create(
        start_time = datetime.now(),
        end_time= datetime.now(),
        location = location,
        item = item
    )
    note = request.GET.get("note")
    if note != "" and note != None:
        use.notes.add(models.Note.objects.create(info=note))
    use.save()
    return HttpResponse(json.dumps(use.dict()))

def item_end_use(request, iid):
    try:
        item = models.Item.objects.get(id=iid)
    except:
        return HttpResponse(jerror("invalid item"))
    try:
        use = models.Use.objects.filter(item=item)
    except:
        return HttpResponse(jerror("no use history for item"))
    use = use[len(use)-1]
    use.end_time = datetime.now()
    #people = request.GET.getlist("people")
    note = request.GET.get("note")
    if note != "" and note != None:
        use.notes.add(models.Note.objects.create(info=note))
    use.save()
    return HttpResponse(json.dumps(use.dict()))
    

def item_start_break(request, iid):
    try:
        item = models.Item.objects.get(id=iid)
    except:
        return HttpResponse(jerror("invalid item"))
    breakage = models.Break.objects.create(
        start_time = datetime.now(),
        end_time = datetime.now(),
        item = item
    )
    note = request.GET.get("note")
    if note != "" and note != None:
        breakage.notes.add(models.Note.objects.create(info=note))
        breakage.save()
    return HttpResponse(json.dumps(breakage.dict()))    

def item_end_break(request, iid):
    try:
        item = models.Item.objects.get(id=iid)
    except:
        return HttpResponse(jerror("invalid item"))
    try:
        breakage = models.Break.objects.filter(item=item)
    except:
        return HttpResponse(jerror("no break history for item"))
    breakage = breakage[len(breakage)-1]
    breakage.end_time = datetime.now()
    note = request.GET.get("note")
    if note != "" and note != None:
        breakage.notes.add(models.Note.objects.create(info=note))
    breakage.save()
    return HttpResponse(json.dumps(breakage.dict()))    

def get_item(request, iid):
    try:
        item = models.Item.objects.get(id=iid)
    except:
        return HttpResponse(jerror("invalid item"))
    breakeage = json.dumps(item.dict())
    if note != "" and note != None:
        breakage.notes.add(models.Note.objects.create(info=note))
    breakage.save()
    return HttpResponse(item)

def get_item_notes(request, iid):
    try:
        item = models.Item.objects.get(id=iid)
    except:
        return HttpResponse(jerror("invalid item"))
    notes = json.dumps([n.dict() for n in item.notes.all()])
    return HttpResponse(notes)

def get_item_history(request, iid):
    try:
        item = models.Item.objects.get(id=iid)
    except:
        return HttpResponse(jerror("invalid item"))
    h = []
    h += [m.dict() for m in models.Move.objects.filter(item=item)]
    h += [u.dict() for u in models.Use.objects.filter(item=item)]
    h += [b.dict() for b in models.Break.objects.filter(item=item)]
    history = json.dumps(h)
    return HttpResponse(history)

def get_item_all(request, iid):
    try:
        i = models.Item.objects.get(id=iid)
    except:
        return HttpResponse(jerror("invalid item"))
    item = i.dict()
    item['notes'] = [n.dict() for n in i.notes.all()]
    item['history'] = []
    item['history'] += [m.dict() for m in models.Move.objects.filter(item=i)]
    item['history'] += [u.dict() for u in models.Use.objects.filter(item=i)]
    item['history'] += [b.dict() for b in models.Break.objects.filter(item=i)]
    item = json.dumps(item)
    return HttpResponse(item)

def get_person_count(request):
    return HttpResponse(models.Person.objects.count())

def new_person(request):
    uuid = request.GET.get("uuid")
    if uuid == "" or uuid == None:
        return HttpResponse(jerror("a uuid is required"))
    try:
        person = models.Person.objects.create(uid = uuid)
    except:
        return HttpResponse(jerror("unique uuid required"))
    note = request.GET.get("note")
    if note != "" and note != None:
        person.notes.add(models.Note.objects.create(info=note))
        person.save()
    return HttpResponse(json.dumps(person.dict()))    

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

def person_new_flag(request, uid):
    try:
        person = models.Person.objects.get(id=uid)
    except:
        return HttpResponse(jerror("invalid person"))
    diagnosis = request.GET.get("diagnosis")
    if diagnosis == "" or diagnosis == None:
        return HttpResponse(jerror("no diagnosis"))
    flag = models.Flag.objects.create(
        diagnosis = diagnosis,
        patient = person,
        info = request.GET.get("info")
    )
    note = request.GET.get("note")
    if note != "" and note != None:
        person.notes.add(models.Note.objects.create(info=note))
        person.save()
    return HttpResponse(json.dumps(flag.dict()))    

def get_person_all(request, uid):
    p = models.Person.objects.get(id=uid)
    person = p.dict()
    person['notes'] = [n.dict() for n in p.notes.all()]
    person['flags'] = [f.dict() for f in models.Flag.objects.filter(patient=p)]
    person = json.dumps(person)
    return HttpResponse(person)

def index(request):
    return HttpResponse("API page")

urlpatterns = [
    path('populate', populate),
    path('item', get_item_count),
    path('item/new', new_item),
    path('item/<int:iid>', get_item),
    path('item/<int:iid>/notes', get_item_notes),
    path('item/<int:iid>/history', get_item_history),
    path('item/<int:iid>/history/start_move', item_start_move),
    path('item/<int:iid>/history/end_move', item_end_move),
    path('item/<int:iid>/history/start_use', item_start_use),
    path('item/<int:iid>/history/end_use', item_end_use),
    path('item/<int:iid>/history/start_break', item_start_break),
    path('item/<int:iid>/history/end_break', item_end_break),
    path('item/<int:iid>/all', get_item_all),
    path('item/<int:iid>/add_note', item_add_note),
    path('item/<int:iid>/change_status', item_change_status),
    path('person', get_person_count),
    path('person/new', new_person),
    path('person/<int:uid>', get_person),
    path('person/<int:uid>/notes', get_person_notes),
    path('person/<int:uid>/flags', get_person_flags),
    path('person/<int:uid>/flags/new', person_new_flag),
    path('person/<int:uid>/all', get_person_all),
    path('', index),
]
