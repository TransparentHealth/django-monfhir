from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class SupportedResourceType(models.Model):
    resource_type           = models.CharField(max_length=256, unique=True,
                                    db_index=True)
    json_schema             = models.TextField(max_length=5120, default="{}",
                                                help_text="{} indicates no schema.")
    database_name = models.CharField(max_length=256, default="",
                                     help_text="MongoDB Database Name")
    collection_name = models.CharField(max_length=256, default="",
                                       help_text="MongoDB Collection Name")
    self_only         = models.BooleanField(default=False, 
                                            help_text="This API is for a user only get their data")
    access_with_oauth2         = models.BooleanField(default=True, 
                                            help_text="Accessible via OAuth2")
    access_with_no_auth         = models.BooleanField(default=False, 
                                            help_text="Accessible without auth (for internal use cases)")
    get                = models.BooleanField(default=False, verbose_name="get",
                                                    help_text="FHIR Interaction Type")
    put                = models.BooleanField(default=False, verbose_name="put",
                                                  help_text="FHIR Interaction Type")
    create             = models.BooleanField(default=False, verbose_name="create",
                                                  help_text="FHIR Interaction Type")
    read               = models.BooleanField(default=False, verbose_name="read",
                                                  help_text="FHIR Interaction Type")
    vread              = models.BooleanField(default=False, verbose_name="vread",
                                                  help_text="FHIR Interaction Type")
    update             = models.BooleanField(default=False, verbose_name="update",
                                                  help_text="FHIR Interaction Type")
    delete             = models.BooleanField(default=False, verbose_name="delete",
                                                  help_text="FHIR Interaction Type")
    search             = models.BooleanField(default=False, verbose_name="search",
                                                  help_text="FHIR Interaction Type")
    history            = models.BooleanField(default=False, verbose_name="_history",
                                                  help_text="FHIR Interaction Type")

    # Python2 uses __unicode__(self):

    def __str__(self):
        return self.resource_type

    def get_supported_interaction_types(self):
        sit = []
        if self.get:
            sit.append(self._meta.get_field("get").verbose_name)
        if self.put:
            sit.append(self._meta.get_field("put").verbose_name)
        if self.create:
            sit.append(self._meta.get_field("create").verbose_name)
        if self.read:
            sit.append(self._meta.get_field("read").verbose_name)
        if self.vread:
            sit.append(self._meta.get_field("vread").verbose_name)
        if self.update:
            sit.append(self._meta.get_field("update").verbose_name)
        if self.delete:
            sit.append(self._meta.get_field("delete").verbose_name)
        if self.search:
            sit.append(self._meta.get_field("search").verbose_name)
        if self.history:
            sit.append(self._meta.get_field("history").verbose_name)
        return sit
