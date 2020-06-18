# Python Multithreaded Batch Address Geocoder
Geocode a list of addresses in a .csv or .txt file to get their GPS coordinates and other geospatial information using the Google Geocoding API.
Each address in the input file *must* be separated by a new line.

### Prerequisites
* Python 3 or above
* Pythons pip

### Usage
To run [geocode.py](geocode.py), you will need a .csv or .txt file containing a list of addresses you want to geocode.
1. **Clone the Repo**<br />
`$ git clone git@github.com:eunicebjm/python-batch-geocoder.git`<br />
2. **Requirements**<br />
`$ pip install -r requirements.txt`<br />
3. **Execute**<br />
`$ python geocode.py [GOOGLE_API_KEY] [FILEPATH] [SAVE] [--country=COUNTRY_RESTRICTION] [--lang=LANGUAGE_OUTPUT]`
e.g. **`python geocode.py <YOUR_KEY_HERE> addr.csv json --country UK`**

#### Positional Arguments
`[GOOGLE_API_KEY]`
your google api key to enable the geocoding service.

`[FILEPATH]`
path to file containing a list of addresses.

`[SAVE]`
set to "json" or "csv" for your desired output format.

#### Optional Flags
`--country=COUNTRY_RESTRICTION`
set country restriction of addresses to an [alpha-2 country code](https://en.wikipedia.org/wiki/ISO_3166-1)

`--lang=LANGUAGE_OUTPUT`
optional [language code](https://developers.google.com/maps/faq#languagesupport) in which to return results

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