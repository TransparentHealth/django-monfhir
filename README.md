django-monfhir
==============

django-mongfhit is a "batteries included" FHIR server written in Django. 
This project is still in development an should be considered in alpha. Basic CRUD operations are functioning at this point.

Features include:


* **Document-Oriented Data Storage** - A Documented-oriented resource strorage - Monfhir uses the highly scaleable Document/NoSQL database MongoDB.
* **OAuth2** - Monfhir has out-of-the-box support for OAuth2. See the  hhs_oauth_server project on https://github.com/transparenthealth for more information.
* **"Me" Support** - Monfhir supports "me" use cases out-of-the-box.  Monfhir allows an authenticated user to access **only** his or her own information. For example: An patient accesses his or her own information (e.g. patient facing API or application. "Blue Button").
* **User Interface** - Monfhir can be configured/administered via the Django admin.
* **JSONSchema Support ** - Monfhir supports FHIR resource valiation via  JSONSchema. These schema valition rules can be applied as prerequisites to creating and/or updating FHIR resources on the seerver.
* **Pure JSON** - Monfhir supports JSON only (not XML). This feature results in a simpler system while still adhering to the FHIR specification.


MonFHIR can be configured via the Django admin web user interface.


MonFHIR is a JSON-only FHIR server at this time.
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

