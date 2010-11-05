#!/usr/bin/env python
# encoding: utf-8
# branches controller for pylons
# Copyright (C) 2009-2010 Marcin Kuzminski <marcin@python-works.com>
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; version 2
# of the License or (at your opinion) any later version of the license.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301, USA.
"""
Created on April 21, 2010
branches controller for pylons
@author: marcink
"""
from pylons import tmpl_context as c
from rhodecode.lib.auth import LoginRequired, HasRepoPermissionAnyDecorator
from rhodecode.lib.base import BaseController, render
from rhodecode.lib.utils import OrderedDict
from rhodecode.model.hg import HgModel
import logging
log = logging.getLogger(__name__)

class BranchesController(BaseController):
    
    @LoginRequired()
    @HasRepoPermissionAnyDecorator('repository.read', 'repository.write', 'repository.admin')
    def __before__(self):
        super(BranchesController, self).__before__()
    
    def index(self):
        hg_model = HgModel()
        c.repo_info = hg_model.get_repo(c.repo_name)
        c.repo_branches = OrderedDict()
        for name, hash_ in c.repo_info.branches.items():
            c.repo_branches[name] = c.repo_info.get_changeset(hash_)
                
        return render('branches/branches.html')
