from django.shortcuts import render
from django.http import HttpResponse
import requests

#
# def index(request):
#     return HttpResponse("Hello World! Welcome to the poll index :D")

def index(request):
    response = requests.get('https://swapi.co/api/films')
    movies = response.json()
    return render(request, 'swinfo/home.html', {
        'movies': movies,
    })

def detail(request, movie_id):
    response = requests.get('https://swapi.co/api/films/')
    movies = response.json()['results']
    characters = {}
    starships = {}
    planets = {}
    for movie in movies:
        if movie['episode_id'] == movie_id:
            correct_movie = movie
    for character in correct_movie['characters']:
        second_response = requests.get(character)
        head, partition, tail = character.partition("people/")
        character_id = tail[:-1]
        characters.update({second_response.json()['name']:character_id})
    for starship in correct_movie['starships']:
        third_response = requests.get(starship)
        head, partition, tail = starship.partition("starships/")
        starships_id = tail[:-1]
        starships.update({third_response.json()['name']:starships_id})
    for planet in correct_movie['planets']:
        fourth_response = requests.get(planet)
        head, partition, tail = planet.partition("planets/")
        planet_id = tail[:-1]
        planets.update({fourth_response.json()['name']:planet_id})

    return render(request, 'swinfo/detail.html', {
        'movie': correct_movie,
        'characters':characters,
        'starships':starships,
        'planets':planets,
    })

def character_detail(request, character_id):
    response = requests.get('https://swapi.co/api/people/'+str(character_id))
    character = response.json()
    planet = character['homeworld']
    homeworld = requests.get(planet).json()
    films = []
    starships = {}

    for film in character['films']:
        movie = requests.get(film)
        films.append(movie.json())

    for starship in character['starships']:
        ships = requests.get(starship)
        head, partition, tail = starship.partition("starships/")
        starships_id = tail[:-1]
        starships.update({ships.json()['name']:starships_id})

    return render(request, 'swinfo/character_detail.html',{
        'character':character,
        'homeworld':homeworld,
        'films':films,
        'starships':starships,
    })

def ship_detail(request, starship_id):
    response = requests.get('https://swapi.co/api/starships/'+str(starship_id))
    ship = response.json()
    films = []
    pilots = {}

    for film in ship['films']:
        movie = requests.get(film)
        films.append(movie.json())

    for pilot in ship['pilots']:
        piloto = requests.get(pilot)
        head, partition, tail = pilot.partition("people/")
        piloto_id = tail[:-1]
        pilots.update({piloto.json()['name']:piloto_id})


    return render(request, 'swinfo/ship_detail.html',{
        'ship':ship,
        'films':films,
        'pilots':pilots,
    })
