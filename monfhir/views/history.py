from __future__ import absolute_import
from __future__ import unicode_literals
from django.conf import settings
from ..models import SupportedResourceType
from collections import OrderedDict
from django.http import HttpResponse
import json
from .utils import check_access_interaction_and_resource_type
from ..utils import operational_outcome_404
from pymongo import MongoClient
from bson.objectid import ObjectId


def history(request, resource_type, id):

    interaction_type = '_history'
    # Check if this interaction type and resource type combo is allowed.
    deny = check_access_interaction_and_resource_type(
        resource_type, interaction_type)
    if deny:
        # If not allowed, return a 4xx error.
        return deny

    """Read Search Interaction"""
    # Example client use in curl:
    # curl  -X GET http://127.0.0.1:8000/fhir/Practitioner/12345/_history
    if request.method != 'GET':
        msg = "HTTP method %s not supported at this URL." % (request.method)
        return operational_outcome_error(msg, 400)

    # testing direct response
    # return FHIR_BACKEND.history(request, resource_type, id)

    od = OrderedDict()
    od['request_method'] = request.method
    od['interaction_type'] = "_history"
    od['resource_type'] = resource_type
    od['id'] = id
    od['note'] = "This is only a stub for future implementation"

    return HttpResponse(json.dumps(od, indent=4),
                        content_type="application/json")


def vread(request, resource_type, id, vid):

    interaction_type = 'vread'
    # Check if this interaction type and resource type combo is allowed.
    deny = check_access_interaction_and_resource_type(
        resource_type, interaction_type)
    if deny:
        # If not allowed, return a 4xx error.
        return deny

    """VRead Interaction"""
    # Example client use in curl:
    # curl  -X GET http://127.0.0.1:8000/fhir/Practitioner/12345/_history/1
    if request.method != 'GET':
        msg = "HTTP method %s not supported at this URL." % (request.method)
        return operational_outcome_error(msg, 400)

    mongodb_client_url = getattr(settings, 'MONGODB_CLIENT',
                                 'mongodb://localhost:27017/')
    client = MongoClient(mongodb_client_url, document_class=OrderedDict)
    db = client[getattr(settings, 'MONFHIR_DB', 'monfhir')]

    historical_collection_name = "%s_history" % (resource_type)
    historical_collection = db[historical_collection_name]
    search = {"fhir_id": id, "meta.versionId": int(vid)}

    r = historical_collection.find_one(search)
    if r:
        r["id"] = str(r["fhir_id"])
        del r["_id"]
        del r["fhir_id"]
        return HttpResponse(json.dumps(r, indent=4),
                            content_type="application/json+fhir")
    # else
    return operational_outcome_404(resource_type, id)
