import logging

from requests import ConnectionError, HTTPError, Request, Session
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)


def make_request(method, url, json_body, headers):
    """Makes a JSON request

    Parameters:
        method (RequestMethod):
        url (url):
        json_body (JSON):
        headers (JSON):

    Returns:
        response (response):

    """
    s = Session()

    req = Request(
        method,
        url,
        json=json_body,
        headers=headers,
    )

    prepped = req.prepare()

    prepped.headers["Content-Type"] = "application/json"
    prepped.headers["Accept"] = "application/json"
    prepped.headers["User-Agent"] = "request-scheduler/0.1.0"

    try:
        response = s.send(prepped)
        response.raise_for_status()
    except HTTPError:
        return response
    except ConnectionError:
        logger.error("ConnectionError", exc_info=True)
    except RequestException:
        logger.error("RequestException", exc_info=True)

    if response:
        return response

    return False
