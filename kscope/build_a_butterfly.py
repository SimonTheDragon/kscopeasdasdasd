import requests
from bs4 import BeautifulSoup as BS
import sys
from bestiary.models import Farfalla, Provincia, Superfamiglia, Famiglia, Sottofamiglia, Tribu

# py manage.py shell
# exec(open('build_a_butterfly.py').read())

TEMPI_VOLO = (
    ('1', 'Inizio Gennaio'),
    ('2', 'Metà Gennaio'),
    ('3', 'Fine Gennaio'),
    ('4', 'Inizio Febbraio'),
    ('5', 'Metà Febbraio'),
    ('6', 'Fine Febbraio'),
    ('7', 'Inizio Marzo'),
    ('8', 'Metà Marzo'),
    ('9', 'Fine Marzo'),
    ('10', 'Inizio Aprile'),
    ('11', 'Metà Aprile'),
    ('12', 'Fine Aprile'),
    ('13', 'Inizio Maggio'),
    ('14', 'Metà Maggio'),
    ('15', 'Fine Maggio'),
    ('16', 'Inizio Giugno'),
    ('17', 'Metà Giugno'),
    ('18', 'Fine Giugno'),
    ('19', 'Inizio Luglio'),
    ('20', 'Metà Luglio'),
    ('21', 'Fine Luglio'),
    ('22', 'Inizio Agosto'),
    ('23', 'Metà Agosto'),
    ('24', 'Fine Agosto'),
    ('25', 'Inizio Settembre'),
    ('26', 'Metà Settembre'),
    ('27', 'Fine Settembre'),
    ('28', 'Inizio Ottobre'),
    ('29', 'Metà Ottobre'),
    ('30', 'Fine Ottobre'),
    ('31', 'Inizio Novembre'),
    ('32', 'Metà Novembre'),
    ('33', 'Fine Novembre'),
    ('34', 'Inizio Dicembre'),
    ('35', 'Metà Dicembre'),
    ('36', 'Fine Dicembre'),
)

TEMPI_VOLO = dict((letter, number) for (number, letter) in TEMPI_VOLO)
print(TEMPI_VOLO)


def build_butterfly():

    url = "https://www.papilionea.it/zerynthia-polyxena/"

    soup = get_soup(url)

    families_list = get_families(soup)

    real_province_objects = get_provs(soup)

    name = get_name(soup)

    aperture = get_aperture(soup)

    common_names = get_common_names(soup)

    flight_pattern = get_flight(soup)

    #new_butterfly = Farfalla(Superfamiglia=families_list[0], Famiglia=families_list[1], Sottofamiglia=families_list[2],
                             #Tribu=families_list[3], nome=name, apertura_alare_m=aperture[0], apertura_alare_f=aperture[1], nomi_comuni=common_names, inizio_volo=flight_pattern[0], fine_volo=flight_pattern[1])

    #new_butterfly.save()

    #new_butterfly.habitat.set(real_province_objects)
    #new_butterfly.save()


def get_soup(url):

    r = requests.get(url)

    soup = BS(r.content, "html5lib")

    return(soup)


def get_families(soup):

    block = soup.find(lambda tag: tag.name ==
                      "span" and "Classificazione:" in tag.text).find_parent().findChildren("strong")

    families_list = []

    for x in block:
        families_list.append(str(x.text))

    fam_tags = (Superfamiglia, Famiglia, Sottofamiglia, Tribu)

    for x in range(0, 4):

        curr_tag = fam_tags[x]

        try:
            families_list[x] = curr_tag.objects.filter(
                nome=families_list[x])[0]

        except:
            new_object = curr_tag(nome=families_list[x])
            new_object.save()
            families_list[x] = new_object

    return(families_list)


def get_provs(soup):

    provinces = soup.find_all("g")
    provinces_list = []
    populated_provinces = []

    for x in provinces:
        provinces_list.append(str(x))

    for x in provinces_list:

        if x.find("#67b564") > -1:

            if x[12] == "_":
                current_province = x[13]+x[14]

            else:
                current_province = x[14]+x[15]

            populated_provinces.append(current_province)

    province_objects = Provincia.objects.filter(sigla__in=populated_provinces)

    real_province_objects = []

    for x in province_objects:
        real_province_objects.append(x.sigla)

    return(real_province_objects)


def get_name(soup):

    name = soup.find("speciesid").text

    print(name)

    return(name)


def get_aperture(soup):

    apertura_alare = soup.find(
        lambda tag: tag.name == "span" and "Apertura alare:" in tag.text).find_parent().text

    start_m = (apertura_alare.index("i") + 2)
    end_m = (apertura_alare.index(" mm"))

    apertura_m = apertura_alare[start_m:end_m]

    start_f = (apertura_alare.index("n")+3)
    end_f = (len(apertura_alare) - 3)

    apertura_f = apertura_alare[start_f:end_f]

    return(apertura_m, apertura_f)


def get_common_names(soup):

    starting_string = soup.find(
        lambda tag: tag.name == "span" and "Nomi comuni:" in tag.text).find_parent().text

    start_names = starting_string.index(":") + 1
    end_names = starting_string.index(".")
    common_names = starting_string[start_names:end_names]

    return(common_names)


def get_flight(soup):

    starting_list = soup.find(
        lambda tag: tag.name == "span" and "Periodo di volo:" in tag.text).find_parent().text.split()

    checks = ['ini', 'met', 'fin']

    if starting_list[3][0:3] in checks:

        first_param = starting_list[3].capitalize(
        ) + ' ' + starting_list[4].capitalize()

        if starting_list[6][0:3] in checks:
            second_param = starting_list[6].capitalize(
            ) + ' ' + starting_list[7].capitalize()

        else:
            second_param = 'Fine ' + starting_list[6].capitalize()

    else:
        first_param = 'Inizio ' + starting_list[3].capitalize()

        if starting_list[5][0:3] in checks:
            second_param = starting_list[5].capitalize(
            ) + ' ' + starting_list[7].capitalize()

        else:
            second_param = 'Fine ' + starting_list[5].capitalize()

    first_param = TEMPI_VOLO[first_param]

    second_param = TEMPI_VOLO[second_param]

    print(first_param, second_param)

    return([first_param, second_param])


build_butterfly()
