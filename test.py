from prefect import flow
from datetime import date

import json
import httpx
import re
import utils

PAGE_LIMIT = 1000
STAGE_REGEXP = re.compile("(?P<quarter>[IV]+) квартал (?P<year>d+) г.")

@flow(log_prints=True)
def parse():
    utils.upload(parse_core())

def parse_core():
    return {
        "systemName": "A101",
        "name": "Группа компаний «А101»",
        "residentialComplexes": list(parse_complexes())
    }

def parse_complexes():
    flats = list(parse_flats())

    complexes_response = httpx.get("https://a101.ru/api/v2/updated_complex/")
    complexes_response.raise_for_status()

    residential_complexes = complexes_response.json()['results']

    for residential_complex in residential_complexes:
        if residential_complex['count'] == 0:
            continue

        slug = residential_complex['url'].split('/')[2]

        yield {
            'internalId': slug,
            'name': residential_complex['title'],
            'geoLocation': {
                'latitude': residential_complex['latitude'],
                'longitude': residential_complex['longitude']
            },
            'renderImageUrl': residential_complex['aboutcomplexgallery_set'][0]['image'],
            'presentationUrl': None,
            'flats': list(filter(lambda f: f['residentialComplexInternalId'] == slug, flats))
        }

    print('Complexes are parsed')

def parse_flats():
    offset = 0

    while True:
        flats_response = httpx.get(f"https://a101.ru/api/v2/flat/?ordering=actual_price&limit={PAGE_LIMIT}&offset={offset}", timeout=30)
        flats_response.raise_for_status()

        flats = flats_response.json()['results']
        if len(flats) == 0:
            break

        for flat in flats:
            yield {
                "residentialComplexInternalId": flat['complex_slug'],
                "developerUrl": f"https://a101.ru/kvartiry/{flat['id']}/",
                "price": flat['price'],
                "floor": int(str(flat['floor']).split('-')[0]),
                "area": flat['area'],
                "rooms": 0 if int(flat['studio']) == 0 else flat['room'],
                "buildingDeadline": evaluate_building_deadline(flat),
                "layoutImageUrl": flat['plan_image'],
            }

        print(f'Parsed {offset + len(flats)} flats')

        offset += PAGE_LIMIT

    print('Flats are parsed')

def evaluate_building_deadline(flat):
    if flat['stage'] == 'Квартира с ключами' or flat['stage'] == 'Подготовка к выдаче ключей':
        return date.min.isoformat()

    parsed_stage = STAGE_REGEXP.fullmatch(flat['stage'])

    building_deadline_date = utils.create_date_from_quarter(
        year=int(parsed_stage.group('year')),
        quarter=utils.transform_roman_to_arabic(parsed_stage.group('quarter'))
    )

    return building_deadline_date.isoformat()

if __name__ == '__main__':
    print(json.dumps(parse_core()))