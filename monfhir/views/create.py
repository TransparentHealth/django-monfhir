from __future__ import absolute_import
from __future__ import unicode_literals
import sys
from ..models import SupportedResourceType
from collections import OrderedDict
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import uuid
from jsonschema import validate, ValidationError
import datetime
from pymongo import MongoClient
from ..utils import operational_outcome_error, operational_outcome_success
from .hello import hello
from .search import search
from .utils import check_access_interaction_and_resource_type, check_for_json_and_schema


@csrf_exempt
def create(request, resource_type):
    """Create FHIR Interaction"""
    # Example client use in curl:
    # curl -H "Content-Type: application/json" -X POST --data @test.json
    # http://127.0.0.1:8000/fhir/Practitioner
    interaction_type = 'create'

    deny = check_access_interaction_and_resource_type(
        resource_type, interaction_type)
    if deny:
        # If not allowed, return a 4xx error.
        return deny
    srt = SupportedResourceType.objects.get(resource_type=resource_type)

    # Catch all for GETs to re-direct to search if CREATE permission is valid
    if request.method == "GET":
        return search(request, resource_type)

    if request.method == 'POST':

        j = check_for_json_and_schema(srt, request.body, interaction_type)

        #write_to_mongo - TBD
        mongodb_client_url = getattr(settings, 'MONGODB_CLIENT',
                                     'mongodb://localhost:27017/')
        client = MongoClient(mongodb_client_url, document_class=OrderedDict)
        db = client[getattr(settings, 'MONFHIR_DB',
                            'monfhir')]

        historical_collection_name = "%s_history" % (resource_type)
        collection = db[resource_type]
        historical_collection = db[historical_collection_name]
        
        if not srt.access_with_no_auth and request.user.is_anonymous():
            return operational_outcome_error(
                "Anonymous requests are not permitted here.", 403)
    
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
            u_id = ObjectId(str(mk.me_key))
        else:
            # the id can be set by the client or the server, so just set it to
            # none for now.
            u_id = None
        # Set the Meta
        j['meta'] = OrderedDict()
        j['meta']['versionId'] = 1
        j['meta']['lastUpdated'] = "%sZ" % (
            datetime.datetime.utcnow().isoformat())

        result = collection.insert_one(j)
        fhir_id = result.inserted_id
        # Write the same record to the historical collection
        j['fhir_id'] = str(fhir_id)
        del j['_id']
        result = historical_collection.insert_one(j)

        details = "Successfully created %s resource with id %s and versionId %s." % (
            resource_type, str(fhir_id), j['meta']['versionId'])
        location = request.build_absolute_uri() + "/" + str(fhir_id) + "/_history/" + \
            str(j['meta']['versionId'])
        return operational_outcome_success(details, location)

    # This is something other than GET or POST (i.e. a  DELETE)
    if request.method not in ("GET", "POST"):
        od = OrderedDict()
        od['request_method'] = request.method
        od['interaction_type'] = "create"
        od['resource_type'] = resource_type
        od['note'] = "Perform an HTTP POST to this URL with the JSON resource as the request body."

        return HttpResponse(json.dumps(od, indent=4),
                            content_type="application/json")
