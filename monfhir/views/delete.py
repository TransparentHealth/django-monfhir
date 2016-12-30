from __future__ import absolute_import
from __future__ import unicode_literals
from django.conf import settings
from ..models import SupportedResourceType
from collections import OrderedDict
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .utils import check_access_interaction_and_resource_type
from ..utils import operational_outcome_success
from pymongo import MongoClient
from bson.objectid import ObjectId

@csrf_exempt
def delete(request, resource_type, id):
    """Delete FHIR Interaction"""
    # Example client use in curl:
    # curl -X DELETE -H "Content-Type: application/json" --data @test.json
    # http://127.0.0.1:8000/fhir/Practitioner/12345
    interaction_type = 'delete'
    # Check if this interaction type and resource type combo is allowed.
    deny = check_access_interaction_and_resource_type(
        resource_type, interaction_type)
    if deny:
        # If not allowed, return a 4xx error.
        return deny
    #write_to_mongo - TBD
    mongodb_client_url = getattr(settings, 'MONGODB_CLIENT',
                                     'mongodb://localhost:27017/')
    client = MongoClient(mongodb_client_url, document_class=OrderedDict)
    db = client[getattr(settings, 'MONFHIR_DB',
                            'monfhir')]
    collection = db[resource_type]
    r = collection.delete_one({"_id": ObjectId(str(id))})
    print(r.deleted_count)
    if r.deleted_count >= 1:
        msg = "The %s resource with the id of %s was deleted." % (resource_type, id)
    else:
        msg = "The %s resource with the id of %s was not found so there was nothing to delete." % (resource_type, id)
    return operational_outcome_success(msg,204)

