import logging
from configparser import ConfigParser

import requests
from bs4 import BeautifulSoup as soup

log = logging.getLogger("cdwifi")


# TODO: put into common
def meta_redirect(content: str) -> str:
    parsed = soup(content, features="html.parser")

    result = parsed.find("meta", attrs={"http-equiv": "refresh"})
    if result:
        wait, text = result["content"].split(";")
        if text.strip().lower().startswith("url="):
            url = text[4:]
            return url
    raise Exception("Cannot find meta redirect in content")


def match_connection(connection: ConfigParser) -> bool:
    """
        return true for an open wifi spot as hotsplots only provides open spots
    """
    log.debug('YYYYYYYYYYYYYYYYYYY')
    log.debug(connection)
    if "wifi" not in connection:
        log.info("Connection is not Wifi, assuming no Captive Portal")
        return False
    elif "wifi-security" in connection:
        log.info("Secured Wifi, assuming no Captive Portal")
        return False
    elif True:
        help(connection)
        log.info("dunno lol")
    else:
        log.info("Unsecured wifi, might be cdwifi!")
        return True


def match(resp: requests.Response) -> bool:
    """
      resp: the initial response of the internet get request
    """
    return "On Board Portal" in resp.text


def accept(resp: requests.Response, s: requests.Session) -> bool:
    """
      resp: the initial response of the internet get request
      s: the requests session for opening new http connections
    return True if successful, else False
    """

    resp = s.get('https://www.ombord.info/hotspot/hotspot.cgi?connect=Connect&method=login&username=lab&password=CAEN&realm=lab&url=http%3A%2F%2Fcdwifi.cz%2Fcaptive%2Fsuccess&onerror=http%3A%2F%2Fcdwifi.cz%2Fcaptive')
    log.debug("Return code: {resp.status_code}")
    return resp.ok
