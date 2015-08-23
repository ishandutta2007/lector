#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Lector: ocrarea.py

    Copyright (C) 2011-2014 Davide Setti, Zdenko Podobný

    This program is released under the GNU GPLv2
"""
#pylint: disable-msg=C0103

from PyQt5.QtGui import QPen, QFont
from PyQt5.QtCore import Qt, QObject
from PyQt5.QtWidgets import (QApplication as QA, QMenu, QGraphicsItem,
                             QGraphicsTextItem, QGraphicsRectItem)


class OcrArea(QGraphicsRectItem):
    ## static data
    resizeBorder = .0

    def __init__(self, pos, size, type_, parent = None, scene = None,
                 areaBorder = 2, index = 0, textSize = 50):
        QGraphicsRectItem.__init__(self, 0, 0, size.width(),
                                         size.height(), parent, scene)
        self.setPos(pos)

        #self.setAcceptedMouseButtons(QtCore.Qt.NoButton)
        self.setFlags(QGraphicsItem.ItemIsMovable |
            QGraphicsItem.ItemIsFocusable |
            QGraphicsItem.ItemIsSelectable)

        ## set index label
        self.text = QGraphicsTextItem("%d" % index, self)
        self.setTextSize(textSize)

        ## TODO: How to create constants for the type?
        ## (such as constants in Qt) (enum?)
        self.type = type_

        pen = QPen(self.color, areaBorder, Qt.SolidLine,
                   Qt.RoundCap, Qt.RoundJoin)
        self.setPen(pen)
        self.setAcceptsHoverEvents(True)

        # self.text.setFlag(QtGui.QGraphicsItem.ItemIgnoresTransformations)
        # needed for the emission of a signal
        self.newEvent = QObject()
        self.newEvent.area = self

    def setIndex(self, idx):
        self.text.setPlainText(str(idx))

    def setTextSize(self, size):
        font = QFont()
        font.setPointSizeF(size)
        self.text.setFont(font)

    def contextMenuEvent(self, event):
        menu = QMenu()
        removeAction = menu.addAction(QA.translate('QOcrWidget', "Remove"))
        #Action = menu.addAction(self.scene().tr("Remove"))
        menu.addSeparator()
        textAction = menu.addAction(QA.translate('QOcrWidget', "Text"))
        graphicsAction = menu.addAction(QA.translate('QOcrWidget', "Graphics"))

        ## verification of the type of the selection and
        ## setting a check box near the type that is in use
        textAction.setCheckable(True)
        graphicsAction.setCheckable(True)

        if self.type == 1:
            textAction.setChecked(True)
        elif self.type == 2:
            graphicsAction.setChecked(True)

        selectedAction = menu.exec_(event.screenPos())

        if selectedAction == removeAction:
            self.scene().removeArea(self)
        elif selectedAction == textAction:
            self.type = 1
        elif selectedAction == graphicsAction:
            self.type = 2

    # when the area is selected the signal "isClicked()" is raised
    def mousePressEvent(self, event):
        # TODO: check this!
        self.newEvent.emit("isClicked()")
        QGraphicsRectItem.mousePressEvent(self, event)

    ## type property
    def _setType(self, type_):
        self.__type = type_

        if self.__type == 1:
            self.color = Qt.darkGreen
        else:  ## TODO: else -> elif ... + else raise exception
            self.color = Qt.blue

        self.text.setDefaultTextColor(self.color)

        pen = self.pen()
        pen.setColor(self.color)
        self.setPen(pen)

    def _type(self):
        return self.__type

    type = property(fget=_type, fset=_setType)


