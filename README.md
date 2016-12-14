django-monfhir
==============

Monfhir is a FHIR server based in Django. It uses a relational database to manage metadata 
and a MongDB to manage the FHIR documents.  MonFHIR is a JSON-only FHIR server at this time.
The system is designed this way for simplicity.  It supports OAuth2 when used in conjumction with
hhs_oauth_server.


Monfhir is in the very begining phases now. It is not ready for prime time at all. 

That said, here is how to install it.


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

