# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110 - 1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "pcloud",
    "author": "dustractor",
    "version": (1,0),
    "blender": (2,5,9),
    "api": 33333,
    "location": "Spacebar Menu > pcloud",
    "description":"Makes point cloud from living particles.",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "https://github.com/dustractor/pcloud",
    "category": "Add Mesh"}

import bpy

class PCLOUD_OT_convert(bpy.types.Operator):

    bl_idname = "pcloud.convert"
    bl_label = "pcloud: Point Cloud from Particles"

    @classmethod
    def poll(self,context):
        try:
            assert context.active_object.particle_systems.active != None
            has = True
        except (AssertionError,ValueError):
            has = False
        finally:
            return has

    def execute(self,context):
        living = lambda _:_.alive_state == "ALIVE"
        psys = context.object.particle_systems.active
        mesh = bpy.data.meshes.new("pcloud")
        verts = [p.location for p in filter(living,psys.particles)]
        mesh.from_pydata(verts,[],[])
        obj = bpy.data.objects.new("pcloud",object_data=mesh)
        bpy.context.scene.objects.link(obj)
        return {"FINISHED"}


def menu(self,context):
    self.layout.operator("pcloud.convert")

def register():
    bpy.utils.register_class(PCLOUD_OT_convert)
    bpy.types.VIEW3D_MT_object_specials.append(menu)

def unregister():
    bpy.types.VIEW3D_MT_object_specials.remove(menu)
    bpy.utils.unregister_class(PCLOUD_OT_convert)

if __name__ == "__main__":
    register()

