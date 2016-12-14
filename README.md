django-monfhir
==============

Monfhir is a FHIR server based in Django. It uses a relational database to manage metadata 
and a MongDB for FHIR resource storage.  MonFHIR is a JSON-only FHIR server at this time.
It supports OAuth2 when used in conjunction with
https://github.com/TransparentHealth/hhs_oauth_server

Monfhir is in the very begining phases now and  is not ready for prime time at all. 
Contributions are welcome! 


Installation
============

This is a reusable Django application so it should be attached to an existing Django project.

To install type the following in a shell:

    git clone https://github.com/transparenthealth/django-monfhir.git
    pip install ./django-monfhir
    

Add "fhir" to your INSTALLED_APPS setting like this:

    INSTALLED_APPS = (
        ...
        'monfhir',
    )

Include the direct URLconf in your project urls.py like this:

    url(r'^monfhir/', include('monfhir.urls')),


Create your database tables.


    python manage.py migrate

Support a couple resource types by adding them in the admin or 
using the following command to activate `Practitioner` and `Organization`.


    python manage.py loaddata [your download path]/django-monfhir/monfhir/fixtures/provider-directory-resources.json


Use the APIs. Visit http://127.0.0.1:8000/monfhir/hello to verify the installation.

