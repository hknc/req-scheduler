import logging

from requests import Request, Session
from requests.exceptions import ConnectionError, RequestException, Timeout

logger = logging.getLogger(__name__)


class ServiceError(Exception):
    """Base class for exceptions"""

    pass


class FailedRequestError(ServiceError):
    pass


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

    try:
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

        response = s.send(prepped)

        return response

    except ConnectionError as err:
        logger.error("Error connecting: ", err)
    except Timeout as err:
        logger.error("Timeout error: ", err)
    except RequestException as err:
        logger.error("Error: ", err)
        raise FailedRequestError()
