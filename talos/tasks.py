from celery import Celery
from .appstore import search_appstores
from .appfactory import DevelopmentConfig as Config

celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)

# The one task in celery, unfortunately cannot be put into another module
@celery.task
def search_appstores_task(term, country, jobid):
    from . import app
    from .models import db, dbJob, dbApp
    with app.app_context():
        # Gets the job object from the ID that is passed
        job = dbJob.query.get(jobid)
        results = search_appstores(term, country)

        # Each app in results is stored in the DB
        for result in results:
            newApp = dbApp(app_title=str(result.app_title),
                           store=result.store,
                           bundleid=result.bundleid,
                           description=result.description,
                           dev_name=result.dev_name,
                           dev_id=result.dev_id,
                           fullprice=result.fullprice,
                           versionnumber=result.versionnumber,
                           osreq=result.osreq,
                           latest_patch=str(result.latest_patch.date()),
                           content_rating=result.content_rating[0],
                           job_id=jobid)
            db.session.add(newApp)
            db.session.commit()

        # For clarity on the webpage the total amount of results is stored
        job.results = len(results)
        job.state = job.state.Finished
        db.session.add(job)
        db.session.commit()
    return  # No need to actually return anything
