import sys

from tornado.options import options as option_parser


def safe_define(
    key,
    default=None,
    type=None,
    help=None,
    metavar=None,
    multiple=False,
    group=None,
    callback=None,
    *args,
    **kwargs
):
    """
    We try to redefine the tornado.options.define to allow redefining,
    but safe-re-updates as well.
    :param key:
    :param default:
    :param type:
    :param help:
    :param metavar:
    :param multiple:
    :param group:
    :param callback:
    :param args:
    :param kwargs:
    :return:
    """
    try:
        _ = option_parser.__getattr__(key)
        # Redefine things here
        normalized = option_parser._normalize_name(key)
        option_object = option_parser._options[normalized]
        if type is None:
            if not multiple and default is not None:
                type = default.__class__
            else:
                type = str

        frame = sys._getframe(0)
        options_file = frame.f_code.co_filename

        # Can be called directly, or through top level define() fn, in which
        # case, step up above that frame to look for real caller.
        if (
            frame.f_back.f_code.co_filename == options_file
            and frame.f_back.f_code.co_name == "define"
        ):
            frame = frame.f_back

        file_name = frame.f_back.f_code.co_filename
        if file_name == options_file:
            file_name = ""
        if type is None:
            if not multiple and default is not None:
                type = default.__class__
            else:
                type = str
        if group:
            group_name = group
        else:
            group_name = file_name

        option_object.default = default
        option_object.help = help
        option_object.type = type
        option_object.metavar = metavar
        option_object.multiple = multiple
        option_object.file_name = file_name
        option_object.group_name = group_name
        option_object.callback = callback
    except AttributeError:
        option_parser.define(
            name=key,
            default=default,
            help=help,
            metavar=metavar,
            type=type,
            multiple=multiple,
            group=group,
            callback=callback,
            *args,
            **kwargs
        )
    return
