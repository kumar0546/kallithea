"""The application's model objects"""
import logging
from pylons_app.model import meta
log = logging.getLogger(__name__)

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    log.info("INITIALIZING DB MODELS")
    meta.Base.metadata.bind = engine
    #meta.Base2.metadata.bind = engine2

#THIS IS A TEST FOR EXECUTING SCRIPT AND LOAD PYLONS APPLICATION GLOBALS
#from paste.deploy import appconfig
#from pylons import config
#from sqlalchemy import engine_from_config
#from pylons_app.config.environment import load_environment
#
#conf = appconfig('config:development.ini', relative_to = './../../')
#load_environment(conf.global_conf, conf.local_conf)
#
#engine = engine_from_config(config, 'sqlalchemy.')
#init_model(engine)
# DO SOMETHING
