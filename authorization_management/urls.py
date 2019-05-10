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

from django.conf.urls import url
from .authentication import login_with_bccr, consute_firma, sign_with_bccr
from django.contrib.auth.views import LoginView
from django.urls.base import reverse_lazy
from .views import home, logout_view

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r"^authenticate$", login_with_bccr, name="login_fd"),
    url(r"^check_sign$", consute_firma, name="consute_firma"),
    url(r"^sign/(?P<fileid>[0-9A-Za-z_\-]+)/$", sign_with_bccr, name="sign_fd"),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^accounts/login/$', LoginView.as_view(), {'redirect_to': reverse_lazy("dfva_upload")}, name='login'),
]