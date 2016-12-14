#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from collections import OrderedDict
from django.http import HttpResponse
import json



def operational_outcome_404(resource_type,
                        resource_id,
                        severity="error"):
    response= OrderedDict()
    response['resourceType']= "OperationOutcome"
    text = OrderedDict()
    text['status'] = "generated"
    text['div'] = """<div><h1>Operation Outcome</h1><table border=\"0\"><tr>
        <td style=\"font-weight: bold;\">error</td><td>[]</td><td><pre>Resource %s/%s is not known</pre>
        </td>\n\t\t\t</tr>\n\t\t</table>\n\t""" % (resource_type, resource_id)
    response['text']=text
    issue = OrderedDict()
    issue['severity']=severity
    issue['details']="Resource %s/%s is not known" % (resource_type, resource_id)
    response['issue']=issue
    
    print("RESPONSE", response)
    r =  HttpResponse(json.dumps(response, indent = 4),
                        status=404, 
                        content_type="application/json")
    return r
    
def kickout_400(reason, status_code=400):
    response= OrderedDict()
    response["code"] = status_code
    response["errors"] = [reason,]
    return HttpResponse(json.dumps(response, indent = 4),
                        status=status_code,     
                        content_type="application/json")


def kickout_401(reason, status_code=401):
    response= OrderedDict()
    response["code"] = status_code
    response["errors"] = [reason,]
    return HttpResponse(json.dumps(response, indent = 4),
                        status=status_code,     
                        content_type="application/json")


def kickout_403(reason, status_code=403):
    response= OrderedDict()
    response["code"] = status_code
    response["errors"] = [reason,]
    return HttpResponse(json.dumps(response, indent = 4),
                        status=status_code,
                        content_type="application/json")


def kickout_404(reason, status_code=404):
    response= OrderedDict()
    response["code"] = status_code
    response["errors"] = [reason,]
    return HttpResponse(json.dumps(response, indent = 4),
                        status=status_code, 
                        content_type="application/json")


def kickout_500(reason, status_code=500):
    response= OrderedDict()
    response["code"] = status_code
    response["errors"] = [reason,]
    return HttpResponse(json.dumps(response, indent = 4),
                        status=status_code, 
                        content_type="application/json") 