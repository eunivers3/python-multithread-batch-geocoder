import requests
import argparse
import json
from urllib.parse import quote_plus

class Geocoder:
    def __init__(self, api_key):
        self.api_key = api_key
        
    def geocode(self, country_restriction, language_output, address):
        address =  quote_plus(str(address))
        base = "https://maps.googleapis.com/maps/api/geocode/json?address={}".format(address)
        key = "&key={}".format(self.api_key)        
        set_country_restriction = "&components=country:{}".format(country_restriction)
        set_language_output = "&language={}".format(language_output)

        if self.api_key is not None:
            if country_restriction is not None and language_output is not None:
                geocode_url = base + key + set_country_restriction + set_language_output
            elif country_restriction is not None:
                geocode_url = base + key + set_country_restriction 
            elif language_output is not None:
                geocode_url = base + key + set_language_output
            else:
                geocode_url = base + key

        def get_address_component(answer, key):
            """
            get info about specific address components from the 
            google geocoder results
            """
            results = ",".join([x['long_name'] for x in answer.get('address_components') 
                if key in x.get('types')])
            return results
        
        # Ping google for the results
        results = requests.get(geocode_url)
        results = results.json()
        output = dict()
        # if there's results, flatten them
        if len(results['results']) > 0:  
            answer = results['results'][0]
            output.update({
                "place_id" : answer.get('place_id'),
                "formatted_address" : answer.get('formatted_address'),
                "type": ",".join(answer.get('types')), # list
                "partial_match": answer.get('partial_match'),
                "latitude": answer.get('geometry').get('location').get('lat'),
                "longitude": answer.get('geometry').get('location').get('lng'),
                "viewport_northeast_lat": answer.get('geometry').get('viewport').get('northeast').get('lat'),
                "viewport_northeast_lng": answer.get('geometry').get('viewport').get('northeast').get('lng'),
                "viewport_southwest_lat": answer.get('geometry').get('viewport').get('southwest').get('lat'),
                "viewport_southwest_lng": answer.get('geometry').get('viewport').get('southwest').get('lng'),
                "accuracy": answer.get('geometry').get('location_type'),
                "street_number": get_address_component(answer, "street_number"),
                "street_address": get_address_component(answer, "street_address"),
                "route": get_address_component(answer, "route"),
                "intersection": get_address_component(answer, "intersection"),
                "political": get_address_component(answer, "political"),
                "country": get_address_component(answer, "country"),
                "administrative_area_level_1": get_address_component(answer, "administrative_area_level_1"),
                "administrative_area_level_2": get_address_component(answer, "administrative_area_level_2"),
                "administrative_area_level_3": get_address_component(answer, "administrative_area_level_3"),
                "administrative_area_level_4": get_address_component(answer, "administrative_area_level_4"),
                "administrative_area_level_5": get_address_component(answer, "administrative_area_level_5"),
                "colloquial_area": get_address_component(answer, "colloquial_area"),
                "locality": get_address_component(answer, "locality"),
                "sublocality": get_address_component(answer, "sublocality"),
                "neighborhood_name": get_address_component(answer, "neighborhood"),
                "premise": get_address_component(answer, "premise"),
                "subpremise": get_address_component(answer, "subpremise"),
                "postal_code": get_address_component(answer, "postal_code"),
                "natural_feature": get_address_component(answer, "natural_feature"),
                "airport": get_address_component(answer, "airport"),
                "park": get_address_component(answer, "park"),
                "point_of_interest": get_address_component(answer, "point_of_interest"),
                "floor": get_address_component(answer, "floor"),
                "parking": get_address_component(answer, "parking"),
                "room": get_address_component(answer, "room")
            })
        output['input_string'] = address
        output['number_of_results'] = len(results['results'])
        output['status'] = results.get('status')
        return output

def save(results_arr, output='json'):
    """
    Saves results list as results.json or results.csv, default output is json file
    """
    import json
    if output == "json":
        with open("results.json", 'w') as outfile:
            print ("Saving results to results.json")
            json.dump(results_arr, outfile)
    elif output == "csv":
        import pandas as pd
        result_df = pd.read_json(json.dumps(results_arr), orient='records')
        print ("Saving results to results.csv")
        result_df.to_csv("results.csv",index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('key', help='your google api key')
    parser.add_argument('file', help='path to .csv or .txt file containing list of new line separated addresses')
    parser.add_argument('save', help='set to "csv" or "json"')
    parser.add_argument('--country', help='set country restriction; see alpha-2 country codes https://en.wikipedia.org/wiki/ISO_3166-1')
    parser.add_argument('--lang', help='optional language code in which to return results; see https://developers.google.com/maps/faq#languagesupport')
    args = parser.parse_args()

    results = list()
    with open(args.file) as f:
        addresses = [ line.strip() for line in f ]
        for address in addresses:
            print("Geocoding: {}".format(address))
            output = Geocoder(args.key).geocode(args.country, args.lang, address)
            results.append(output)
            if len(results) % 100 == 0:
                print ("Geocoded {} of {} addresses".format(len(results), len(addresses)))
        print("Finished geocoding all addresses!")

    if args.save == 'csv' : save(results, output='csv') 
    if args.save == 'json' : save(results) 