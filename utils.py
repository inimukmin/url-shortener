from urllib.parse import urlparse
import random
import string

import pymysql


db_config = {"host": "localhost", "user": "root", "password": "", "db": "SHORTY"}


def get_db_connection() -> pymysql.Connection:
    """Create and return a new database connection."""
    return pymysql.connect(**db_config)


def list_data(shorty_url: str) -> tuple:
    """
    Takes short_url for input.
    Returns counter , browser , platform ticks.
    """
    with get_db_connection() as conn, conn.cursor() as cursor:

        su = [shorty_url]
        info_sql = "SELECT URL , S_URL ,TAG FROM WEB_URL WHERE S_URL= %s; "
        counter_sql = "SELECT COUNTER FROM WEB_URL WHERE S_URL= %s; "
        browser_sql = "SELECT CHROME , FIREFOX , SAFARI, OTHER_BROWSER FROM WEB_URL WHERE S_URL =%s;"
        platform_sql = "SELECT ANDROID , IOS , WINDOWS, LINUX , MAC , OTHER_PLATFORM FROM WEB_URL WHERE S_URL = %s;"

        cursor.execute(info_sql, su)
        info_fetch = cursor.fetchone()
        cursor.execute(counter_sql, su)
        counter_fetch = cursor.fetchone()
        cursor.execute(browser_sql, su)
        browser_fetch = cursor.fetchone()
        cursor.execute(platform_sql, su)
        platform_fetch = cursor.fetchone()

    return info_fetch, counter_fetch, browser_fetch, platform_fetch


def update_counters(
    cursor: pymysql.Connection, short_url: str, browser_dict: dict, platform_dict: dict
) -> None:
    """Update browser and platform counters in the database for the given short_url."""
    counter_sql = """UPDATE WEB_URL SET COUNTER = COUNTER + 1,
                     CHROME = CHROME + %s, FIREFOX = FIREFOX + %s, SAFARI = SAFARI + %s, OTHER_BROWSER = OTHER_BROWSER + %s,
                     ANDROID = ANDROID + %s, IOS = IOS + %s, WINDOWS = WINDOWS + %s, LINUX = LINUX + %s, MAC = MAC + %s, OTHER_PLATFORM = OTHER_PLATFORM + %s
                     WHERE S_URL = %s;"""
    cursor.execute(
        counter_sql,
        (
            browser_dict["chrome"],
            browser_dict["firefox"],
            browser_dict["safari"],
            browser_dict["other"],
            platform_dict["android"],
            platform_dict["iphone"],
            platform_dict["windows"],
            platform_dict["linux"],
            platform_dict["macos"],
            platform_dict["other"],
            short_url,
        ),
    )


def random_token(size: int = 6) -> str:
    """
    Generates a random string of 6 chars , use size argument
    to change the size of token.
    Returns a valid token of desired size ,
    *default is 6 chars
    """
    BASE_LIST = string.digits + string.ascii_letters

    token = "".join((random.choice(BASE_LIST)) for char in range(size))
    return token


def url_check(url: str) -> bool:
    """
    Expects a string as argument.
    Retruns True , if URL is valid else False.
    For detailed docs look into urlparse.
    """
    try:
        result = urlparse(url)
        if all([result.scheme, result.netloc]):
            return True
        else:
            return False
    except:
        return False