# This file is part of libigl, a simple c++ geometry processing library.
#
# Copyright (C) 2017 Sebastian Koch <s.koch@tu-berlin.de> and Daniele Panozzo <daniele.panozzo@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.
import sys, os

# Add the igl library to the modules search path
sys.path.insert(0, os.getcwd() + "/../")
import pyigl as igl

from shared import TUTORIAL_SHARED_PATH, check_dependencies

dependencies = ["glfw"]
check_dependencies(dependencies)


viewer = igl.viewer.Viewer()

# Quad mesh generated from conjugate field
VQC = igl.eigen.MatrixXd()
FQC = igl.eigen.MatrixXi()
FQCtri = igl.eigen.MatrixXi()
PQC0 = igl.eigen.MatrixXd()
PQC1 = igl.eigen.MatrixXd()
PQC2 = igl.eigen.MatrixXd()
PQC3 = igl.eigen.MatrixXd()

# Planarized quad mesh
VQCplan = igl.eigen.MatrixXd()
FQCtriplan = igl.eigen.MatrixXi()
PQC0plan = igl.eigen.MatrixXd()
PQC1plan = igl.eigen.MatrixXd()
PQC2plan = igl.eigen.MatrixXd()
PQC3plan = igl.eigen.MatrixXd()


def key_down(viewer, key, modifier):
    if key == ord('1'):
        # Draw the triangulated quad mesh
        viewer.data.set_mesh(VQC, FQCtri)

        # Assign a color to each quad that corresponds to its planarity
        planarity = igl.eigen.MatrixXd()
        igl.quad_planarity(VQC, FQC, planarity)
        Ct = igl.eigen.MatrixXd()
        igl.jet(planarity, 0, 0.01, Ct)
        C = igl.eigen.MatrixXd(FQCtri.rows(), 3)
        C.setTopRows(Ct.rows(), Ct)
        C.setBottomRows(Ct.rows(), Ct)
        viewer.data.set_colors(C)

        # Plot a line for each edge of the quad mesh
        viewer.data.add_edges(PQC0, PQC1, igl.eigen.MatrixXd([[0, 0, 0]]))
        viewer.data.add_edges(PQC1, PQC2, igl.eigen.MatrixXd([[0, 0, 0]]))
        viewer.data.add_edges(PQC2, PQC3, igl.eigen.MatrixXd([[0, 0, 0]]))
        viewer.data.add_edges(PQC3, PQC0, igl.eigen.MatrixXd([[0, 0, 0]]))

    elif key == ord('2'):
        # Draw the planar quad mesh
        viewer.data.set_mesh(VQCplan, FQCtri)

        # Assign a color to each quad that corresponds to its planarity
        planarity = igl.eigen.MatrixXd()
        igl.quad_planarity(VQCplan, FQC, planarity)
        Ct = igl.eigen.MatrixXd()
        igl.jet(planarity, 0, 0.01, Ct)
        C = igl.eigen.MatrixXd(FQCtri.rows(), 3)
        C.setTopRows(Ct.rows(), Ct)
        C.setBottomRows(Ct.rows(), Ct)
        viewer.data.set_colors(C)

        # Plot a line for each edge of the quad mesh
        viewer.data.add_edges(PQC0plan, PQC1plan, igl.eigen.MatrixXd([[0, 0, 0]]))
        viewer.data.add_edges(PQC1plan, PQC2plan, igl.eigen.MatrixXd([[0, 0, 0]]))
        viewer.data.add_edges(PQC2plan, PQC3plan, igl.eigen.MatrixXd([[0, 0, 0]]))
        viewer.data.add_edges(PQC3plan, PQC0plan, igl.eigen.MatrixXd([[0, 0, 0]]))

    else:
        return False

    return True


# Load a quad mesh generated by a conjugate field
igl.readOFF(TUTORIAL_SHARED_PATH + "inspired_mesh_quads_Conjugate.off", VQC, FQC)

# Convert it to a triangle mesh
FQCtri.resize(2 * FQC.rows(), 3)

FQCtriUpper = igl.eigen.MatrixXi(FQC.rows(), 3)
FQCtriLower = igl.eigen.MatrixXi(FQC.rows(), 3)

FQCtriUpper.setCol(0, FQC.col(0))
FQCtriUpper.setCol(1, FQC.col(1))
FQCtriUpper.setCol(2, FQC.col(2))
FQCtriLower.setCol(0, FQC.col(2))
FQCtriLower.setCol(1, FQC.col(3))
FQCtriLower.setCol(2, FQC.col(0))

FQCtri.setTopRows(FQCtriUpper.rows(), FQCtriUpper)
FQCtri.setBottomRows(FQCtriLower.rows(), FQCtriLower)

igl.slice(VQC, FQC.col(0), 1, PQC0)
igl.slice(VQC, FQC.col(1), 1, PQC1)
igl.slice(VQC, FQC.col(2), 1, PQC2)
igl.slice(VQC, FQC.col(3), 1, PQC3)

# Planarize it
igl.planarize_quad_mesh(VQC, FQC, 100, 0.005, VQCplan)

# Convert the planarized mesh to triangles
igl.slice(VQCplan, FQC.col(0), 1, PQC0plan)
igl.slice(VQCplan, FQC.col(1), 1, PQC1plan)
igl.slice(VQCplan, FQC.col(2), 1, PQC2plan)
igl.slice(VQCplan, FQC.col(3), 1, PQC3plan)

# Launch the viewer
key_down(viewer, ord('2'), 0)
viewer.core.invert_normals = True
viewer.core.show_lines = False
viewer.callback_key_down = key_down
viewer.launch()
