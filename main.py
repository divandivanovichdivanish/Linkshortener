import requests
from urllib.parse import urlparse
import os
import argparse
from dotenv import load_dotenv


API_URL = "https://api-ssl.bitly.com/v4/bitlinks"


def shorten_url(input_url, oauth2_http_header):
    long_url = {"long_url": input_url}
    response = requests.post(
        API_URL, 
        json=long_url, 
        headers=oauth2_http_header,
    )
    response.raise_for_status()
    bitlink = response.json()["link"]
    return bitlink


def count_clicks(bitlink_id, oauth2_http_header):
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink_id}/clicks/summary"
    response = requests.get(
        url, 
        headers=oauth2_http_header,
    )
    response.raise_for_status()
    total_clicks = response.json()["total_clicks"]
    return total_clicks


def is_bitlink(oauth2_http_header, bitlink_id):
    response = requests.get(
        f"{API_URL}/{bitlink_id}",
        headers=oauth2_http_header,
    )
    return response.ok


def get_bitlink_id(bitlink_url):
    bitlink_url_components = urlparse(bitlink_url)
    bitlink_id = f"{bitlink_url_components.netloc}{bitlink_url_components.path}"
    return bitlink_id



def main():
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="You must provide a link for the program here")
    args = parser.parse_args()
    oauth2_http_header = {"Authorization": os.environ["BITLYTOKEN"]}
    input_url = args.url
    bitlink_id = get_bitlink_id(input_url)
    try:
        if is_bitlink(oauth2_http_header, bitlink_id):
            total_clicks = count_clicks(
                bitlink_id,
                oauth2_http_header,
            )
            print("Переходов по ссылке: ", total_clicks)
        else:  
            bitlink = shorten_url(
            input_url,
            oauth2_http_header,
            )
            print("Битлинк", bitlink)
    except requests.exceptions.HTTPError:
        print("Была введена некорректная ссылка")


if __name__ == "__main__":
    main()
