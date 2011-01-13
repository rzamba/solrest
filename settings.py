#!/usr/bin/python
# -*- coding: utf-8 -*-
SOLR_HOST = 'http://127.0.0.1:8983/solr/'
solr_rest_url_mapper = {"texto":"texto","materia":u"Matéria"}
solr_rest_content_fields = {
					"texto": 	{
								u"Matéria": 
									{
									"title":"required",
									"creator":"required",
									"contentGroup":"required",
									"created":"required",
									"site":"required",
									"url":"optional",
									"caption":"optional",
									"thumbnail":"optional",
									"issued":"optional",
									"modified":"optional",
									"section":"optional",
									"label":"optional",
									"editoria_principal_s":"optional"
									},
								"post": 
									{
									"title":"required",
									"creator":"required",
									"created":"required",
									"url":"optional",
									"caption":"optional",
									"thumbnail":"optional"
									}
								},
					"video": 	{
								"Integra": 
									{
									"title":"required",
									"creator":"required"
									}
								}
					}