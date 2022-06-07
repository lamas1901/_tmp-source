from django.utils.text import slugify
from django.core.files.uploadedfile import UploadedFile
from django.contrib.auth.models import User

from pets.models import FrequentlyAskedQuestion, Pet, PetType

from orjson import loads
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

with open(BASE_DIR/'pets/source.json') as f:
	pets = loads(f.read())
with open(BASE_DIR/'faq/source.json') as f:
	faq = loads(f.read())

bird_pet_type = PetType.objects.get(slug='kus')
for pet in pets:
	_pet = Pet(
		name = pet['name'],
		slug = slugify(pet['name']),
		owner = User.objects.first(),
		price = 0,
		animal_type = bird_pet_type,
		age = pet['age'],
		sex = 'male' if 'Erkek' in pet['sex'] else 'female',
		breed= pet['breed'],
		city = slugify(pet['city']),
		description = pet['content'],
		special_phone = pet['owner_phone'],
		special_waphone = pet['owner_phone'],
		special_owner = pet['owner_name']
	)
	_pet.save()
	_pet.photo.save(
		slugify(pet['name'])+str(_pet.id)+'.jpg',
		UploadedFile(
			file=open(BASE_DIR/f'pets/images/{slugify(pet["name"])}.jpg','rb')
		)
	)
	_pet.save()

for quesiton in faq:
	_question = FrequentlyAskedQuestion(
		title=quesiton[0],
		content=quesiton[1]
	)
	_question.save()