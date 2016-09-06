# Copyright 2016 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


from oslo_versionedobjects import fields

from glare.objects import base
from glare.objects.meta import attribute
from glare.objects.meta import fields as glare_fields
from glare.objects.meta import validators


Field = attribute.Attribute.init
Blob = attribute.BlobAttribute.init


class Image(base.BaseArtifact):

    fields = {
        'container_format': Field(fields.StringField,
                                  description="Image container format."),
        'disk_format': Field(fields.StringField,
                             validators=[
                                 validators.AllowedValues(['raw', 'vhd', 'vhdx',
                                 'vmdk', 'vdi', 'iso', 'qcow2',
                                 'aki', 'ari', 'ami'])],
                             description="Image disk format."),
        'min_ram': Field(fields.IntegerField, required_on_activate=False,
                         validators=[validators.MinNumberSize(0)],
                         description="Minimal RAM required to boot image."),
        'min_disk': Field(fields.IntegerField, required_on_activate=False,
                          validators=[validators.MinNumberSize(0)],
                          description="Minimal disk space "
                                      "required to boot image."),
        'image': Blob(max_blob_size=1073741824000,
                      required_on_activate=False,
                      description="Image binary."),
        'image_indirect_url': Field(fields.StringField,
                                    required_on_activate=False,
                                    description="URL where image is available "
                                                "for users by accepting EULA "
                                                "or some other form. It is "
                                                "used when it is not possible"
                                                "to upload image directly to "
                                                "Glare. F.e. some Windows "
                                                "cloud images requires EULA "
                                                "acceptance before download."),
        'cloud_user': Field(fields.StringField,
                            required_on_activate=False,
                            description="Default cloud user."),
    }

    @classmethod
    def get_type_name(cls):
        return "images"

    @classmethod
    def validate_activate(cls, context, af, values=None):
        blob_status = None
        if af.image:
            blob_status = af.image['status']
        if (blob_status != glare_fields.BlobFieldType.ACTIVE and
                not af.image_indirect_url):
            raise ValueError("Either image or image_indirect_url must be "
                             "specified for Binary Image.")
