
from loader.crawler import CrawlerPlugin, CrawlerLoader
from loader.crawler import CrawlerImplModel
import loader.script as script_loader

if __name__ == '__main__':
    ldr = CrawlerLoader()
    res = ldr('D:/zerosetall/VideoCrawlerEngine/plugin/bilibili.py')
    print(res)
