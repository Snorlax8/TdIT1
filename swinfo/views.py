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

def planet_detail(request, planet_id):
    response = requests.get('https://swapi.co/api/planets/'+str(planet_id))
    planet = response.json()
    films = []
    residents = {}

    for film in planet['films']:
        movie = requests.get(film)
        films.append(movie.json())

    for resident in planet['residents']:
        residente = requests.get(resident)
        head, partition, tail = resident.partition("people/")
        residente_id = tail[:-1]
        residents.update({residente.json()['name']:residente_id})

    return render(request, 'swinfo/planet_detail.html',{
        'planet':planet,
        'films':films,
        'residents':residents,
    })


def search(request):
    if 'q' in request.GET:
        q = request.GET['q']
        movies_result = requests.get('https://swapi.co/api/films/'+'?search='+q)
        movies = movies_result.json()
        movies_sources = []

        for pelicula in movies["results"]:
            movies_sources.append(pelicula)

        while movies["next"]:
            movies = requests.get(movies["next"]).json()
            for pelicula in movies["results"]:
                movies_sources.append(pelicula)

        character_result = requests.get('https://swapi.co/api/people/'+'?search='+q)
        characters = character_result.json()
        characters_sources = []
        for personaje in characters["results"]:
            head, partition, tail = personaje["url"].partition("people/")
            character_id = tail[:-1]
            personaje.update({"id":character_id})
            characters_sources.append(personaje)
        while characters["next"]:
            characters = requests.get(characters["next"]).json()
            for personaje in characters["results"]:
                head, partition, tail = personaje["url"].partition("people/")
                character_id = tail[:-1]
                personaje.update({"id":character_id})
                characters_sources.append(personaje)


        planet_result = requests.get('https://swapi.co/api/planets/'+'?search='+q)
        planets = planet_result.json()
        planets_sources = []
        for planeta in planets["results"]:
            head, partition, tail = planeta["url"].partition("planets/")
            planet_id = tail[:-1]
            planeta.update({"id":planet_id})
            planets_sources.append(planeta)
        while planets["next"]:
            planets = requests.get(planets["next"]).json()
            for planeta in planets["results"]:
                head, partition, tail = planeta["url"].partition("planets/")
                planet_id = tail[:-1]
                planeta.update({"id":planet_id})
                planets_sources.append(planeta)


        ship_result = requests.get('https://swapi.co/api/starships/'+'?search='+q)
        ships = ship_result.json()
        ships_sources = []
        for nave in ships["results"]:
            head, partition, tail = nave["url"].partition("starships/")
            ship_id = tail[:-1]
            nave.update({"id":ship_id})
            ships_sources.append(nave)
        while ships["next"]:
            ships = requests.get(ships["next"]).json()
            for nave in ships["results"]:
                head, partition, tail = nave["url"].partition("starships/")
                ship_id = tail[:-1]
                nave.update({"id":ship_id})
                ships_sources.append(nave)


        return render(request, 'swinfo/search.html', {
            'movies' : movies_sources,
            'characters' : characters_sources,
            'planets' : planets_sources,
            'ships' : ships_sources,
        })


    else:
        return HttpResponse("Por favor ingresa un término para buscar.")
