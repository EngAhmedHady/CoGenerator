# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 08:10:16 2022

@author: admin
"""
# from CoGenerator import CoordinatesGenerator as CG
from CoGeneratorPup import CoordinatesGenerator as CG

# CADinfo   = [0.5, 92.11884, 5.48382]
#[76.2347,75.8262,77.2260,74.7054,81.8757,83.6850,85.6464,89.3003,92.1738,94.1656,96.0591]
#[0.325  ,0.493  ,1.355  ,2.395  ,4.089  ,4.719  ,5.183  ,5.617  ,5.475  ,4.9099 ,4.0104 ]
#[0.995  ,0.99   ,0.95   ,0.9    ,0.8    ,0.75   ,0.7    ,0.6    ,0.5    ,0.4    ,0.25   ]


# TEAMAero Mine
LAZERinfo = [[230.50,-176.00,367.20],   # Leading  edge coordinates lower blade "Measured" [x00,y00,z00]
             [328.00,-194.45,367.20],   # Trailing edge coordinates lower blade "Measured" [x01,y01,z01]
             [276.90,-141.70,367.20]]   # Leading  edge coordinates Upper blade "Measured" [x10,y10,z10]

# LAZERinfo = [[226.1435400,24.94990000000,367.20],   # Leading  edge coordinates lower blade "Measured" [x00,y00,z00]
#               [323.7721016,5.59196630381,367.20],   # Trailing edge coordinates lower blade "Measured" [x01,y01,z01]
#               [273.616941797,58.896306915,367.20]]   # Leading  edge coordinates Upper blade "Measured"
              # [275.616941797,58.896306915,367.20]]   # Leading  edge coordinates Upper blade "Measured" [x10,y10,z10]

# LAZERinfo = [[126.00,-134.50,362.60],   # Leading  edge coordinates lower blade "Measured" [x00,y00,z00]
#               [173.615,-149.118,362.60],   # Trailing edge coordinates lower blade "Measured" [x01,y01,z01]
#               [103.30,-155.30,362.60]]   # Leading  edge coordinates Upper blade "Measured"

Profile_path     = "Co-fig\\profile.jpg"
ProfileImgSize   = [2.5,5.5,15.5,6] # [Left, Right, Bottom, Top]

Schlieren_path   = "Co-fig\\Profile_Sch.jpg"
SchlierenImgSize = [49,65,85.5,36.5] # [Left, Right, Bottom, Top]

Fully_Open_path   = "Co-fig\\Fully_Open_Sch.jpg"
Fully_OpenImgSize = [49,67,82,42] # [Left, Right, Bottom, Top]

testsection_model_path   = "Co-fig\\TestSectionModel3.png"
testsection_model_pathImgSize = [58,88.5,112.5,56.8] # [Left, Right, Bottom, Top]

Arun_model_path   = "Co-fig\\11(edge).jpg"
Arun_model_pathImgSize = [95,98.5,67,75] # [Left, Right, Bottom, Top]

Images = [[Profile_path  ,  ProfileImgSize],
          [Schlieren_path,SchlierenImgSize],
          [Fully_Open_path,Fully_OpenImgSize],
          [testsection_model_path,testsection_model_pathImgSize],
          [Arun_model_path, Arun_model_pathImgSize]]

Co_Generator = CG(LAZERinfo,Images);

# CADinfo  = [0.75, 83.6850, 4.719]
# Delta_l  = [[20.0, 20.0]]
# lineInfo = [0,Delta_l,2]
# Co_Generator.BLLineGenerator(CADinfo,lineInfo,Imageindex = 1, invert = False)
lineInfo = [60,30,80,20] # [starting point, H-line distance, Vertical length, N-points]
Co_Generator.LineGenerator(lineInfo, Imageindex = 1, invert = False,
                            arrows_color = 'w', text_color = 'w',preview_lengths = False,
                            legend_loc = 'upper right', legend_fsize = 30, points_size = 15,
                            )

# lineInfo = [32,50,57,20] # [starting point, H-line distance, Vertical length, N-points]
# Co_Generator.LineGenerator(lineInfo, Imageindex = 4, invert = False, inclination = 'ParallelToLEs',
#                             arrows_color = 'w', text_color = 'w',
#                             legend_loc = 'lower right', legend_fsize = 20,
#                             figxlim = [-120,100], figylim = [-60,40], BGcolor = 'k')

# lineInfo = [41.3,20,21,10] # [starting point, H-line distance, Vertical length, N-points]
lineInfo = [60,10,70,40] # [starting point, H-line distance, Vertical length, N-points]
Co_Generator.LineGenerator(lineInfo, inclination ='ParallelToLEs',
                            LineShiftRepresentation = 'NormalToLine',
                            Imageindex = 1, invert = False, preview_lengths = True,
                            points_display = 'line', points_color = 'yellow',line_width = 3,
                            # figxlim = [-20,100], figylim = [-30,80],
                            show_legend = False, points_size = 15, dim_size =30)



# lineInfo = [15,-105,50,20] # [starting point, H-line distance, Vertical length, N-points]
# Co_Generator.LineGenerator(lineInfo, inclination ='ParallelToLEs',
#                             LineShiftRepresentation = 'DistanseOnCord',
#                             Imageindex = 1, invert = False)

# Delta_l  = [[0.10,1.10],
#             [0.20,2.10],
#             [0.25,4.10],
#             [1.00,10.1],
#             [5.00,20.1]]                 #[[Distance between each point(mm), distance from surface(mm)], ... ]
# lineInfo = [0.2,Delta_l,31]              #[starting distance from the surface, Delta l Matrix, number of points]

# NPR is the number of points per run, it can be constant number or an array (Defulte = 6)
# NPR array: [[Number of points per run, Till distance], .....]
# Co_Generator.BLLineGenerator(CADinfo,lineInfo,Imageindex = 1, invert = False, NPR = [[4,1],[6,31]])

# CADinfo  = [0.9, 74.7054, 2.395]
# Delta_l  = [[0.10,1.50],
#             [0.25,6.50],
#             [0.50,7.00],
#             [1.00,10.0],
#             [5.00,20.0]]
# lineInfo = [0.2,Delta_l,40]
# Co_Generator.BLLineGenerator(CADinfo,lineInfo,Imageindex = 2, invert = False)

CADinfo  = [0.75, 83.6850, 4.719]
Delta_l  = [[0.10,1.50],
            [0.25,6.50],
            [0.50,7.00],
            [1.00,10.0],
            [5.00,20.0]]
lineInfo = [0.2,Delta_l,40]
Co_Generator.BLLineGenerator(CADinfo,lineInfo,Imageindex = 1, invert = False,
                              show_legend = False, points_size = 15, line_width = 3,
                              points_display = 'line', points_color = 'tab:red',
                              figxlim = [-40,120], figylim = [-40,80],
                              # figxlim = [-20,105], figylim = [-25,20],
                              display_BL_calculation = 1)



#Ref
# CADinfo  = [0.60, 89.3003, 5.617]
# Delta_l  = [[0.10,1.00],
#             [0.20,2.00],
#             [0.25,4.00],
#             [1.00,10.0],
#             [5.00,20.0]]
# lineInfo = [0.2,Delta_l,31]
# Co_Generator.BLLineGenerator(CADinfo,lineInfo,Imageindex = 3, invert = False, NPR = [[4,1],[6,34]],
#                              show_legend = False, points_size = 15, line_width = 20,
#                              points_display = 'line', points_color = 'tab:orange')

# Co_Generator.ax.legend(['0.75x/c','0.60x/c','0.25x/c'])

#Rough/smoothP1/P2
# CADinfo  = [0.60, 89.3003, 5.617]
# Delta_l  = [[0.10,1.80],
#             [0.20,2.00],
#             [0.25,4.00],
#             [1.00,10.0],
#             [5.00,20.0]]
# lineInfo = [0.2,Delta_l,34]
# Co_Generator.BLLineGenerator(CADinfo,lineInfo,Imageindex = 1, invert = False, NPR = [[4,1],[6,34]])

# CADinfo  = [0.5, 92.11884, 5.48382]
# Delta_l  = [[0.10,1.00],
#             [0.20,2.20],
#             [0.25,4.25],
#             [1.00,10.0],
#             [5.00,20.0]]
# lineInfo = [0.25,Delta_l,31]
# Co_Generator.BLLineGenerator(CADinfo,lineInfo,Imageindex = 2, invert = False, NPR = [[4,1],[6,31]])

# CADinfo  = [0.6, 89.3003, 5.617]
# Delta_l  = [[5,5]]
# lineInfo = [0,Delta_l,2]
# Co_Generator.BLLineGenerator(CADinfo,lineInfo,Imageindex = 1, invert = False)

# CADinfo  = [0.25, 96.0591, 4.0104]
# Delta_l  = [[0.05,0.45],
#             [0.10,1.5],
#             [0.25,2.0],
#             [1.00,10.0],
#             [2.50,15.0]]
# lineInfo = [0.1,Delta_l,31]
# Co_Generator.BLLineGenerator(CADinfo,lineInfo,Imageindex = 3, invert = False, NPR = [[4,1],[6,41]],
#                              show_legend = False, points_size = 15, line_width = 20,
#                              figxlim = [-20,105], figylim = [-25,20],
#                              points_display = 'line', points_color = 'tab:green')

# CADinfo  = [0.1, 100, 2.6]
# Delta_l  = [[0.05,0.46],
#             [0.10,1.4],
#             [0.20,2.0],
#             [0.50,8.0],
#             [1.00,10.0]]
# lineInfo = [0.15,Delta_l,30]
# Co_Generator.BLLineGenerator(CADinfo,lineInfo,Imageindex = 2, invert = False, NPR = [[4,1],[6,41]])



# CADinfo  = [0.4, 94.1656, 4.9099]
# Delta_l  = [[5,5]]
# lineInfo = [0,Delta_l,2]
# Co_Generator.BLLineGenerator(CADinfo,lineInfo,Imageindex = 1, invert = False)