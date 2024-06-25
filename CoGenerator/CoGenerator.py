# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 15:23:37 2022

@author: Hady
"""

import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import matplotlib.patches as mpatch
plt.rcParams.update({'font.size': 30})
plt.rcParams["text.usetex"] = True
plt.rcParams["font.family"] = "Times New Roman"
# from matplotlib.patches import Arc


class CoordinatesGenerator:
    # Initiating class parameters
    def __init__(self, LAZERinfo, Images):
        # Leading  edge coordinates lower blade "Measured" [x,y,z]
        self.LazerLE_lower = LAZERinfo[0]
        # Trailing edge coordinates lower blade "Measured" [x,y,z]
        self.LazerTE_lower = LAZERinfo[1]
        # Leading  edge coordinates upper blade "Measured" [x,y,z]
        self.LazerLE_upper = LAZERinfo[2]
        # Lower profile cord info, # Chord line slope
        delta_y = LAZERinfo[0][1] - LAZERinfo[1][1]
        delta_x = LAZERinfo[0][0] - LAZERinfo[1][0]
        if delta_x == 0:
            self.m1 = float('inf')  # to handle the vertical line case
        else:
            self.m1 = delta_y / delta_x

        self.a1 = LAZERinfo[0][1]-(self.m1*LAZERinfo[0][0])  # .... y-intercept
        self.Theta1 = np.arctan(self.m1)  # Chordline Angle to Horizontal (Rad)
        # Chordline Angle to Horizontal (Deg)
        self.DegTheta1 = self.Theta1*180/np.pi
        self.fig, self.ax = plt.subplots(figsize=(30, 15),
                                         gridspec_kw={'hspace': 0.05})
        self.images = Images
        # Export input parmeters
        with open('Info.txt', 'w') as f:
            f.write(f"Leading  edge Lazer co. [x,y,z]: \t {LAZERinfo[0]}\n")
            f.write(f"Trailing edge Lazer co. [x,y,z]: \t {LAZERinfo[1]}\n")
            f.write(f"Leading  edge Lazer co. [x,y,z]: \t {LAZERinfo[2]}\n")

    def ImageVisualization(self, Imageindex, reverse=True, **kwargs):
        imagePath = self.images[Imageindex][0]
        ImageSize = self.images[Imageindex][1]
        img = plt.imread(imagePath)
        points_size = kwargs.get('points_size', 8)

        x = [self.LazerLE_lower[0],
             self.LazerTE_lower[0],
             self.LazerLE_upper[0]]

        y = [self.LazerLE_lower[1],
             self.LazerTE_lower[1],
             self.LazerLE_upper[1]]

        self.ax.plot(x, y, 'rx', label='_Hidden', ms=points_size)
        self.ax.imshow(img, extent=[x[0]-ImageSize[0], x[1]+ImageSize[1],
                                    y[0]+ImageSize[2], y[1]-ImageSize[3]])
        # grid
        self.ax.grid(True, which='major', color='#D8D8D8', linestyle='-',
                     alpha=0.2, lw=1.5)
        self.ax.minorticks_on()
        self.ax.grid(True, which='minor', color='#D8D8D8', linestyle='-',
                     alpha=0.1)
        if reverse:
            self.ax.invert_xaxis()
        self.ax.invert_yaxis()

        self.ax.set_xticks(np.arange(round(x[0]-100), round(x[0]+260),
                                     step=20))

        xticks = self.ax.get_xticks()
        labelsX = [round(item - x[0]) for item in xticks]
        self.ax.set_xticklabels(labelsX)

        self.ax.set_yticks(np.arange(round(y[0]-100), round(y[0]+260),
                                     step=20))

        yticks = self.ax.get_yticks()
        labelsY = [round(item - y[0]) for item in yticks]
        self.ax.set_yticklabels(labelsY)

        figxlim = kwargs.get('figxlim', [0, 0])
        figylim = kwargs.get('figylim', [0, 0])
        if abs(figxlim[0] - figxlim[1]) > 0:
            self.ax.set_xlim([round(x[0]+figxlim[0]), round(x[0]+figxlim[1])])

        if abs(figylim[0] - figylim[1]) > 0:
            self.ax.set_ylim([round(y[0]+figylim[0]), round(y[0]+figylim[1])])

        # self.ax.set_xlabel(r'$x$[mm]')
        # self.ax.set_ylabel(r'$y$[mm]')
        self.ax.set_xlabel(r'$X$[mm]')
        self.ax.set_ylabel(r'$Y$[mm]')
        BGcolor = kwargs.get('BGcolor', 'white')
        self.ax.set_facecolor(BGcolor)

    def PointsInfoVisualization(self, lineInfo, H_shifting, **kwargs):
        Origin = self.LazerLE_lower
        V_Start = lineInfo[0]  # starting point vertical distance from origine
        V_Length = lineInfo[2]  # Vertical length of the line
        LowerTE = self.LazerTE_lower

        arrows_color = kwargs.get('arrows_color', 'w')
        text_color = kwargs.get('text_color', 'w')
        dim_size = kwargs.get('dim_size', 30)
        x = ((Origin[0]+Origin[0]-3*H_shifting+12)/2)

        self.ax.plot([Origin[0]-2, x-5], [Origin[1]+0.1, Origin[1]+0.1], '-',
                     label='_Hidden', lw=1, color=arrows_color)

        self.ax.annotate('', xy=(Origin[0], Origin[1]), color=arrows_color,
                         xytext=(x, Origin[1]),
                         arrowprops=dict(arrowstyle='<|-|>', lw=1,
                                         color=arrows_color,
                                         mutation_aspect=0.5))
        # H_shifting
        H_shift_dim_size = kwargs.get('H_shift_dim_size', dim_size)
        self.ax.text(((Origin[0]+Origin[0]-H_shifting)/2),
                     Origin[1]-5, str(round(H_shifting, 2)),
                     {'ha': 'center', 'va': 'center'}, size=H_shift_dim_size,
                     color=text_color)

        # self.ax.plot([((Origin[0]+Origin[0]-3*H_shifting+12)/2),((Origin[0]+Origin[0]-3*H_shifting+12)/2)],
        #          [Origin[1],Origin[1]+V_Start],'w-', ms = 10,label='_Hidden')

        self.ax.plot([x-5, x+5], [Origin[1]+V_Start, Origin[1]+V_Start], '-',
                     label='_Hidden', lw=1, color=arrows_color)
        self.ax.annotate('', xy=(x, Origin[1]-2), color=arrows_color,
                         xytext=(x, Origin[1]+V_Start+1.5),
                         arrowprops=dict(arrowstyle='<|-|>', lw=1,
                                         color=arrows_color, mutation_aspect=4,
                                         mutation_scale=10))

        # Distance from starting point
        strt_dist_dim_size = kwargs.get('strt_dist_dim_size', dim_size)
        self.ax.text(((Origin[0]+Origin[0]-3*H_shifting+5)/2)-2,
                     ((Origin[1]+Origin[1]+V_Start)/2), f'{V_Start:0.0f}',
                     {'ha': 'center', 'va': 'center'}, size=strt_dist_dim_size,
                     color=text_color, rotation=90)

    # self.ax.plot([((Origin[0]+Origin[0]-3*H_shifting+12)/2),((Origin[0]+Origin[0]-3*H_shifting+12)/2)],
    # [Origin[1],Origin[1]-(V_Length-V_Start)],'w-', ms = 10,label='_Hidden')
        self.ax.plot([x-5, x+5], [Origin[1]-(V_Length-V_Start),
                                  Origin[1]-(V_Length-V_Start)],
                     '-', label='_Hidden', lw=1, color=arrows_color)

        self.ax.annotate('', xy=(x, Origin[1]+2), color=arrows_color,
                         xytext=(x, Origin[1]-(V_Length-V_Start)-1.5),
                         arrowprops=dict(arrowstyle='<|-|>', lw=1,
                                         color=arrows_color, mutation_aspect=4,
                                         mutation_scale=10))

        ngtiv_dim_size = kwargs.get('ngtiv_dim_size', dim_size)
        self.ax.text(((Origin[0]+Origin[0]-3*H_shifting+5)/2)-2,
                     ((Origin[1]+Origin[1]-(V_Length-V_Start))/2),
                     f'{V_Length-V_Start:0.0f}',
                     {'ha': 'center', 'va': 'center'}, size=ngtiv_dim_size,
                     color=text_color, rotation=90)

        x3 = kwargs.get('x3', None)
        y3 = kwargs.get('y3', None)
        Theta = kwargs.get('Theta', None)
        x4 = kwargs.get('x4', None)
        y4 = kwargs.get('y4', None)
        if x3 is not None:
            self.ax.plot([LowerTE[0], x3], [LowerTE[1], y3], 'r--', ms=10,
                         label='_Hidden')

            # Chord extension length
            Chord_ext_dim_size = kwargs.get('Chord_ext_dim_size', dim_size)
            L3 = np.sqrt((Origin[0]-x3)**2+(Origin[1]-y3)**2)
            self.ax.text(((Origin[0]+x3)/2)+2, ((Origin[1]+y3)/2)+2,
                         f"{L3:0.2f}", {'ha': 'center', 'va': 'center'},
                         size=Chord_ext_dim_size, color='r',
                         rotation=self.DegTheta1)

            p4 = np.array([x4, y4])
            L4 = np.linalg.norm(self.LazerLE_upper[:2] - p4)
    # L4 = np.sqrt((self.LazerLE_upper[0]-x4)**2+(self.LazerLE_upper[1]-y4)**2)
            self.ax.plot([Origin[0], self.LazerLE_upper[0], x4],
                         [Origin[1], self.LazerLE_upper[1], y4],
                         'y--', ms=5, linewidth=0.5, label='_Hidden')

            DegTheta3 = Theta*180/np.pi
            rect = mpatch.Rectangle((x4, y4), 2, 2, facecolor='y',
                                    angle=270+DegTheta3)
            self.ax.add_patch(rect)

            self.ax.text(((self.LazerLE_upper[0]+x4)/2)+2,
                         ((self.LazerLE_upper[1]+y4)/2)+2, str(round(L4, 2)),
                         {'ha': 'center', 'va': 'center'}, size=30, color='y',
                         rotation=270+DegTheta3)

    def PointsInfoVisualizationPaper(self, lineInfo, H_shifting):
        Origin = self.LazerLE_lower
        V_Start = lineInfo[0]   # starting point vertical distance from origine
        V_Length = lineInfo[2]  # Vertical length of the line

        self.ax.plot([Origin[0]-2, Origin[0]-H_shifting-10],
                     [Origin[1], Origin[1]], 'w-', label='_Hidden', lw=0.5)

        self.ax.annotate('', xy=(Origin[0], Origin[1]), color='w',
                         xytext=(Origin[0]-H_shifting, Origin[1]),
                         arrowprops=dict(arrowstyle='<|-|>', lw=1, color='w',
                                         mutation_aspect=0.5))

        self.ax.text(((Origin[0]+Origin[0]-H_shifting)/2),
                     Origin[1]-3, str(round(H_shifting, 2)),
                     {'ha': 'center', 'va': 'center'}, size=5, color='w')

        # self.ax.plot([((Origin[0]+Origin[0]-3*H_shifting+12)/2),((Origin[0]+Origin[0]-3*H_shifting+12)/2)],
        #          [Origin[1],Origin[1]+V_Start],'w-', ms = 10,label='_Hidden')
        x = ((Origin[0]+Origin[0]-3*H_shifting+12)/2)
        self.ax.plot([x-5, x+5], [Origin[1]+V_Start, Origin[1]+V_Start], 'w-',
                     label='_Hidden', lw=0.5)

        self.ax.annotate('', xy=(x, Origin[1]-2), color='w',
                         xytext=(x, Origin[1]+V_Start+1.5),
                         arrowprops=dict(arrowstyle='<|-|>', lw=1, color='w',
                                         mutation_aspect=4, mutation_scale=10))

        self.ax.text(((Origin[0]+Origin[0]-3*H_shifting+5)/2)-2,
                     ((Origin[1]+Origin[1]+V_Start)/2), str(V_Start),
                     {'ha': 'center', 'va': 'center'}, size=20, color='w',
                     rotation=90)

        # self.ax.plot([((Origin[0]+Origin[0]-3*H_shifting+12)/2),((Origin[0]+Origin[0]-3*H_shifting+12)/2)],
    # [Origin[1],Origin[1]-(V_Length-V_Start)],'w-', ms = 10,label='_Hidden')
        self.ax.plot([x-5, x+5], [Origin[1]-(V_Length-V_Start),
                                  Origin[1]-(V_Length-V_Start)],
                     'w-', label='_Hidden', lw=0.5)

        self.ax.annotate('', xy=(x, Origin[1]+2), color='w',
                         xytext=(x, Origin[1]-(V_Length-V_Start)-1.5),
                         arrowprops=dict(arrowstyle='<|-|>', lw=1, color='w',
                                         mutation_aspect=4, mutation_scale=10))

        self.ax.text(((Origin[0]+Origin[0]-3*H_shifting+5)/2)-2,
                     ((Origin[1]+Origin[1]-(V_Length-V_Start))/2),
                     f'{V_Length-V_Start}', {'ha': 'center', 'va': 'center'},
                     size=20, color='w', rotation=90)

        self.ax.xaxis.set_ticks(np.arange(170, 430, 20))
        self.ax.yaxis.set_ticks(np.arange(-257.5, -57.5, 20))

    def PointGenerator(self, StartingPoint, n_points, NPR,
                       Delta=[0, 0], V_Delta=[], slope=0, Dis=0,
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

        if V_Delta != []:
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
                if V_Delta != []:
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

    def LineGenerator(self, lineInfo, inclination = 'Vertical', Imageindex = 0 , NPR = 6,
                      LineShiftRepresentation = 'NormalToLine', invert = True, preview_lengths = True,
                      **kwargs):

        Origin = self.LazerLE_lower
        UpperLE = self.LazerLE_upper
        # LowerTE = self.LazerTE_lower

        V_Start = lineInfo[0]         # starting point vertical distance from origine
        line_Shift = lineInfo[1]      # line distance from origine (Normal distance in case of rotating the Coordinates otherwise it will be horizontal distance)
        V_Length = lineInfo[2]        # Vertical length of the line
        n_points = lineInfo[3]        # Number of measuring points

        y_new = Origin[1]+V_Start

        if inclination == 'Vertical':
            H_shifting = line_Shift
            x_new = Origin[0] - H_shifting
            LineLength = V_Length
            Theta = math.pi/2
        elif inclination == 'ParallelToLEs':
            print('Chord Solpe = ',self.m1, ',\nChord y-intercept = ',self.a1, ',\nChordline Angle to Horizontal = ', self.DegTheta1)
            m3 = (Origin[1]-UpperLE[1])/(Origin[0]-UpperLE[0])
            Theta = np.arctan(m3)
            kwargs['Theta'] = Theta

            if LineShiftRepresentation == 'NormalToLine':
                H_shifting = line_Shift / np.sin(Theta)
            elif LineShiftRepresentation == 'DistanseOnCord':
                H_shifting = line_Shift*np.cos(self.Theta1)+line_Shift*np.sin(abs(self.Theta1))/m3
            elif LineShiftRepresentation == 'HorizontalDistance':
                H_shifting = line_Shift
            LineLength = V_Length/np.sin(Theta)
            x_new = Origin[0]-H_shifting+V_Start/m3

            # Finding the distance between the line and the inclined line
            a3 = y_new-m3*x_new
            x3 = (a3-self.a1)/(self.m1-m3)
            y3 = m3*x3+a3
            kwargs['x3'] = x3
            kwargs['y3'] = y3

            m4 = -1/m3
            a4 = self.LazerLE_upper[1]-m4*self.LazerLE_upper[0]
            x4 = (a3-a4)/(m4-m3)
            y4 = m4*x4+a4
            kwargs['x4'] = x4
            kwargs['y4'] = y4

        Delta_l_new = LineLength/(n_points-1)

        self.ImageVisualization(Imageindex, reverse=invert, **kwargs)
        if preview_lengths:
            self.PointsInfoVisualization(lineInfo, H_shifting, **kwargs)
        print(f"Delta_xy = {Delta_l_new} mm,\t line length  = {LineLength} mm")

        full_points_set = self.PointGenerator([x_new, y_new], n_points, NPR,
                                              Delta = [-(Delta_l_new*np.cos(Theta)), -(Delta_l_new*np.sin(Theta))],
                                              PointType='L', **kwargs)
        with open('Info.txt', 'a') as f:
            f.write("Starting point vertical distance from origine (mm): \t"+str(V_Start));f.write('\n')
            f.write("Line distance from origine (mm): \t"+str(line_Shift));f.write('\n')
            f.write("Vertical length of the line (mm): \t"+str(V_Length));f.write('\n')
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

        self.ImageVisualization(Imageindex, reverse=invert, **kwargs)

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
