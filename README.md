django-monfhir
==============

django-mongfhir is a FHIR server written in Django. 
This project is still in development. It should be considered alpha. 
CRUD interactions are functioning at this point.

Features include:


* **Document-Oriented Data Storage** - A Documented-oriented resource strorage - Monfhir uses the highly scaleable Document/NoSQL database MongoDB.
* **OAuth2** - Monfhir has out-of-the-box support for OAuth2. See the  hhs_oauth_server project on https://github.com/TransparentHealth/hhs_oauth_server for more information.
* **"Me" Support** - Monfhir supports "me" use cases out-of-the-box.  Monfhir allows an authenticated user to access **only** his or her own information. For example: An patient accesses his or her own information (e.g. patient facing API or application. "Blue Button").
* **User Interface** - Monfhir can be configured/administered via the Django admin.
* **JSONSchema Support** - Monfhir supports FHIR resource valiation via  JSONSchema. These schema valition rules can be applied as prerequisites to creating and/or updating FHIR resources on the seerver.
* **Pure JSON** - Monfhir supports JSON only (not XML). This feature results in a simpler system while still adhering to the FHIR specification.



Monfhir is in development.  Contributions/Pull requests welcome!


Installation
============

This is a reusable Django application so it should be attached to an existing Django project.

To install type the following in a shell:

    git clone https://github.com/TransparentHealth/django-monfhir.git
    pip install ./django-monfhir
    

Add "fhir" to your INSTALLED_APPS setting like this:

    INSTALLED_APPS = (
        ...
        'monfhir',
    )

Include the direct URLconf in your project urls.py like this:

    url(r'^monfhir/', include('monfhir.urls')),


If you want to use oauth2, you need to be running hhs_oauth_server and then inlcude the urls like so:


    url(r'^monfhir/', include('monfhir.oauth2_urls')),

Create your database tables by running migratre


    python manage.py migrate

You must add ther resoutrces and interaction types you wish to support.  This can be achieved via the Django admin.
You can alSupport a couple resource types by adding them in the admin or 
using the following command to activate `Practitioner` and `Organization`. 
(You can also do this sort of thing via the Django admin.)


    python manage.py loaddata [your download path]/django-monfhir/monfhir/fixtures/provider-directory-resources.json

Use the APIs. Visit http://127.0.0.1:8000/monfhir/hello to verify the installation.

