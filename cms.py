#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# python library for google earth plot
#
# author: Atsushi Sakai
#
# Copyright (c): 2015 Atsushi Sakai
#
# License : GPL Software License Agreement
import os
import sys
import simplekml
import pandas
import math
import argparse
from polycircles import polycircles


class googleearthplot:

    def __init__(self):
        self.kml = simplekml.Kml()


    def PlotPoints(self, lat, lon, label, description="", color="red", labelScale=1, time="", id=""):
        """
        Plot only label
        """
        pnt = self.kml.newpoint(name=label,
                                description=description
                                )
        pnt.coords = [(lat, lon)]
        pnt.style.labelstyle.color = self.GetColorObject(color)
        pnt.style.labelstyle.scale = labelScale
        pnt.timestamp.when = time

        print "[PlotPoint]" + label + ",lat:" + str(lat) + ",lon:" + str(lon) + ",time" + time

    def PlotLineChart(self, latList, lonList, heightList=[], name="", color="red", width=5):
        """
        Plot Line Chart
        """
        ls = self.kml.newlinestring(
            name=name,
            description=name
        )
        coords = []
        if len(heightList) == 0:
            for (lat, lon) in zip(latList, lonList):
                coords.append((lon, lat))
        else:
            for (lat, lon, height) in zip(latList, lonList, heightList):
                coords.append((lon, lat, height))

        ls.coords = coords
        ls.extrude = 1
        ls.altitudemode = simplekml.AltitudeMode.relativetoground
        ls.style.linestyle.width = width
        ls.style.linestyle.color = self.GetColorObject(color)

        print "[PlotLineChart]name:" + name + ",color:" + color + ",width:" + str(width)

    def PlotLabel(self, lat, lon, label, color="red", labelScale=1):
        """
        Plot only label
        """
        pnt = self.kml.newpoint(name=label)
        pnt.coords = [(lon, lat)]
        pnt.style.labelstyle.color = self.GetColorObject(color)
        pnt.style.labelstyle.scale = labelScale
        pnt.style.iconstyle.scale = 0  # hide icon
        print "[PlotLabel]" + label


    def PlotOverlayImg(self, filepath, name="ScreenOverlay", coords=[(18.410524, -33.903972), (18.411429, -33.904171),
                                      (18.411757, -33.902944), (18.410850, -33.902767)]):

        ground = self.kml.newgroundoverlay(name=name)
        ground.icon.href = filepath
        ground.gxlatlonquad.coords = coords

    def GetColorObject(self, color):
        valiableStr = "simplekml.Color." + color
        colorObj = eval(valiableStr)
        return colorObj

    def CalcLatFromMeter(self, shift):
        return shift / 111263.283  # degree

    def CalcLonFromMeter(self, shift, lon):
        const = 6378150 * math.cos(lon / 180 * math.pi) * 2 * math.pi / 360
        return shift / const  # degree

    def GenerateKMLFile(self, filepath="sample.kml"):
        """Generate KML File"""
        self.kml.save(filepath)
gep=googleearthplot()

parser = argparse.ArgumentParser(description='Process some kml.')
parser.add_argument('-image', default=False, action='store_true')
parser.add_argument('-radius', default=None, type = int, help='Radius of circle')
parser.add_argument('-triangle', default=False, action='store_true')
parser.add_argument('-circle', default=False, action='store_true')
parser.add_argument('-square', default=False, action='store_true')
parser.add_argument('-bubble', default=False, action='store_true')
parser.add_argument('-imgForBubble', default=False, action='store_true')
parser.add_argument('-labelForBubble', default=None, type = str, help='label if you want one for the bubble')



args = parser.parse_args()
if args.image:
    gep.PlotOverlayImg("C:\Users\Lenovo\Pictures\\tiger.jpg", name="image")
    gep.GenerateKMLFile(filepath="sample.kml")
    os.startfile("sample.kml")
    sys.exit()

if args.triangle:
    kml = gep.kml
    pol = kml.newpolygon(name="Triangle",
                         outerboundaryis=[(1, 0), (0, 0),
                                          (0, 1),(1,0)])
    pol.style.polystyle.color = \
        simplekml.Color.changealphaint(200, simplekml.Color.green)
    gep.GenerateKMLFile(filepath="sample.kml")
    os.startfile("sample.kml")
    sys.exit()

if args.circle:
    radius=200
    if args.radius:
        radius=args.radius
    polycircle = polycircles.Polycircle(latitude=18.43348,
                                        longitude=-33.98985,
                                        radius=radius,
                                        number_of_vertices=36)
    kml = gep.kml
    pol = kml.newpolygon(name="Circle",
                         outerboundaryis=polycircle.to_kml())
    pol.style.polystyle.color = \
        simplekml.Color.changealphaint(200, simplekml.Color.green)
    gep.GenerateKMLFile(filepath="sample.kml")
    os.startfile("sample.kml")
    sys.exit()
if args.square:
    kml = gep.kml
    pol = kml.newpolygon(name="Square",
                         outerboundaryis=[(18, -33), (19, -33),
                                          (19, -32),(18,-32)])
    pol.style.polystyle.color = \
        simplekml.Color.changealphaint(200, simplekml.Color.green)

    gep.GenerateKMLFile(filepath="sample.kml")
    os.startfile("sample.kml")
    sys.exit()

if args.bubble:
    kml = gep.kml
    outerboundary =[(18, -33), (19, -33), (19, -32), (18, -32)]
    pol = kml.newpolygon(name="Square",
                         outerboundaryis=outerboundary)
    pol.style.polystyle.color = \
        simplekml.Color.changealphaint(200, simplekml.Color.green)
    if args.labelForBubble:
        gep.PlotLabel(lat=-32.5,lon=18.5, label=args.labelForBubble)
    if args.imgForBubble:
        gep.PlotOverlayImg("C:\Users\Lenovo\Pictures\\tiger.jpg", name="image", coords=outerboundary)
    gep.GenerateKMLFile(filepath="sample.kml")
    os.startfile("sample.kml")
    sys.exit()








