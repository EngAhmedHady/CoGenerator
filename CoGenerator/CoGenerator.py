# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 15:23:37 2022

@author: Hady
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
# import matplotlib.patches as mpatch
from plotting import (ImageVisualization,
                      PointsInfoVisualization,
                      display_BL_calcu_data)
from supportfunc import (IntersectionPoint, inclined_line,
                         cascade_inc_line_plotting_pram, 
                         generatNPRlist, dy_list_generator)

plt.rcParams.update({'font.size': 30})
plt.rcParams["text.usetex"] = True
plt.rcParams["font.family"] = "Times New Roman"
# from matplotlib.patches import Arc

class BCOLOR:  # For coloring the text in terminal
    """
    A class to represent ANSI escape sequences for coloring terminal text.
    This class provides various ANSI escape codes to color and style text in
    terminal output.

    Supported formats:
        - BGOKBLUE: background blue
        - BGOKCYAN: background cyan
        - OKCYAN: cyan text
        - BGOKGREEN: background green
        - OKGREEN: green text
        - WARNING: yellow background (warning)
        - FAIL: yellow text (fail)
        - ITALIC: italic text
        - UNDERLINE: underlined text
        - ENDC: reset all attributes.
    """
    BGOKBLUE = '\033[44m'
    BGOKCYAN = '\033[46m'
    OKCYAN = '\033[36m'
    BGOKGREEN = '\033[42m'
    OKGREEN = '\033[32m'
    WARNING = '\033[43m'
    FAIL = '\033[33m'
    ENDC = '\033[0m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'

class CoordinatesGenerator:
    # Initiating class parameters
    def __init__(self, lazer_info, bg = None):
        self.lazer_info = lazer_info
        # ``origin_LE``: Measured Leading edge coordinates main blade [x,y,z]
        # ``origin_TE``: Measured Trailing edge coordinates main blade [x,y,z]
        # ``profile2_LE``: Measured Leading edge coordinates of other blade

        origin_LE, origin_TE, profile2_LE = lazer_info

        # main profile cord info, # Chord line slope
        delta_y = origin_LE[1] - origin_TE[1]
        delta_x = origin_LE[0] - origin_TE[0]

        # AOA calculation
        if delta_x == 0:
            self.m1 = float('inf')  # to handle the vertical line case
        else:
            self.m1 = delta_y / delta_x

        self.chord_len = np.sqrt((delta_x)**2+(delta_y)**2)

        self.a1 = origin_LE[1]-(self.m1*origin_LE[0])  # .... y-intercept
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

    def PointGenerator(self, starting_point, n_points, NPR,
                       delta=[0, 0], slope=None, Dis=0,
                       PointType='BL', **kwargs):

        origin_LE, _, _ = self.lazer_info
        line_width = kwargs.get('line_width', 1)
        points_size = kwargs.get('points_size', 8)
        points_width = kwargs.get('points_width', 1)
        legend_loc = kwargs.get('legend_loc', 'best')
        show_legend = kwargs.get('show_legend', True)
        legend_fsize = kwargs.get('legend_fsize', None)
        points_display = kwargs.get('points_display', 'points')
        dy_list = kwargs.get('dy_list', None)

        points = [[starting_point[0], starting_point[1], origin_LE[2]]]
        full_points_set = [points[-1]]

        points_X = [starting_point[0]]
        points_Y = [starting_point[1]]
        Counter = 0
        points_color = kwargs.get('points_color', 'C{}'.format(Counter))
        i = 1  # Points counter
        D = 0  # Distance group counter
        # NPR is the number of points per run, it can be constant number or
        # an array (Defulte = 6)
        # NPR array: [[Number of points per run, Till distance], .....]
        
        if dy_list is not None:
            # In case of variable vertical gap betwwen points
            dy_new_list = dy_list_generator(Dis, dy_list)
        else:
            dy_new_list = delta[1]*np.ones(n_points-1)
            
        # print(dy_new_list)

        if PointType == 'BL':
            # In case of changing the coordinate system (BL for example)
            dx = [np.sqrt(dy**2/(slope**2+1)) for dy in dy_new_list]
            dy = [np.sqrt(dy**2-dx[i]**2) for i, dy in enumerate(dy_new_list)]
        else:
            if slope is not None:
                dx = [dy/slope for dy in dy_new_list]
            else:
                dx = delta[0]*np.ones(n_points-1)
            dy = dy_new_list
            
        if not hasattr(NPR, "__len__"):
            NPR = generatNPRlist(n_points, NPR, Dis, dy_new_list)
            
        # print(NPR)
        
        NPPR = NPR[0][0]
        while i < n_points:
            k = 1
            Counter += 1
            while k < NPPR and i < n_points:
                D += 1 if Dis > NPR[D][1] else 0
                NPPR = NPR[D][0]
                # print(D, NPR[D][1], f'{Dis:0.2f}', dy_new_list[i-1])
                Dis += abs(dy_new_list[i-1])
                
                points.append([points[k-1][0]+dx[i-1],
                               points[k-1][1]+dy[i-1],
                               origin_LE[2]])
                full_points_set.append(points[-1])
                points_X.append(points[k-1][0]+dx[i-1])
                points_Y.append(points[k-1][1]+dy[i-1])

                k += 1
                i += 1
            np.array(points)
            np.savetxt(f"Points{Counter}.txt", points, delimiter="\t")
            # ======== Visualization Code ==========
            if points_display == 'line':
                if PointType == 'L':
                    self.ax.plot(points_X, points_Y, '-',
                                 label=f'Run {Counter}', color=points_color,
                                 lw=line_width)
                else:
                    self.ax.plot(points_X, points_Y, '-',
                                 label=f'Run {Counter}', lw=line_width,
                                 color=points_color)
            else:
                self.ax.plot(points_X, points_Y, 'x', label=f'Run {Counter}',
                             ms=points_size, mew=points_width)

            points = [points[-1]]
            points_X = [points[-1][0]]
            points_Y = [points[-1][1]]

        # fullLength =
        fullLength = np.sqrt((starting_point[0]-points_X[-1])**2+(starting_point[1]-points_Y[-1])**2)
        print(f"Number of Runs = {Counter}", f", Distance from starting point = {fullLength:0.5f}")
        print(f"x_distance = {starting_point[0]-points_X[-1]:0.3f}", 
              f", y_distance = {starting_point[1]-points_Y[-1]:0.3f}")
        # print("Number of Runs = ",Counter, ", Distance from starting point = ",round(fullLength,5))
        print("starting point:",starting_point,", last point: ", [points_X[-1], points_Y[-1]])

        if show_legend:
            self.ax.legend(loc = legend_loc, fontsize = legend_fsize);
        return full_points_set

    def LineGenerator(self, lineInfo, inclination = 'Vertical', NPR = 6,
                      LineShiftRepresentation = 'NormalToLine',
                      invert = True, preview_lengths = True,
                      **kwargs):

        # ``v_start``: starting point vertical distance from origine
        # ``line_shift``: line distance from origine (Normal distance in case of rotating
        #                 the Coordinates otherwise it will be horizontal distance)
        # ``v_length``: Vertical length of the line
        # ``n_points``: Number of measuring points

        origin_LE, Origin_TE , profile2_LE = self.lazer_info
        o_x,o_y,_ = origin_LE
        v_start, line_shift, v_length, n_points = lineInfo
        print('Chordline Angle to Horizontal = ', self.DegTheta1,
              ',\nChord length = ', self.chord_len )
        kwargs['chord_len'] = self.chord_len
        kwargs['inclind_line'] = False
        y_new = o_y + v_start
        # x-coordinate of the chord line extention on the travers line
        x3 = None
        m3 = None

        if inclination == 'Vertical':
            H_shifting = line_shift
            x_new = o_x - H_shifting
            LineLength = v_length
            Theta = np.pi / 2
        elif inclination == 'ParallelToLEs':
            kwargs['inclind_line'] = True
            # Calculate line inclination
            m3 = (o_y - profile2_LE[1]) / (o_x - profile2_LE[0])
            Theta = np.arctan(m3)
            kwargs['Theta'] = Theta
            kwargs['AOA'] = self.Theta1

            H_shifting = inclined_line(LineShiftRepresentation, line_shift,
                                       Theta, **kwargs)

        elif inclination == 'PerpendicularToChord':
            kwargs['inclind_line'] = True
            m3 = -1/self.m1 if self.m1 != 0 else np.inf
            Theta = np.arctan(m3)
            kwargs['Theta'] = Theta
            H_shifting = inclined_line(LineShiftRepresentation,
                                       line_shift, Theta, **kwargs)

        if kwargs['inclind_line']:
            LineLength = v_length / np.sin(Theta)
            x_new = o_x - H_shifting + v_start / m3

            # Finding the distance between the line and the inclined line
            a3 = y_new - m3 * x_new
            x3, y3 = IntersectionPoint([self.m1, m3], [self.a1, a3],
                                       [origin_LE, (x_new, y_new)])
            kwargs['chord_intx'] = (x3, y3)
            print('Points inclination angle to Horizontal = ', np.rad2deg(Theta))

            if len(self.lazer_info) > 2:
                x_other = profile2_LE[0] + self.chord_len * np.cos(self.Theta1)
                y_other = profile2_LE[1] + self.chord_len * np.sin(self.Theta1)
                print(x_other, y_other, m3, a3)

                p4, p5 = cascade_inc_line_plotting_pram(profile2_LE,
                                                        (x_other, y_other),
                                                        line_shift, m3, a3,
                                                        (x3,y3), **kwargs)
                kwargs['dist_from_origin'] = p4
                kwargs['perpendicular_intx'] = p5
                kwargs['profile2_TE'] = (x_other, y_other)


        self.ax = ImageVisualization(self.ax, self.lazer_info, BG =self.bg,
                                     reverse = invert, **kwargs)
        if preview_lengths:
            PointsInfoVisualization(self.ax, self.lazer_info, lineInfo,
                                    H_shifting, self.DegTheta1, **kwargs)

        dy_list = kwargs.get('dy_list', None)
        if dy_list is None:
            delta_l_new = LineLength / (n_points - 1)
            dx = -(delta_l_new*np.cos(Theta))
            dy = -(delta_l_new*np.sin(Theta))
            print(f"Delta_xy = {delta_l_new} mm,",
                  f"dx,dy = {dx}, {dy}")

        full_points_set = self.PointGenerator([x_new, y_new], n_points, NPR,
                                              delta = [dx , dy], slope = m3,
                                              PointType='L', **kwargs)
        with open('Info.txt', 'a') as f:
            f.write(f"Starting point vertical distance from origine (mm):\t{v_start}\n")
            f.write(f"Line distance from origine (mm):\t{line_shift}\n")
            f.write(f"Vertical length of the line (mm):\t{v_length}\n")
            f.write(f"Number of measuring points:\t{n_points}\n")
            f.write(f"Line inclination:\t{inclination}\n")
            f.write(f"Line shift representation:\t{LineShiftRepresentation}\n")
        return full_points_set

    def BLLineGenerator(self,
                        CADinfo: tuple[float, float, float],
                        lineInfo: tuple[float, list[tuple[float, float]], int],
                        Imageindex: int = 0,
                        invert: bool = True,
                        NPR: int = 6,
                        **kwargs) -> list[tuple[float, float]]:

        """
        Generates boundary layer lines based on CAD and line information.

        Parameters:
            - **self**: Instance of the class.
            - **CADinfo (tuple[float, float, float])**: CAD information including:
                - MP: Location on the chord (x/c).
                - SVA: Surface normal angle to the chord.
                - SCD: Distance from the chord to the profile surface.
            - **lineInfo (tuple[float, list[tuple[float, float]], int])**: Line information including:
                - starting_l: Starting point vertical distance from the origin.
                - Delta_l: List of tuples containing distance between each point (mm) and distance from the surface (mm).
                - n_points: Number of measuring points.
            - **Imageindex (int)**: Index of the image to use. Defaults to 0.
            - **invert (bool)**: Whether to invert the plot. Defaults to True.
            - **NPR (int)**: Number of points per run. Defaults to 6.

        Keyword Arguments:
            - **display_BL_calculation (bool)**: Whether to display boundary layer calculation details. Defaults to False.
            - **points_size (int)**: Size of the points to plot. Defaults to 8.
            - **line_width (int)**: Width of the lines to plot. Defaults to 1.

        Returns:
            - **full_points_set (list)**: Generated points for the boundary layer line.
        """

        # Unpack self variables
        origin_LE, origin_TE, profile2_LE = self.lazer_info
        # ``starting_l``: starting point distance from surface
        # ``v_length``: vertical length of the line
        # ``Delta_l``:[[distance between each point (mm),
        #               distance from surface (mm)], .... ]
        # ``v_start``: starting point vertical distance from origine
        starting_l, Delta_l, n_points = lineInfo
        # ``MP`` : Location on cord "Measuring point on the chord" (x/c)
        # ``SVA``: Surface normal angle to the chord
        # ``SCD``: distance from chord to the profile surface
        MP, SVA, SCD = CADinfo

        # Lazer_Cord_Length = np.sqrt((origin_LE[0]-origin_TE[0])**2+(origin_LE[1]-origin_TE[1])**2)

        # Calculate point on the chord line
        Delta_x1 = ((1 - MP) * self.chord_len) * np.cos(self.Theta1)
        x1 = origin_TE[0] - Delta_x1
        Delta_y1 = ((1 - MP)*self.chord_len) * np.sin(self.Theta1)
        y1 = origin_TE[1] - Delta_y1

        Surface_V_toH_Angle = SVA + self.DegTheta1
        Theta2 = np.deg2rad(Surface_V_toH_Angle)
        print('Normal Angle (to vertical) = ', 90-Surface_V_toH_Angle, 'Deg')

        # Calculate surface point
        Delta_x2 = SCD * np.cos(Theta2)
        x2 = x1 + Delta_x2

        Delta_y2 = SCD*np.sin(Theta2)
        y2 = y1+Delta_y2
        m2 = np.tan(Theta2)

        # Calculate starting point
        Starting_x = x2 + np.sqrt(starting_l ** 2 / (m2 ** 2 + 1))
        Starting_y = y2 + np.sqrt(starting_l ** 2 - (Starting_x - x2) ** 2)

        fullLength = np.sqrt((Starting_x - x2) ** 2 + (Starting_y - y2) ** 2)

        # Get keyword arguments
        display_BL_calculation = kwargs.get('display_BL_calculation', False)
        points_size = kwargs.get('points_size', 8)


        # Display boundary layer calculation if enabled
        if display_BL_calculation:
            display_BL_calcu_data(self.ax, origin_LE, origin_TE,
                                  self.DegTheta1, Surface_V_toH_Angle,
                                  (x1,y1), (x2,y2), m2, **kwargs)

        full_points_set = self.PointGenerator([Starting_x, Starting_y],
                                              n_points, NPR, dy_list=Delta_l,
                                              slope=m2, Dis=starting_l,
                                              **kwargs)

        if display_BL_calculation == True:
            line_width = kwargs.get('line_width', 1)
            self.ax.plot(x1, y1, 'x', color='tab:orange', ms=points_size, lw=line_width)
            arc1 = Arc((x1, y1), 2, 2, color='k')
            self.ax.add_patch(arc1)

            self.ax.plot(x2, y2, 'x', color='tab:orange', ms=points_size, lw=line_width)

            arc1 = Arc((x2, y2), 2, 2, color='k')

            self.ax.add_patch(arc1)

            self.ax.plot([x1, x2], [y1, y2], '-', lw=line_width, color='#77dd77')

            arc1 = Arc((x1, y1), 20, 20, theta1=0, theta2=Surface_V_toH_Angle,
                       color='k', lw=line_width)

            arc2 = Arc((x1, y1), 35, 35, theta1=self.DegTheta1,
                       theta2=SVA+self.DegTheta1, color='k', lw=line_width)

            self.ax.add_patch(arc1)
            self.ax.add_patch(arc2)

        self.ax = ImageVisualization(self.ax, self.lazer_info, BG =self.bg,
                                     reverse=invert, **kwargs)

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
