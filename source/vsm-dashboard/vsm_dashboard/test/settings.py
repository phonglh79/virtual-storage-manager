
# Copyright 2014 Intel Corporation, All Rights Reserved.

# Licensed under the Apache License, Version 2.0 (the"License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#  http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.

import os

from django.utils.translation import ugettext_lazy as _

from horizon.test.settings import *
from horizon.utils.secret_key import generate_or_read_from_file

from vsm_dashboard.exceptions import UNAUTHORIZED, RECOVERABLE, NOT_FOUND

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.abspath(os.path.join(TEST_DIR, ".."))

SECRET_KEY = generate_or_read_from_file(os.path.join(TEST_DIR,
                                                     '.secret_key_store'))
ROOT_URLCONF = 'vsm_dashboard.urls'
TEMPLATE_DIRS = (
    os.path.join(TEST_DIR, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS += (
    'vsm_dashboard.context_processors.openstack',
)

INSTALLED_APPS = (
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django.contrib.humanize',
    'django_nose',
    'openstack_auth',
    'compressor',
    'horizon',
    'vsm_dashboard',
    'vsm_dashboard.dashboards.project',
    'vsm_dashboard.dashboards.admin',
    'vsm_dashboard.dashboards.settings',
)

AUTHENTICATION_BACKENDS = ('openstack_auth.backend.KeystoneBackend',)

SITE_BRANDING = 'VSM'

HORIZON_CONFIG = {
    'dashboards': ('project', 'admin', 'settings'),
    'default_dashboard': 'project',
    "password_validator": {
        "regex": '^.{8,18}$',
        "help_text": _("Password must be between 8 and 18 characters.")
    },
    'user_home': None,
    'help_url': "dashboard/vsm",
    'exceptions': {'recoverable': RECOVERABLE,
                   'not_found': NOT_FOUND,
                   'unauthorized': UNAUTHORIZED},
}

# Set to True to allow users to upload images to glance via Horizon server.
# When enabled, a file form field will appear on the create image form.
# See documentation for deployment considerations.
HORIZON_IMAGES_ALLOW_UPLOAD = True

AVAILABLE_REGIONS = [
    ('http://localhost:5000/v2.0', 'local'),
    ('http://remote:5000/v2.0', 'remote'),
]

OPENSTACK_KEYSTONE_URL = "http://localhost:5000/v2.0"
OPENSTACK_KEYSTONE_DEFAULT_ROLE = "Member"

OPENSTACK_KEYSTONE_BACKEND = {
    'name': 'native',
    'can_edit_user': True,
    'can_edit_project': True
}

OPENSTACK_QUANTUM_NETWORK = {
    'enable_lb': True
}

OPENSTACK_HYPERVISOR_FEATURES = {
    'can_set_mount_point': True,

    # NOTE: as of Grizzly this is not yet supported in Nova so enabling this
    # setting will not do anything useful
    'can_encrypt_volumes': False
}

LOGGING['loggers']['vsm_dashboard'] = {
    'handlers': ['test'],
    'propagate': False,
}

NOSE_ARGS = ['--nocapture',
             '--nologcapture',
             '--cover-package=vsm_dashboard',
             '--cover-inclusive',
             '--all-modules']
