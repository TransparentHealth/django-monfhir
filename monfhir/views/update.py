from __future__ import absolute_import
from __future__ import unicode_literals
from django.conf import settings
from collections import OrderedDict
from ..utils import (operational_outcome_405,
                     operational_outcome_success,
                     operational_outcome_error)
from django.views.decorators.csrf import csrf_exempt
import datetime
from ..models import SupportedResourceType, MeKey
from .utils import (check_access_interaction_and_resource_type,
                    check_for_json_and_schema)
from pymongo import MongoClient
from bson.objectid import ObjectId


@csrf_exempt
def update(request, resource_type, id):
    """Update FHIR Interaction"""
    # Example client use in curl:
    # curl -X PUT -H "Content-Type: application/json" --data @test.json
    # http://127.0.0.1:8000/fhir/Practitioner/12345

    interaction_type = 'update'
    # Check if this interaction type and resource type combo is allowed.
    deny = check_access_interaction_and_resource_type(
        resource_type, interaction_type)
    if deny:
        # If not allowed, return a 4xx error.
        return deny
    srt = SupportedResourceType.objects.get(resource_type=resource_type)

    mongodb_client_url = getattr(settings, 'MONGODB_CLIENT',
                                 'mongodb://localhost:27017/')
    client = MongoClient(mongodb_client_url, document_class=OrderedDict)
    db = client[getattr(settings, 'MONFHIR_DB',
                        'monfhir')]

    historical_collection_name = "%s_history" % (resource_type)
    collection = db[resource_type]
    historical_collection = db[historical_collection_name]
    # check if this is a self only call.
    if not srt.access_with_no_auth and request.user.is_anonymous():
        return operational_outcome_error(
                "Anonymous requests are not permitted here.", 403)

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
        u_id = ObjectId(str(mk.me_key))
    else:
        r = collection.find_one({"_id": ObjectId(str(id))})
        u_id = ObjectId(str(id))

    # If not r, then cannot update so return 405.
    if not r:
        return operational_outcome_405()

    # Make sure the request body is JSON and schema passes
    j = check_for_json_and_schema(srt, request.body, interaction_type)

    # check and set meta
    if 'meta' in r:
        if 'versionId' in r['meta']:
            if 'meta' not in r:
                j['meta']['versionId'] = r['meta']['versionId'] + 1
                r['meta']['versionId'] = j['meta']['versionId']

    else:
        r['meta'] = OrderedDict()
        r['meta']['versionId'] = 1
        j['meta']['versionId'] = 1

    j['meta'] = OrderedDict()
    j['meta']['versionId'] = r['meta']['versionId'] + 1
    j['meta']['lastUpdated'] = "%sZ" % (datetime.datetime.utcnow().isoformat())

    # Set the ID for the update
    j["_id"] = u_id
    if "id" in j:
        del j["id"]

    # store the old document in the historical collection
    r['fhir_id'] = u_id
    r['meta']['versionId'] = j['meta']['versionId']
    r['meta']['lastUpdated'] = j['meta']['lastUpdated']
    del r['_id']
    result = historical_collection.insert_one(r)

    result = collection.update_one({"_id": u_id}, {"$set": j})
    details = "Successfully updated resource %s to versionId %s." % (
        u_id, j['meta']['versionId'])
    location = request.build_absolute_uri() + "/_history/" + \
        str(j['meta']['versionId'])
    return operational_outcome_success(details, location)
