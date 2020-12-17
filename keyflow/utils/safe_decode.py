import logging


def safe_decode(item):
    if isinstance(item, bytes):
        return item.decode()
    elif not isinstance(item, str):
        logging.info(
            "safe_decode() was passed unexected type: {item_type}".format(
                item_type=item.__class__
            )
        )
    return item
