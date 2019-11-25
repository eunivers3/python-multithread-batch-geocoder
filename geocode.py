import requests
import json
from urllib.parse import quote_plus

class Geocoder:
    def __init__(self, api_key, country_restriction, language_output, address):
        self.api_key = api_key
        self.country_restriction = country_restriction
        self.language_output = language_output
        self.address = address
        self.__output = {
            "place_id": None,
            "formatted_address" : None,
            "type": None,
            "partial_match": None,
            "latitude": None,
            "longitude": None,
            "viewport_northeast_lat": None,
            "viewport_northeast_lng": None,
            "viewport_southwest_lat": None,
            "viewport_southwest_lng": None,
            "accuracy": None,
            "street_number": None,
            "street_address": None,
            "route": None,
            "intersection": None,
            "political": None,
            "country": None,
            "administrative_area_level_1": None,
            "administrative_area_level_2": None,
            "administrative_area_level_3": None,
            "administrative_area_level_4": None,
            "administrative_area_level_5": None,
            "colloquial_area": None,
            "locality": None,
            "sublocality": None,
            "neighborhood_name": None,
            "premise": None,
            "subpremise": None,
            "postal_code": None,
            "natural_feature": None,
            "airport": None,
            "park": None,
            "point_of_interest": None,
            "floor": None,
            "parking" : None,
            "room": None
        }

    def geocode(self):
        address =  quote_plus(str(self.address))
        base = "https://maps.googleapis.com/maps/api/geocode/json?address={}".format(address)
        key = "&key={}".format(self.api_key)        
        set_country_restriction = "&components=country:{}".format(self.country_restriction)
        set_language_output = "&language={}".format(self.language_output)

        if self.api_key is not None:
            if self.country_restriction is not None and self.language_output is not None:
                geocode_url = base + key + set_country_restriction + set_language_output
            elif self.country_restriction is not None:
                geocode_url = base + key + set_country_restriction 
            elif self.language_output is not None:
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
        # if there's results, flatten them
        if len(results['results']) > 0:  
            answer = results['results'][0]
            self.__output = {
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
            }    
            self.__output['input_string'] = self.address
            self.__output['number_of_results'] = len(results['results'])
            self.__output['status'] = results.get('status')
        return self.__output

def save_results(results_arr, output='json'):
    """
    Saves results list as results.json or results.csv, default output is json file
    """
    import json
    if output == "json":
        with open("results.json", 'w') as outfile:
            print ("Saving results to {}".format("results.json"))
            json.dump(results_arr, outfile)
    elif output == "csv":
        import pandas as pd
        result_df = pd.read_json(json.dumps(results_arr), orient='records')
        print ("Saving results to {}".format("results.csv"))
        result_df.to_csv("results.csv",index=False)


#------------------ PROCESSING -----------------------------
if __name__ == "__main__":
    # TODO Developer: Set arguments
    api_key = 'SET_YOUR_GOOGLE_API_KEY_HERE' 
    # alpha-2 country code; https://en.wikipedia.org/wiki/ISO_3166-1 e.g.
    country_restriction = 'UK'
    # OPTIONAL; language code in which to return results; https://developers.google.com/maps/faq#languagesupport
    language_output = None
    # list of locations e.g.
    addresses = [
        "the gherkin, london", 
        "nw6 2lh"
    ]
    results = list()
    for address in addresses:
        output = Geocoder(
            api_key, country_restriction, language_output, address
        ).geocode()
        results.append(output)
        if len(results) % 100 == 0:
            print ("Geocoded {} of {} address".format(len(results), len(addresses)))
    # Save results here
    save_results(results)
    print(json.dumps(results, indent=4))