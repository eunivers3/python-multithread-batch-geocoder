# Python Batch Address Geocoder
Geocode a list of string addresses to get their coordinates and other geospatial information using the Google Geocoding API.

## Usage
To run [geocode.py](geocode.py), insert your Google API key and list of addresses you'd like to geocode. Optionally, set a country restriction you'd like to limit your addresses to, or set a language output. Leave country restriction and language output as *None* if you don't want to set any component restrictions.

Execute the code with `python geocode.py`

## Results
The list of results generated will be saved as a JSON file by default. Option to save results as a csv too.

For each address parsed, **successful** responses will have the the form:
```json
{   
    "place_id" : "string",
    "formatted_address" : "string, Google formatted address of the input string",
    "type": "string",
    "partial_match": "string",
    "latitude": "float",
    "longitude":"float",
    "viewport_northeast_lat": "string",
    "viewport_northeast_lng": "string",
    "viewport_southwest_lat": "string",
    "viewport_southwest_lng": "string",
    "accuracy": "string",
    "street_number": "string",
    "street_address": "string",
    "route": "string",
    "intersection": "string",
    "political": "string",
    "country": "string",
    "administrative_area_level_1": "string",
    "administrative_area_level_2": "string",
    "administrative_area_level_3": "string",
    "administrative_area_level_4": "string",
    "administrative_area_level_5":"string",
    "colloquial_area": "string",
    "locality": "string",
    "sublocality": "string",
    "neighborhood_name":"string",
    "premise": "string",
    "subpremise": "string",
    "postal_code": "string",
    "natural_feature": "string",
    "airport": "string",
    "park": "string",
    "point_of_interest": "string",
    "floor": "string",
    "parking": "string",
    "room": "string",
    "input_string": "string",
    "number_of_results": "int",
    "status": "string"
}
```

See the Google geocoding [guide](https://developers.google.com/maps/documentation/geocoding/intro) for detailed descriptions of each key field.