from pysolr import Solr
from minicms.solrest.settings import *

class SolrSearch:
   
    def query(self,q,**kwargs):
        conn = Solr(SOLR_HOST)
        results = conn.search(q,**kwargs)
        return results
