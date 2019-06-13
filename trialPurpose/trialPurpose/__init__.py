# -*- coding: utf-8 -*-
"""
/***************************************************************************
 trialPurpose
                                 A QGIS plugin
 tp
                             -------------------
        begin                : 2019-04-20
        copyright            : (C) 2019 by sayali khade
        email                : sayalikhade@gmail.com
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
    """Load trialPurpose class from file trialPurpose.

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    #
    from .trial_purpose import trialPurpose
    return trialPurpose(iface)
