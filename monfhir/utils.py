#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from collections import OrderedDict
from django.http import HttpResponse
import json


def operational_outcome_success(details,
                                location,
                                status=200,
                                severity="information"):
    response = OrderedDict()
    response['resourceType'] = "OperationOutcome"
    text = OrderedDict()
    text['status'] = "generated"
    text['div'] = """<div><h1>Operation Outcome</h1><table border=\"0\"><tr>
        <td style=\"font-weight: bold;\">information</td><td>[]</td><td><pre>%s</pre>
        </td>\n\t\t\t</tr>\n\t\t</table>\n\t""" % (details)
    response['text'] = text
    issue = OrderedDict()
    issue['severity'] = severity
    issue['code'] = "informational"
    issue['details'] = details
    response['issue'] = issue
    r = HttpResponse(json.dumps(response, indent=4),
                     status=status,
                     content_type="application/json+fhir")
    r['Location'] = location
    return r


def operational_outcome(status,
                        details,
                        severity="error"):
    response = OrderedDict()
    response['resourceType'] = "OperationOutcome"
    text = OrderedDict()
    text['status'] = "generated"
    text['div'] = """<div><h1>Operation Outcome</h1><table border=\"0\"><tr>
        <td style=\"font-weight: bold;\">error</td><td>[]</td><td><pre>%s</pre>
        </td>\n\t\t\t</tr>\n\t\t</table>\n\t""" % (details)
    response['text'] = text
    issue = OrderedDict()
    issue['severity'] = severity
    issue['details'] = details
    response['issue'] = issue
    r = HttpResponse(json.dumps(response, indent=4),
                     status=status,
                     content_type="application/json+fhir")
    return r


def operational_outcome_404(resource_type,
                            resource_id,
                            severity="error"):
    response = OrderedDict()
    response['resourceType'] = "OperationOutcome"
    text = OrderedDict()
    text['status'] = "generated"
    text['div'] = """<div><h1>Operation Outcome</h1><table border=\"0\"><tr>
        <td style=\"font-weight: bold;\">error</td><td>[]</td><td><pre>Resource %s/%s is not known</pre>
        </td>\n\t\t\t</tr>\n\t\t</table>\n\t""" % (resource_type, resource_id)
    response['text'] = text
    issue = OrderedDict()
    issue['severity'] = severity
    issue[
        'details'] = "Resource %s/%s is not known" % (resource_type, resource_id)
    response['issue'] = issue

    print("RESPONSE", response)
    r = HttpResponse(json.dumps(response, indent=4),
                     status=404,
                     content_type="application/json+fhir")
    return r


def operational_outcome_404_details(resource_type,
                                    resource_id,
                                    details,
                                    severity="error"):
    response = OrderedDict()
    response['resourceType'] = "OperationOutcome"
    text = OrderedDict()
    text['status'] = "generated"
    text['div'] = """<div><h1>Operation Outcome</h1><table border=\"0\"><tr>
        <td style=\"font-weight: bold;\">error</td><td>[]</td><td><pre>Resource %s/%s is not known</pre>
        </td>\n\t\t\t</tr>\n\t\t</table>\n\t""" % (resource_type, resource_id)
    response['text'] = text
    issue = OrderedDict()
    issue['severity'] = severity
    issue['details'] = details
    response['issue'] = issue

    print("RESPONSE", response)
    r = HttpResponse(json.dumps(response, indent=4),
                     status=404,
                     content_type="application/json+fhir")
    return r


def operational_outcome_405(severity="error"):
    response = OrderedDict()
    response['resourceType'] = "OperationOutcome"
    text = OrderedDict()
    text['status'] = "generated"
    text['div'] = """<div><h1>Operation Outcome</h1><table border=\"0\"><tr>
        <td style=\"font-weight: bold;\">error</td><td>[]</td><td><pre>The resource did
        not exist prior to the update, and the server does not allow client defined ids.</pre>
        </td>\n\t\t\t</tr>\n\t\t</table>\n\t"""
    response['text'] = text
    issue = OrderedDict()
    issue['severity'] = severity
    issue['details'] = "The resource did not exist prior to the update, and the server does not allow client defined ids."
    response['issue'] = issue

    r = HttpResponse(json.dumps(response, indent=4),
                     status=405,
                     content_type="application/json+fhir")
    return r


def operational_outcome_error(details, status_code=400):
    response = OrderedDict()
    response['resourceType'] = "OperationOutcome"
    text = OrderedDict()
    text['status'] = "generated"
    text['div'] = """<div><h1>Operation Outcome</h1><table border=\"0\"><tr>
        <td style=\"font-weight: bold;\">error</td><td>[]</td><td><pre>%s</pre>
        </td>\n\t\t\t</tr>\n\t\t</table>\n\t""" % (details)
    response['text'] = text
    issue = OrderedDict()
    issue['severity'] = "error"
    issue['details'] = details
    response['issue'] = issue

    r = HttpResponse(json.dumps(response, indent=4),
                     status=status_code,
                     content_type="application/json+fhir")
    return r
