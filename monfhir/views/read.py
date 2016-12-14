from django.shortcuts import render
from ..models import SupportedResourceType
from django.shortcuts import render
from collections import OrderedDict
from ..utils import operational_outcome_404
from django.http import HttpResponse
import json
from .utils import check_access_interaction_and_resource_type
from pymongo import MongoClient
from bson.objectid import ObjectId

def read(request, resource_type, id):
    """Read FHIR Interaction"""
    # Example client use in curl:
    # curl  -X GET http://127.0.0.1:8000/fhir/Practitioner/1234
    
    interaction_type = 'read'
    #Check if this interaction type and resource type combo is allowed.
    deny = check_access_interaction_and_resource_type(resource_type,
                                                      interaction_type)
    if deny:
        #If not allowed, return a 4xx error.
        return deny
    
    srt = SupportedResourceType.objects.get(resource_type=resource_type)
    
    
    print(srt)
    client = MongoClient('mongodb://localhost:27017/', document_class=OrderedDict)
    db = client['monfhir']
    collection = db[resource_type]
    print(collection)
    
    r = collection.find_one({"_id": ObjectId(str("585035895170aa59b7d2f68d")) })
    if r:
        r["id"] = str(r["_id"])
        del r["_id"]
        return HttpResponse(json.dumps(r, indent=4),
                        content_type="application/json") 
    # else
    print("here")
    return operational_outcome_404(resource_type, id)

