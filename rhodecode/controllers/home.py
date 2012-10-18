# -*- coding: utf-8 -*-
"""
    rhodecode.controllers.home
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Home controller for Rhodecode

    :created_on: Feb 18, 2010
    :author: marcink
    :copyright: (C) 2010-2012 Marcin Kuzminski <marcin@python-works.com>
    :license: GPLv3, see COPYING for more details.
"""
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging

from pylons import tmpl_context as c, request
from pylons.i18n.translation import _
from webob.exc import HTTPBadRequest

import rhodecode
from rhodecode.lib import helpers as h
from rhodecode.lib.ext_json import json
from rhodecode.lib.auth import LoginRequired
from rhodecode.lib.base import BaseController, render
from rhodecode.model.db import Repository
from sqlalchemy.sql.expression import func

log = logging.getLogger(__name__)


class HomeController(BaseController):

    @LoginRequired()
    def __before__(self):
        super(HomeController, self).__before__()

    def index(self):
        c.groups = self.scm_model.get_repos_groups()
        c.group = None

        if c.visual.lightweight_dashboard is False:
            c.repos_list = self.scm_model.get_repos()
        ## lightweight version of dashboard
        else:
            c.repos_list = Repository.query()\
                            .filter(Repository.group_id == None)\
                            .order_by(func.lower(Repository.repo_name))\
                            .all()
            repos_data = []
            total_records = len(c.repos_list)

            _tmpl_lookup = rhodecode.CONFIG['pylons.app_globals'].mako_lookup
            template = _tmpl_lookup.get_template('data_table/_dt_elements.html')

            quick_menu = lambda repo_name: (template.get_def("quick_menu")
                                            .render(repo_name, _=_, h=h, c=c))
            repo_lnk = lambda name, rtype, private, fork_of: (
                template.get_def("repo_name")
                .render(name, rtype, private, fork_of, short_name=False,
                        admin=False, _=_, h=h, c=c))
            rss_lnk = lambda repo_name: (template.get_def("rss")
                                           .render(repo_name, _=_, h=h, c=c))
            atom_lnk = lambda repo_name: (template.get_def("atom")
                                           .render(repo_name, _=_, h=h, c=c))

            for repo in c.repos_list:
                repos_data.append({
                    "menu": quick_menu(repo.repo_name),
                    "raw_name": repo.repo_name.lower(),
                    "name": repo_lnk(repo.repo_name, repo.repo_type,
                                     repo.private, repo.fork),
                    "last_change": h.age(repo.last_db_change),
                    "desc": repo.description,
                    "owner": h.person(repo.user.username),
                    "rss": rss_lnk(repo.repo_name),
                    "atom": atom_lnk(repo.repo_name),
                })

            c.data = json.dumps({
                "totalRecords": total_records,
                "startIndex": 0,
                "sort": "name",
                "dir": "asc",
                "records": repos_data
            })

        return render('/index.html')

    def repo_switcher(self):
        if request.is_xhr:
            all_repos = Repository.query().order_by(Repository.repo_name).all()
            c.repos_list = self.scm_model.get_repos(all_repos,
                                                    sort_key='name_sort',
                                                    simple=True)
            return render('/repo_switcher_list.html')
        else:
            return HTTPBadRequest()

    def branch_tag_switcher(self, repo_name):
        if request.is_xhr:
            c.rhodecode_db_repo = Repository.get_by_repo_name(c.repo_name)
            c.rhodecode_repo = c.rhodecode_db_repo.scm_instance
            return render('/switch_to_list.html')
        else:
            return HTTPBadRequest()
