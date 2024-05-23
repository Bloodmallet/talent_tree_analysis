import requests
import logging
import json

logging.basicConfig(level=logging.INFO)

logger =logging.getLogger()

class CouldNotLoadTalentError(Exception):
    pass

def update_data()->None:
    # options: beta / ptr / xptr / live
    data_endpoint = "live"

    url = f"https://www.raidbots.com/static/data/{data_endpoint}/talents.json"
    logger.info(f"Updating talent '{data_endpoint}' data using '{url}'. Make sure to thank him and don't stress the endpoint!")

    loaded_data = requests.get(url)
    try:
        loaded_data.raise_for_status()
    except requests.HTTPError as e:
        raise CouldNotLoadTalentError(
            f"Couldn't load Talent information from raidbots. {loaded_data.status_code}: {loaded_data.reason}"
        ) from e
    
    json_data = loaded_data.json()

    with open(
        r"data/talents.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(json_data, f, ensure_ascii=False)


if __name__ == "__main__":
    update_data()
