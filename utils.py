from dotenv import load_dotenv

from database.database import DatabaseManager


def get_dbm() -> DatabaseManager:
    load_dotenv()
    return DatabaseManager()


def rename_keys_in_dict_list(l: list, keys: list) -> list:
    """
    Uses the list of keys to change the keys in each dictionary
    in the given list
    """
    for i, item in enumerate(l):
        dict = {}
        for x, key in enumerate(keys):
            if key is not None:
                dict[key] = list(item.values())[x]
        l[i] = dict

    return l


def get_price_change_from_previous(ticker: str, latest_price: int) -> dict:
    """
    Get's the percentage and actual change in price from previous close
    """
    dbm = DatabaseManager()
    previous_close = dbm.get_previous_close(ticker)
    return {
        "actual": latest_price - previous_close,
        "previous": previous_close,
        "percentage": round(((latest_price - previous_close) / previous_close) * 100, 2)
    }


def merge_lists_by_date_time(list1: list, list2: list) -> list:
    """
    Merges two lists into one list of dictionaries
    """
    merged = []
    list1.sort(key=lambda x: x['datetime'])
    list2.sort(key=lambda x: x['datetime'])

    for i, dict in enumerate(list1):
        new_dict = dict.copy()
        for key, value in list2[i].items():
            new_dict[key] = value
        merged.append(new_dict)
    return merged
