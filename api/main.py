# main.py
from fastapi import FastAPI, BackgroundTasks, Request
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings
from pydantic import BaseModel
from twisted.internet import reactor, defer
import multiprocessing
process = CrawlerProcess(get_project_settings())
runner = CrawlerRunner(get_project_settings())

app = FastAPI()

@defer.inlineCallbacks
def crawl(item_dict):
    print('age____:',item_dict['age'])
    yield runner.crawl('judge',id=item_dict['id'], name=item_dict['name'], age=item_dict['age'],
                  currentAddress=item_dict['currentAddress'], companyAddress=item_dict['companyAddress'],residenceAddress=item_dict['residenceAddress'],
                    fatherName=item_dict['fatherName'],motherName=item_dict['motherName'])
    reactor.stop()

class Item(BaseModel):
    id: str 
    name: str
    age: int
    currentAddress: str 
    companyAddress: str 
    residenceAddress: str 
    fatherName: str 
    motherName: str 

@app.get("/test")
async def root():
    return {"message": "Hello World"}

@app.post("/")
def proxy(request: Request, bt: BackgroundTasks):
    process.crawl('us_proxy')
    # Changed line below using Background tasks
    bt.add_task(process.start, stop_after_crawl=False)
    return {"crawled": True}

def scrape(item_dict):
    crawl(item_dict)
    reactor.run()

@app.post("/judge")
def judge(request: Request, bt: BackgroundTasks, item: Item):
    item_dict = item.model_dump()
    process = multiprocessing.Process(target=scrape, args=(item_dict,))
    # process.crawl('judge', id=item_dict['id'], name=item_dict['name'],
    #               currentAddress=item_dict['currentAddress'], companyAddress=item_dict['companyAddress'],residenceAddress=item_dict['residenceAddress'],
    #                 fatherName=item_dict['fatherName'],motherName=item_dict['motherName'])
    
    
    # Changed line below using Background tasks
    # bt.add_task(process.start, stop_after_crawl=False)
    process.start()
    process.join()
    return {"crawled": True}
    
    # process.close()