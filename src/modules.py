import os
import logging
import datetime

from sqlalchemy import MetaData, create_engine, text, insert


# --> Initializing logging 
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s // %(message)s', filename='/opt/WorldAssetsData/logs/myapp.log', level=logging.INFO)
logger.debug('Module logging has been initialized!')

# --> Initializing sensetive data from .env
def initEnvironment():
    from dotenv import load_dotenv

    try:
        load_dotenv()
        DB_URL = os.getenv("DATABASE_URL")
        API_KEY = os.getenv("API_KEY")
        
        logger.debug('Hidden environment has been initialized from .env-file!')
        
        return DB_URL, API_KEY
    except Exception as err:
        logger.error(f'Caught error in initEnvironment(). Info about error --> {err}', exc_info=True)
        

# --> Initializing core-engine for sqlalchemy
def initEngine():
    DB_URL, API_KEY = initEnvironment()
    
    engine = create_engine(DB_URL, echo=True)
    metadata_obj = MetaData()
    metadata_obj.create_all(engine)
    metadata_obj.reflect(bind=engine)
    
    return engine, metadata_obj