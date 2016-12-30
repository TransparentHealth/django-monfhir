from __future__ import absolute_import
from __future__ import unicode_literals
from django.conf import settings
from django.http import HttpResponse
from ..models import SupportedResourceType, MeKey
from collections import OrderedDict
from ..utils import operational_outcome_404, operational_outcome_error
import json
from .utils import check_access_interaction_and_resource_type
from pymongo import MongoClient
from bson.objectid import ObjectId


def read(request, resource_type, id):
    """Read FHIR Interaction"""
    # Example client use in curl:
    # curl  -X GET http://127.0.0.1:8000/fhir/Practitioner/1234

    interaction_type = 'read'
    # Check if this interaction type and resource type combo is allowed.
    deny = check_access_interaction_and_resource_type(resource_type,
                                                      interaction_type)
    if deny:
        # If not allowed, return a 4xx error.
        return deny

    mongodb_client_url = getattr(settings, 'MONGODB_CLIENT',
                                 'mongodb://localhost:27017/')
    client = MongoClient(mongodb_client_url, document_class=OrderedDict)

    db = client[getattr(settings, 'MONFHIR_DB',
                        'monfhir')]
    collection = db[resource_type]

    srt = SupportedResourceType.objects.get(resource_type=resource_type)
    # check if this is a self only call.
    if srt.self_only:
        if request.user.is_anonymous():
            # This is not allowed.
            return operational_outcome_error(
                "Anonymous requests are not permitted here.", 403)
        try:
            mk = MeKey.objects.get(user=request.user, resource_type=srt)
        except MeKey.DoesNotExist:
            return operational_outcome_error("A user key does not exist", 404)
        r = collection.find_one({"_id": ObjectId(str(mk.me_key))})
    else:
        r = collection.find_one({"_id": ObjectId(str(id))})

    # r = collection.find_one({"_id": ObjectId(str("585035895170aa59b7d2f68d")) })
    if r:
        r["id"] = str(r["_id"])
        del r["_id"]
        return HttpResponse(json.dumps(r, indent=4),
                            content_type="application/json+fhir")
    # else
    return operational_outcome_404(resource_type, id)
