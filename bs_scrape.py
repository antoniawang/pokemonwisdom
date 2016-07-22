import json
import os
import re
import urllib2

from bs4 import BeautifulSoup


def grab_names_and_images(main_url):
    contents = urllib2.urlopen(main_url).read()
    soup = BeautifulSoup(contents, "html.parser")
    pokemon_obj_list = []
    for a in soup.findAll('a', class_='rowLink') :
        pokemon_obj_list.append(a)
    print len(pokemon_obj_list)

    return pokemon_obj_list


def create_pokemon_dicts():
    all_pokemons_dicts = []
    main_url = 'http://pokedream.com' 
    scrape_url = main_url + '/pokedex'
    pokemon_obj_list = grab_names_and_images(scrape_url)
    for pokemon in pokemon_obj_list:
        pokemon_dict = {}
        img = pokemon.find('img', attrs={'src': True, 'alt':True}) 
        pokemon_dict['id'] = img.attrs['alt'] # pokemon id

       # download thumbnail
        r = urllib2.urlopen(main_url + img.attrs['src'])
        f = open(r'static/thumbnails/%s_thumbnail.png' % img.attrs['alt'], 'wb')
        f.write(r.read())
        pokemon_dict['thumbnail_path'] = 'static/thumbnails/%s_thumbnail.png' % img.attrs['alt'] # path to thumbnail
        f.close()


        # download main image
        pokemon_page = urllib2.urlopen(main_url + pokemon.attrs['href']).read()
        new_soup = BeautifulSoup(pokemon_page, "html.parser")
        main_img = new_soup.find('img', class_='main-picture')
        r = urllib2.urlopen(main_url + main_img.attrs['src'])
        print main_url + main_img.attrs['src']
        f = open(r'static/images/%s.jpg' % main_img.attrs['title'], 'wb')
        f.write(r.read())
        pokemon_dict['name'] = main_img.attrs['title'] # pokemon name
        pokemon_dict['pic_path'] = 'static/images/%s.jpg' % main_img.attrs['title'] # path to main image   
        f.close()


        all_pokemons_dicts.append(pokemon_dict)

    return all_pokemons_dicts


def load_file():
    exiting_file = os.path.exists("pokemons.json")
    if exiting_file:
        f = open("pokemons.json", "r")
        all_pokemons_dicts = json.load(f)
        f.close()
    else:
        all_pokemons_dicts = []
    return all_pokemons_dicts


def dump_to_file(all_pokemons_dicts):
    f = open("pokemons.json", "w+")
    json.dump(all_pokemons_dicts, f, indent=4, separators=(", ", ": "))
    f.close()


def main():
    all_pokemons_dicts = load_file()
    all_pokemons_dicts = create_pokemon_dicts()
    dump_to_file(all_pokemons_dicts)

if __name__ == "__main__":
    main()