import requests
import argparse
import json
import pandas as pd
import multiprocessing
import multiprocessing.pool
import time
from urllib.parse import quote_plus
from ratelimit import limits, sleep_and_retry
import logging


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
FORMATTER = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
STREAM_HANDLER = logging.StreamHandler()
STREAM_HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(STREAM_HANDLER)

ONE_SECOND = 1
MAX_CALLS = 50
POOL_SIZE = multiprocessing.cpu_count()


class GeocoderService:
    def __init__(self, api_key):
        self.api_key = api_key

    @staticmethod
    def get_address_component(answer, key):
        """
            get info about specific address components from the google geocoder results
            """
        results = ",".join(
            [
                x["long_name"]
                for x in answer.get("address_components")
                if key in x.get("types")
            ]
        )
        return results

    @sleep_and_retry
    @limits(calls=MAX_CALLS, period=ONE_SECOND)
    def geocode(
        self, address: str, country_restriction: str = None, language_output: str = None
    ):
        if self.api_key is not None:
            reformatted_address = quote_plus(str(address).strip())
            geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={key}".format(
                address=reformatted_address, key=self.api_key
            )
            if country_restriction and language_output:
                geocode_url = "{base}{country}{language}".format(
                    base=geocode_url,
                    country="&components=country:{}".format(country_restriction),
                    language="&language={}".format(language_output),
                )
            elif country_restriction:
                geocode_url = "{base}{country}".format(
                    base=geocode_url,
                    country="&components=country:{}".format(country_restriction),
                )
            # Ping google for the results
            results = requests.get(geocode_url)
            results = results.json()
            status = results.get("status")
            output = dict()
            # if there's results, flatten them
            if len(results["results"]) > 0:
                # return first result only if there's multiple
                answer = results["results"][0]
                output.update(
                    {
                        "requested_address": str(address),
                        "place_id": answer.get("place_id"),
                        "formatted_address": answer.get("formatted_address"),
                        "type": ",".join(answer.get("types")),  # list
                        "partial_match": True if answer.get("partial_match") else False,
                        "location_type": answer.get("geometry").get("location_type"),
                        "latitude": answer.get("geometry").get("location").get("lat"),
                        "longitude": answer.get("geometry").get("location").get("lng"),
                        "street_number": GeocoderService.get_address_component(
                            answer, "street_number"
                        ),
                        "street_address": GeocoderService.get_address_component(
                            answer, "street_address"
                        ),
                        "route": GeocoderService.get_address_component(answer, "route"),
                        "intersection": GeocoderService.get_address_component(
                            answer, "intersection"
                        ),
                        "political": GeocoderService.get_address_component(
                            answer, "political"
                        ),
                        "country": ",".join(
                            [
                                x["short_name"]
                                for x in answer.get("address_components")
                                if "country" in x.get("types")
                            ]
                        ),
                        "administrative_area_level_1": GeocoderService.get_address_component(
                            answer, "administrative_area_level_1"
                        ),
                        "administrative_area_level_2": GeocoderService.get_address_component(
                            answer, "administrative_area_level_2"
                        ),
                        "administrative_area_level_3": GeocoderService.get_address_component(
                            answer, "administrative_area_level_3"
                        ),
                        "administrative_area_level_4": GeocoderService.get_address_component(
                            answer, "administrative_area_level_4"
                        ),
                        "administrative_area_level_5": GeocoderService.get_address_component(
                            answer, "administrative_area_level_5"
                        ),
                        "colloquial_area": GeocoderService.get_address_component(
                            answer, "colloquial_area"
                        ),
                        "locality": GeocoderService.get_address_component(
                            answer, "locality"
                        ),
                        "sublocality": GeocoderService.get_address_component(
                            answer, "sublocality"
                        ),
                        "neighborhood": GeocoderService.get_address_component(
                            answer, "neighborhood"
                        ),
                        "premise": GeocoderService.get_address_component(
                            answer, "premise"
                        ),
                        "subpremise": GeocoderService.get_address_component(
                            answer, "subpremise"
                        ),
                        "postal_code": GeocoderService.get_address_component(
                            answer, "postal_code"
                        ),
                        "floor": GeocoderService.get_address_component(answer, "floor"),
                        "parking": GeocoderService.get_address_component(
                            answer, "parking"
                        ),
                        "room": GeocoderService.get_address_component(answer, "room"),
                    }
                )
                LOGGER.info("%s: %s", status, address)
            else:
                LOGGER.warning("%s: %s", status, address)
        else:
            LOGGER.error("Missing API key")

        output["status"] = status
        output["number_of_results"] = len(results["results"])
        return output


def save(results_arr, output="json"):
    """
    Saves results list as results.json or results.csv, default output is json file
    """
    if output == "json":
        with open("results.json", "w") as outfile:
            LOGGER.info("Saving results to results.json")
            json.dump(results_arr, outfile, ensure_ascii=False)
    elif output == "csv":
        result_df = pd.read_json(json.dumps(results_arr), orient="records")
        LOGGER.info("Saving results to results.csv")
        result_df.to_csv("results.csv", index=False)


def GeocodeWrapper(addresses: list, country: str, language: str, api_key: str):
    """
        GeocodeWrapper is a wrapper for multiprocessing
        Returns:
            geocode results
        """
    LOGGER.info("Starting Geocoder - country:%s lang:%s", country, language)
    start_time = time.time()
    with multiprocessing.pool.ThreadPool(POOL_SIZE) as executor:
        args = [(address, country, language) for address in addresses]
        results = executor.starmap(GeocoderService(api_key).geocode, args)
    LOGGER.info("Finished in %s seconds", (time.time() - start_time))

    return results


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("key", help="your google api key")
    PARSER.add_argument(
        "file",
        help="path to .csv or .txt file containing list of new line separated addresses",
    )
    PARSER.add_argument("save", help='set to "csv" or "json"')
    PARSER.add_argument(
        "--country",
        help="set country restriction; see alpha-2 country codes https://en.wikipedia.org/wiki/ISO_3166-1",
    )
    PARSER.add_argument(
        "--lang",
        help="optional language code in which to return results; see https://developers.google.com/maps/faq#languagesupport",
    )
    ARGS = PARSER.parse_args()

    with open(ARGS.file) as f:
        ADDRESSES = [line.strip() for line in f]
        GEOCODE_RESULTS = GeocodeWrapper(ADDRESSES, ARGS.country, ARGS.lang, ARGS.key)

        if ARGS.save == "csv":
            save(GEOCODE_RESULTS, output="csv")
        elif ARGS.save == "json":
            save(GEOCODE_RESULTS)
        else:
            LOGGER.error("Invalid save format. Must be csv or json.")
