from __future__ import absolute_import
from __future__ import unicode_literals
from ..models import SupportedResourceType
from ..utils import operational_outcome_error
import json
import sys
from jsonschema import validate, ValidationError
from collections import OrderedDict


def check_access_interaction_and_resource_type(
        resource_type, interaction_type):
    try:
        rt = SupportedResourceType.objects.get(resource_type=resource_type)
        if interaction_type not in rt.get_supported_interaction_types():
            msg = "The interaction %s is not permitted on %s FHIR resources on this FHIR sever." % (
                interaction_type, resource_type)
            return operational_outcome_error(msg, 403)
    except SupportedResourceType.DoesNotExist:
        msg = "%s is not a supported resource type on this FHIR server." % (
            resource_type)
        return operational_outcome_error(msg, 400)
    return False


def check_for_json_and_schema(
        supportedResourceType,
        request_body,
        interaction_type):
        # interaction_type is 'create' or 'update'
        # Check if request body is JSON ------------------------
    try:
        j = json.loads(str(request_body.decode('utf-8')),
                       object_pairs_hook=OrderedDict)
        if not isinstance(j, type(OrderedDict())):
            return operational_outcome_error(
                "The request body did not contain a JSON object i.e. {}.", 400)
    except:
        return operational_outcome_error(
            "The request body did not contain valid JSON.", 400)

    if 'id' in j and interaction_type == 'create':
        return operational_outcome_error(
            "Create cannot have an id. Perhaps you meant to perform an update?", 400)
    # check json_schema is valid
    try:
        json_schema = json.loads(
            supportedResourceType.json_schema,
            object_pairs_hook=OrderedDict)

    except:
        print(sys.exc_info())
        return operational_outcome_error(
            "The JSON Schema on the server did not contain valid JSON. Please contact the system administrator",
            500)

    # Check JSON Schema
    if json_schema:
        try:
            validate(j, json_schema)
        except ValidationError:
            message = "JSON Schema Conformance Error. %s" % (
                str(sys.exc_info()[1][0]))
            return operational_outcome_error(message, 400)
    return j
