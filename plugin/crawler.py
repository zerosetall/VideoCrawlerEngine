

class Crawler:
    NAME = '__base__'
    VERSION = '0'
    AUTHOR = 'zerosetall'
    CREATE_AT = '2021-05-19'
    SUPPORTS = []
    RANKING = []

    def run(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError



