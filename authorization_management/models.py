# encoding: utf-8

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''
@date: 08/10/2018
@author: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from django.core.validators import RegexValidator
from dateutil.relativedelta import relativedelta


identification_validator = RegexValidator(
    r'"(^[1|5]\d{11}$)|(^\d{2}-\d{4}-\d{4}$)"',
    message=_("Debe tener el formato 08-8888-8888 para nacionales o 500000000000 o 100000000000"))


class AuthenticateDataRequest(models.Model):
    identification = models.CharField(
        max_length=15, validators=[identification_validator],
        help_text="Debe tener el formato 08-8888-8888 para nacionales o 500000000000 o 100000000000"
    )
    expiration_datetime = models.DateTimeField()
    # '%Y-%m-%d %H:%M:%S',   es decir  '2006-10-25 14:30:59'
    request_datetime = models.DateTimeField(
        help_text="""'%Y-%m-%d %H:%M:%S',   es decir  '2006-10-25 14:30:59'""")
    status_text = models.CharField(max_length=256, default='n/d')
    status = models.IntegerField(default=0)
    received_notification = models.BooleanField(default=False)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "AuthenticateDataRequest(%s)  " % (
            self.identification,
        )

    @property
    def left_time(self):
        now = timezone.now()
        ttime = relativedelta(self.expiration_datetime, now)
        return "%d:%d:%d" % (ttime.hours, ttime.minutes, ttime.seconds)

    class Meta:
        ordering = ('-request_datetime',)
        permissions = (
            ("view_authenticatedatarequest",
             "Can see available Authenticate Data Request"),
        )
