from tornado.web import URLSpec


class KeyflowWebApplicationHelper(object):
    @classmethod
    def add_handler_regex_to_handler_parameters(cls, handlers):
        #
        # Add the handler regex as a dict in the third tuple value. This dict will be passed to the handler's
        # initialize() method. We need this regex to be able to perform role lookups.
        #
        new_handlers = []
        for handler in handlers:
            if isinstance(handler, URLSpec):
                new_handlers.append(handler)
                continue

            handler_regex = handler[0]
            handler_class = handler[1]
            handler_init_arguments = handler[2] if len(handler) > 2 else {}
            handler_init_arguments["handler_regex"] = handler_regex
            new_handlers.append((handler_regex, handler_class, handler_init_arguments))
        return new_handlers
