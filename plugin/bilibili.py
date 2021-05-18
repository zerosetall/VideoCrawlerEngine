

from plugin.crawler import Crawler


class Bilibili(Crawler):
    NAME = 'bilibili'
    VERSION = '0.1'
    AUTHOR = 'ZSAIM'
    CREATE_AT = '2020-03-05'
    SUPPORTS = ['www.bilibili.com']
    RANKING = [116, 80, 74, 64, 32, 16]


