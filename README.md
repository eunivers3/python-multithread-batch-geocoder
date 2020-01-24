# Python Batch Address Geocoder
Geocode a list of addresses to get their GPS coordinates and other geospatial information using the Google Geocoding API.

## Usage
To run [geocode.py](geocode.py), you will also need a .csv or .txt file containing a list of addresses you want to geocode.

#### Synopsis
`python geocode.py [GOOGLE_API_KEY] [FILEPATH] [SAVE] [--country=COUNTRY_RESTRICTION] [--lang=LANGUAGE_OUTPUT]`

#### Positional Arguments
**GOOGLE_API_KEY**
Your google api key to enable the geocoding service.

**FILEPATH**
Path to file containing a list addresses. Each address *must* be separated by a new line.

**SAVE**
Set to "json" or "csv" for your desired output format.

#### Optional Flags
**--country=COUNTRY_RESTRICTION** 
Set a country restriction; see alpha-2 country codes https://en.wikipedia.org/wiki/ISO_3166-1

**--lang=LANGUAGE_OUTPUT** 
Optional language code in which to return results; see https://developers.google.com/maps/faq#languagesupport

## Results
The results generated will be saved as a JSON or CSV file.

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
    "number_of_results": "int, number of results returned by the Geocoding API given the input string (only the first result is represented in the successful response)",
    "status": "string"
}
```

See the Google geocoding [guide](https://developers.google.com/maps/documentation/geocoding/intro) for detailed descriptions of each key field.