class Factory(object):
    def __init__(self, config):
        self.config = config

    def __parse(self):
        pass

    def __make(self, t_class, **args):
        return t_class(**args)


class UtteranceFactory(Factory):
    def __init__(self):
        super.__init__()

    def __parse(self, u):
        # this is where a lot of actual work is done
        # the question still is where we put actual corpus-specific function pointers
        # which are pretty necessary if we want to keep our modules small

        return self.config["functions"]["u_parsing"](u)

    def make_utterance(self, u):
            return self.__make(Utterance, self.__parse(u))

