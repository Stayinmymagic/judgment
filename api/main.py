from fastapi import FastAPI, BackgroundTasks, Request
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())
app = FastAPI()

@app.get("/test")
async def root():
    return {"message": "Hello World"}

@app.post("/")
def scrapy(request: Request, bt: BackgroundTasks):
    process.crawl('us_proxy')
    # Changed line below using Background tasks
    bt.add_task(process.start, stop_after_crawl=False)
    return {"crawled": True}