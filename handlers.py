#!/usr/bin/python
# -*- coding: utf-8 -*-
from piston.handler import BaseHandler
from minicms.solrest.solrconn import SolrSearch
from minicms.solrest.settings import *
from piston.utils import rc, require_mime, require_extended

class ContentsHandler(BaseHandler):
	allowed_methods = ('GET',)
	
	def read(self, request, contenSolrType, contentSolrSpecies, publisher=None):
		
		busca = SolrSearch()
		
		solrType = ""
		# Verifica se tipo de conteudo esta no urlMapper
		if solr_rest_url_mapper.has_key(contenSolrType):
			# Valida se tipo de conteudo existe
			solrType = solr_rest_url_mapper[contenSolrType]
			q = 'type:"%s"' % (solrType)
			results = busca.query(q,rows="1")
			if len(results) == 0:
				resp = rc.BAD_REQUEST
				resp.write(" %s - Tipo de conteudo inexistente no solr" % (solrType))
				return resp
		else:
			resp = rc.BAD_REQUEST
			resp.write(" %s - Tipo de conteudo inexistente no mapper" % (contenSolrType))
			return resp
			
		# Verifica se species de conteudo esta no urlMapper
		solrSpecies = ""
		if solr_rest_url_mapper.has_key(contenSolrType):
			# Valida se species de conteudo existe
			solrSpecies = solr_rest_url_mapper[contentSolrSpecies]
			q = 'species:"%s"' % (solrSpecies)
			results = busca.query(q,rows="1")
			if len(results) == 0:
				resp = rc.BAD_REQUEST
				resp.write("%s - Species de conteudo inexistente" % (solrSpecies))
				return resp
		else:
			resp = rc.BAD_REQUEST
			resp.write(" %s - Species de conteudo inexistente no mapper" % (contentSolrSpecies))
			return resp
		
		# obtem campo do dicionario de resultado
		dict_fields = solr_rest_content_fields[solrType][solrSpecies]
		
		# verifica se o publisher foi passado
		qpublisher = ""
		if (publisher != None and publisher != ""):
			# valida se o publisher existe
			q = 'publisher:"%s"' % (publisher)
			results = busca.query(q,rows="1")
			if len(results) == 0:
				resp = rc.BAD_REQUEST
				resp.write(" - Publisher inexistente")
				return resp
			qpublisher = 'AND publisher:"%s"' % (publisher)
		
		# verifica queryStrings
		rows = request.GET.get("rows","40")
		start = request.GET.get("start","0")
		sort = request.GET.get("sort","created desc")
		isIssued = request.GET.get("isIssued","")
		qisIssued = ""
		if isIssued != "":
			# ordenacao padrao para conteudos publicados
			if isIssued.upper() == "TRUE":
				sort = request.GET.get("sort","issued desc")
			isIssued = 'AND isIssued:%s' % (isIssued)
		
		# monta query
		q = 'type:"%s" AND species:"%s" %s %s' % (solrType,solrSpecies,isIssued,qpublisher)
		
		results = busca.query(q,sort=sort,rows=rows,start=start,indent="on")
        
		if len(results) == 0:
			resp = rc.NOT_FOUND
			resp.write (" - conteudo inexistente")
			return resp
			
		res = []
		for result in results:
			content = {}
			# Uri
			aidentifier = result["identifier"]
			identifier = aidentifier[7:len(aidentifier)]
			uricontent = "http://%s/restapi/item/%s" % (request.get_host(),identifier)
			content["uri"] = uricontent
			# percorre dict de campos e verifica se e requerido
			for solrField in dict_fields.keys():
				if dict_fields[solrField] == "required":
					content[solrField] = result[solrField]
				else:
					if result.has_key(solrField):
						content[solrField] = result[solrField]
			
			if len(results) >= 2:
				res.append(content)
			elif len(results) == 1:
				return content
				
		return res

class ContentItemHandler(BaseHandler):
	allowed_methods = ('GET',)
	
	def read(self, request,identifier):
		hostidentifier = "http://%s" % (identifier)
		q = 'identifier:"%s"' % (hostidentifier)
		busca = SolrSearch()
		results = busca.query(q,indent="on")

		if len(results) == 0:
			return rc.NOT_FOUND
		for result in results:
			aidentifier = result["identifier"]
			identifier = aidentifier[7:len(aidentifier)]
			uriContent = "http://%s/restapi/item/%s" % (request.get_host(),identifier)
			result["uri"] = uriContent
			return result