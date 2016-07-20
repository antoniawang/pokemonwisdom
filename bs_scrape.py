import json
import os
import re
import urllib2

from bs4 import BeautifulSoup



# <tr class=" UILinkedTableRow">
# <td class="bulbasaur" style="width: 168px;">
# <a class="rowLink" href="/pokedex/pokemon/bulbasaur"><img src="/pokedex/images/mini/001.png" alt="001">Bulbasaur</a>
# </td>
# <td style="width: 110px;">001</td>
# <td style="width: 69px;">---</td>
# <td class="grass" style="width: 74px;"><img src="/pokedex/images/types/grass.gif" alt="Grass"></td>
# <td class="poison" style="width: 74px;"><img src="/pokedex/images/types/poison.gif" alt="Poison"></td>
# <td style="width: 65px;">45</td><td style="width: 65px;">49</td><td style="width: 65px;">49</td><td style="width: 65px;">65</td><td style="width: 65px;">65</td><td style="width: 65px;">45</td><td style="width: 65px;">318</td>
# </tr>


# <tr class="alt UILinkedTableRow">
# <td class="ivysaur">
# <a class="rowLink" href="/pokedex/pokemon/ivysaur"><img src="/pokedex/images/mini/002.png" alt="002">Ivysaur</a>
# </td>
# <td>002</td>
# <td>---</td>
# <td class="grass"><img src="/pokedex/images/types/grass.gif" alt="Grass"></td>
# <td class="poison"><img src="/pokedex/images/types/poison.gif" alt="Poison"></td>
# <td>60</td><td>62</td><td>63</td><td>80</td><td>80</td><td>60</td><td>405</td>
# </tr>

# http://pokedream.com/pokedex/images/mini/711.png

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
        pokemon_dict['name'] = img.get_text() # pokemon name
        pokemon_dict['thumbnail_path'] = 'static/thumbnails/%s_thumbnail.png' % img.attrs['alt'] # path to thumbnail
        pokemon_dict['pic_path'] = 'static/images/%s' % img.attrs['alt'] # path to main image

        
        print main_url + img.attrs['src']

        # download thumbnail
        r = urllib2.urlopen(main_url + img.attrs['src'])
        f = open(r'static/thumbnails/%s_thumbnail.png' % img.attrs['alt'], 'wb')
        f.write(r.read())
        f.close()

        # download main image
        pokemon_page = urllib2.urlopen(main_url + pokemon.attrs['href']).read()
        soup = BeautifulSoup(pokemon_page, "html.parser")
        main_img = soup.find('img', class_='main-picture')
        r = urllib2.urlopen(main_url + main_img.attrs['src'])
        f = open(r'static/images/%s.jpg' % main_img.attrs['title'], 'wb')
        f.write(r.read())
        f.close()


        all_pokemons_dicts.append(pokemon_dict)

    return all_pokemons_dicts

create_pokemon_dicts()



