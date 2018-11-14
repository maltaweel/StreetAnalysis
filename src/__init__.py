# -*- coding: utf-8 -*-
"""
/***************************************************************************
 StreetAnalysis
                                 A QGIS plugin
 Analysis for Streets
                             -------------------
        begin                : 2018-11-11
        copyright            : (C) 2018 by Mark Altaweel
        email                : maltaweel@ucl.ac.uk
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load StreetAnalysis class from file StreetAnalysis.

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    #
    from .StreetAnalysis import StreetAnalysis
    return StreetAnalysis(iface)
