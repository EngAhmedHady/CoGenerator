# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 15:23:37 2022

@author: Hady
"""


import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import matplotlib.patches as mpatch
from plotting import (ImageVisualization,
                      PointsInfoVisualization)
plt.rcParams.update({'font.size': 30})
plt.rcParams["text.usetex"] = True
plt.rcParams["font.family"] = "Times New Roman"
# from matplotlib.patches import Arc


class CoordinatesGenerator:
    # Initiating class parameters
    def __init__(self, lazer_info, bg = None):
        self.lazer_info = lazer_info
        # Leading  edge coordinates lower blade "Measured" [x,y,z]
        self.LazerLE_lower = lazer_info[0]
        # Trailing edge coordinates lower blade "Measured" [x,y,z]
        self.LazerTE_lower = lazer_info[1]
        # Leading  edge coordinates upper blade "Measured" [x,y,z]
        self.LazerLE_upper = lazer_info[2]
        # Lower profile cord info, # Chord line slope
        delta_y = lazer_info[0][1] - lazer_info[1][1]
        delta_x = lazer_info[0][0] - lazer_info[1][0]
        # AOA calculation
        if delta_x == 0:
            self.m1 = float('inf')  # to handle the vertical line case
        else:
            self.m1 = delta_y / delta_x

        self.a1 = lazer_info[0][1]-(self.m1*lazer_info[0][0])  # .... y-intercept
        self.Theta1 = np.arctan(self.m1)  # Chordline Angle to Horizontal (Rad)
        # Chordline Angle to Horizontal (AOA-Deg)
        self.DegTheta1 = self.Theta1*180/np.pi
        self.fig, self.ax = plt.subplots(figsize=(30, 15),
                                         gridspec_kw={'hspace': 0.05})
        self.bg = bg
        # Export input parmeters
        with open('Info.txt', 'w') as f:
            f.write(f"Leading  edge Lazer co. [x,y,z]: \t {lazer_info[0]}\n")
            f.write(f"Trailing edge Lazer co. [x,y,z]: \t {lazer_info[1]}\n")
            f.write(f"Leading  edge Lazer co. [x,y,z]: \t {lazer_info[2]}\n")

    def PointGenerator(self, StartingPoint, n_points, NPR,
                       Delta=[0, 0], V_Delta = None, slope=0, Dis=0,
                       PointType='BL', **kwargs):

        legend_loc = kwargs.get('legend_loc', 'best')
        legend_fsize = kwargs.get('legend_fsize', None)
        show_legend = kwargs.get('show_legend', True)
        line_width = kwargs.get('line_width', 1)
        points_size = kwargs.get('points_size', 8)
        points_display = kwargs.get('points_display', 'points')

        Points = [[StartingPoint[0], StartingPoint[1], self.LazerLE_lower[2]]]
        Points_X = [StartingPoint[0]]
        Points_Y = [StartingPoint[1]]
        i = 1
        Counter = 0
        points_color = kwargs.get('points_color', 'C{}'.format(Counter))

        if V_Delta is not None:
            D = 0
        nNPR = 0

        # NPR is the number of points per run, it can be constant number or
        # an array (Defulte = 6)
        # NPR array: [[Number of points per run, Till distance], .....]
        full_points_set = [Points[-1]]
        while i < n_points:
            k = 1
            Counter += 1
            if hasattr(NPR, "__len__"):
                if Dis >= NPR[nNPR][1]:
                    nNPR += 1
                NPPR = NPR[nNPR][0]
                # print(NPPR, Dis)
            else:
                NPPR = NPR
            while k < NPPR and i < n_points:
                if V_Delta is not None:
                    if Dis >= V_Delta[D][1]:
                        D += 1
                    Delta[0] = np.sqrt(V_Delta[D][0]**2/(slope**2+1))
                    Delta[1] = np.sqrt(V_Delta[D][0]**2-Delta[0]**2)
                    Dis += V_Delta[D][0]
                # print(round(Dis,2),i+1)
                Points.append([Points[k-1][0]+Delta[0],
                               Points[k-1][1]+Delta[1],
                               self.LazerLE_lower[2]])
                full_points_set.append(Points[-1])
                Points_X.append(Points[k-1][0]+Delta[0])
                Points_Y.append(Points[k-1][1]+Delta[1])
                k += 1
                i += 1
            np.array(Points)
            np.savetxt("Points"+str(Counter)+".txt", Points, delimiter="\t")
            # ======== Visualization Code ==========
            if points_display == 'line':
                if PointType == 'L':
                    self.ax.plot(Points_X, Points_Y, '-',
                                 label=f'Run {Counter}', color=points_color,
                                 lw=line_width)
                else:
                    self.ax.plot(Points_X, Points_Y, '-',
                                 label=f'Run {Counter}', lw=line_width,
                                 color=points_color)
            else:
                self.ax.plot(Points_X, Points_Y, 'x', label=f'Run {Counter}',
                             ms=points_size, mew=5)

            # self.ax.plot(Points_X,Points_Y,'o',label='Run '+str(Counter),
            # ms = points_size/2, color = 'orange')

            # ======== Visualization Code ==========
            Points = [Points[-1]]
            Points_X = [Points[-1][0]]
            Points_Y = [Points[-1][1]]

        # fullLength =
        fullLength = np.sqrt((StartingPoint[0]-Points_X[-1])**2+(StartingPoint[1]-Points_Y[-1])**2)
        print("Number of Runs = ",Counter, ", Distance from starting point = ",round(fullLength,5))
        print("starting point",StartingPoint,", last point = ", [Points_X[-1],Points_Y[-1]])

        if show_legend:
            self.ax.legend(loc = legend_loc, fontsize = legend_fsize);
        return full_points_set

    def LineGenerator(self, lineInfo, inclination = 'Vertical', NPR = 6,
                      LineShiftRepresentation = 'NormalToLine', invert = True, preview_lengths = True,
                      **kwargs):

        Origin = self.LazerLE_lower
        UpperLE = self.LazerLE_upper
        # LowerTE = self.LazerTE_lower
        # ``v_start``: starting point vertical distance from origine
        # ``line_shift``: line distance from origine (Normal distance in case of rotating 
        #                 the Coordinates otherwise it will be horizontal distance)
        # ``v_length``: Vertical length of the line
        # ``n_points``: Number of measuring points
        v_start, line_shift, v_length, n_points = lineInfo

        y_new = Origin[1]+v_start

        if inclination == 'Vertical':
            H_shifting = line_shift
            x_new = Origin[0] - H_shifting
            LineLength = v_length
            Theta = np.pi/2
        elif inclination == 'ParallelToLEs':
            print('Chord Slope = ', self.m1,
                  ',\nChord y-intercept = ', self.a1,
                  ',\nChordline Angle to Horizontal = ', self.DegTheta1)
            
            m3 = (Origin[1]-UpperLE[1])/(Origin[0]-UpperLE[0])
            Theta = np.arctan(m3)
            kwargs['Theta'] = Theta

            if LineShiftRepresentation == 'NormalToLine':
                H_shifting = line_shift / np.sin(Theta)
            elif LineShiftRepresentation == 'DistanseOnCord':
                H_shifting = line_shift*np.cos(self.Theta1)+line_shift*np.sin(abs(self.Theta1))/m3
            elif LineShiftRepresentation == 'HorizontalDistance':
                H_shifting = line_shift
            LineLength = v_length/np.sin(Theta)
            x_new = Origin[0]-H_shifting+v_start/m3

            # Finding the distance between the line and the inclined line
            a3 = y_new-m3*x_new
            x3 = (a3-self.a1)/(self.m1-m3)
            y3 = m3*x3+a3
            kwargs['x3'] = x3
            kwargs['y3'] = y3
            kwargs['a3'] = a3
            if m3 != 0:  m4 = -1/m3 # perpendicular line
            else: m4 = np.inf
            a4 = self.LazerLE_upper[1]-m4*self.LazerLE_upper[0]
            x4 = (a3-a4)/(m4-m3)
            y4 = m4*x4+a4
            kwargs['x4'] = x4
            kwargs['y4'] = y4
            kwargs['m4'] = a3

        Delta_l_new = LineLength/(n_points-1)

        self.ax = ImageVisualization(self.ax, self.lazer_info, BG =self.bg,
                                     reverse = invert, **kwargs)
        if preview_lengths:
            PointsInfoVisualization(self.ax, self.lazer_info, lineInfo, 
                                    H_shifting, self.DegTheta1, **kwargs)
        print(f"Delta_xy = {Delta_l_new} mm,\t line length  = {LineLength} mm")

        full_points_set = self.PointGenerator([x_new, y_new], n_points, NPR,
                                              Delta = [-(Delta_l_new*np.cos(Theta)), -(Delta_l_new*np.sin(Theta))],
                                              PointType='L', **kwargs)
        with open('Info.txt', 'a') as f:
            f.write(f"Starting point vertical distance from origine (mm):\t{v_start}\n")
            f.write("Line distance from origine (mm): \t"+str(line_shift));f.write('\n')
            f.write("Vertical length of the line (mm): \t"+str(v_length));f.write('\n')
            f.write("Number of measuring points: \t"+str(n_points));f.write('\n')
            f.write("Line inclination: \t"+str(inclination));f.write('\n')
            f.write("Line shift representation: \t"+str(LineShiftRepresentation));f.write('\n')
        return full_points_set

    def BLLineGenerator(self,CADinfo,lineInfo,Imageindex = 0, invert = True, NPR =6,**kwargs):
        Origin = self.LazerLE_lower
        LowerTE = self.LazerTE_lower
        starting_l = lineInfo[0]  # ..... starting distance from the surface
        Delta_l  = lineInfo[1]  # ....... [[Distance between each point (mm), distance from surface (mm)], .... ]
        n_points = lineInfo[2]

        MP = CADinfo[0]   # ...........Location on cord "Measuring point" (x/c)
        SVA = CADinfo[1]  # ...........Surface Normal angle to the cord
        SCD = CADinfo[2]  # ...........Surface to cord length

        Lazer_Cord_Length = np.sqrt((Origin[0]-LowerTE[0])**2+(Origin[1]-LowerTE[1])**2)

        # Point on the cord line
        Delta_x1 = ((1-MP)*Lazer_Cord_Length)*np.cos(self.Theta1)
        x1 = LowerTE[0]-Delta_x1
        Delta_y1 = ((1-MP)*Lazer_Cord_Length)*np.sin(self.Theta1)
        y1 = LowerTE[1]-Delta_y1

        Surface_V_toH_Angle = SVA + self.DegTheta1
        Theta2 = Surface_V_toH_Angle*math.pi/180
        print('Normal Angle (to vertical) = ', 90-Surface_V_toH_Angle, 'Deg')

        Delta_x2 = SCD*np.cos(Theta2)
        x2 = x1+Delta_x2

        Delta_y2 = SCD*np.sin(Theta2)
        y2 = y1+Delta_y2
        m2 = np.tan(Theta2)

        Starting_x = x2 + np.sqrt(starting_l**2/(m2**2+1))
        Starting_y = y2 + np.sqrt(starting_l**2-(Starting_x-x2)**2)

        fullLength = np.sqrt((Starting_x-x2)**2+(Starting_y-y2)**2)

        display_BL_calculation = kwargs.get('display_BL_calculation', False)
        points_size = kwargs.get('points_size', 8)
        line_width = kwargs.get('line_width', 1)

        if display_BL_calculation:
            self.ax.plot([Origin[0], LowerTE[0]], [Origin[1], LowerTE[1]], lw=line_width)
            arc1 = Arc(LowerTE,20, 20, theta1=180+self.DegTheta1, theta2=180, color = 'k', lw =line_width)
            self.ax.add_patch(arc1);
            # self.ax.text(LowerTE[0]-13 ,LowerTE[1]+0.75 , r'$\theta_1$', color = 'tab:red');
            self.ax.plot([x1,x1+15], [y1,y1], '--', color = 'k', lw =line_width)
            self.ax.plot([LowerTE[0],LowerTE[0]-15], [LowerTE[1],LowerTE[1]], '--', color = 'k', lw =line_width)

            a3 = y2 - (-1/m2)*x2
            y3 = (-1 / m2) * (x2 - 15) + a3
            y4 = (-1 / m2) * (x2 + 3) + a3
            self.ax.plot([x2-15, x2+3], [y3, y4], '--', lw=line_width,
                         color='tab:blue')
            rect = mpatch.Rectangle((x2, y2), 2, 2, facecolor='tab:blue',
                                    angle=270+Surface_V_toH_Angle)
            self.ax.add_patch(rect)

        full_points_set = self.PointGenerator([Starting_x, Starting_y],
                                              n_points, NPR, V_Delta=Delta_l,
                                              slope=m2, Dis=starting_l,
                                              **kwargs)

        if display_BL_calculation == True:
            self.ax.plot(x1, y1, 'x', color = 'tab:orange', ms = points_size, lw =line_width)
            arc1 = Arc((x1, y1),2, 2, color = 'k')
            self.ax.add_patch(arc1);

            self.ax.plot(x2, y2, 'x', color = 'tab:orange', ms = points_size, lw =line_width)
            arc1 = Arc((x2, y2),2, 2, color = 'k')
            self.ax.add_patch(arc1);
            self.ax.plot([x1,x2],[y1,y2],'-', lw =line_width, color = '#77dd77')

            arc1 = Arc((x1, y1), 20, 20, theta1=0, theta2=Surface_V_toH_Angle,
                       color='k', lw=line_width)
            arc2 = Arc((x1, y1), 35, 35, theta1=self.DegTheta1,
                       theta2=SVA+self.DegTheta1, color='k', lw=line_width)
            self.ax.add_patch(arc1)
            self.ax.add_patch(arc2)

        self.ax = ImageVisualization(self.ax, self.lazer_info, BG =self.bg,
                                     reverse = invert, **kwargs)

        print(f'Coordinate on the chordline: ({x1}, {y1})')
        print(f'Surface Point (x_p2,y_p2)= ({x2}, {y2})')
        print(f"starting distance from surface = {fullLength:0.2f}")

        with open('Info.txt', 'a') as f:
            f.write("Boundary layer line generator -  CAD info:\n")
            f.write(f"Location on cord 'Measuring point' (x/c):\t {MP}\n")
            f.write(f"Surface Normal angle to the cord: \t {SVA}\n")
            f.write(f"Surface to cord length (mm): \t {SCD}\n \n")
            f.write("Line info:\n")
            f.write(f"Starting distance from the surface (mm)\t{starting_l}\n")
            f.write(f"Distance between each point (mm): \t {Delta_l} \n")
            f.write(f"Number of measuring points: \t {n_points} \n")
            f.write(f"Normal Angle (prop rotating angle): \t {90-Surface_V_toH_Angle} \n")
            f.write(f"Number of points per run: \t {NPR} \n")

        return full_points_set
