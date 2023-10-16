# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "SynImages",
    "author" : "Marcos Zacchi de Medeiros",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "3D View"
}

from . import operators, panels, properties, utils

def register():
    properties.register_properties()
    panels.register_panels()
    operators.register_operators()
    utils.register_utils()

def unregister():
    properties.unregister_properties()
    panels.unregister_panels()
    operators.unregister_operators()
    utils.unregister_utils()
