from django.shortcuts import render
from ..models import SupportedResourceType
from collections import OrderedDict
from django.http import HttpResponse
import json
from ..utils import operational_outcome_error
from .utils import check_access_interaction_and_resource_type


def search(request, resource_type):
    interaction_type = 'search'

    """Search Interaction"""
    # Example client use in curl:
    # curl -X GET  http://127.0.0.1:8000/fhir/Practitioner?foo=bar
    if request.method != 'GET':
        msg = "HTTP method %s not supported at this URL." % (request.method)
        return operational_outcome_error(msg, 400)

    # Move to fhir_io_mongo (Plugable back-end)
    od = OrderedDict()
    od['request_method'] = request.method
    od['interaction_type'] = "search"
    od['resource_type'] = resource_type
    od['search_params'] = request.GET
    od['note'] = "This is only a stub for future implementation"

    return HttpResponse(json.dumps(od, indent=4),
                        content_type="application/json")
