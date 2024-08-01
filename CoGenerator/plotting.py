
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import transforms
import matplotlib.patches as mpatch

def ImageVisualization(ax, lazer_info: list[list[float]], 
                       BG: tuple[str, tuple[int]] = None, reverse: bool=True,
                       **kwargs):
    """
    Visualize data points and optionally a background image on a given axis.

    Parameters:
        - **ax (matplotlib.axes.Axes)**: The axes on which to plot the data.
        - **LAZERinfo (list[list[float]])**: List of [x, y,...] coordinates to plot.
        - **BG (tuple[str, tuple[int], float], optional)**: Tuple containing
        the path to a background image and the image extent adjustments as 
        (left, right, top, bottom) and rotation if required. Defaults to None.
        - **reverse (bool)**: Whether to reverse the x-axis. Defaults to True.

    Keyword Arguments:
        - **points_size (int)**: Size of the points to plot. Defaults to 8.
        - **grid_on (bool)**: Whether to display the grid. Defaults to True.
        - **xlabel (str)**: Label for the x-axis. Defaults to r'$X$[mm]'.
        - **ylabel (str)**: Label for the y-axis. Defaults to r'$Y$[mm]'.
        - **BGcolor (str)**: Background color of the plot. Defaults to 'white'.
        - **figxlim (list[int, int])**: X-axis limits as [min, max]. 
                                       Defaults to [0, 0].
        - **figylim (list[int, int])**: Y-axis limits as [min, max]. 
                                        Defaults to [0, 0].

    Returns:
        - **ax (matplotlib.axes.Axes)**: The modified axes with the plot.

    Example:
        >>> import matplotlib.pyplot as plt

        >>> fig, ax = plt.subplots()
        >>> LAZERinfo = [[100, 200],  # Leading Edge P1
                         [150, 250],  # Trailling Edge P1
                         [200, 300]]  # Leading Edge P2
        >>> BG = ('path/to/image.jpg', (10, 10, 10, 10))
        >>> ImageVisualization(ax, LAZERinfo, BG, reverse=True, 
                                points_size=10, grid_on=True, 
                                xlabel='X-axis', ylabel='Y-axis')
        >>> plt.show()
    """
    # Get keyword arguments or use defaults
    points_size = kwargs.get('points_size', 8)
    grid_on = kwargs.get('grid_on', True)
    xlabel = kwargs.get('xlabel', r'$X$[mm]')
    ylabel = kwargs.get('ylabel', r'$Y$[mm]')
    BGcolor = kwargs.get('BGcolor', 'white')
    figxlim = kwargs.get('figxlim', [0, 0])
    figylim = kwargs.get('figylim', [0, 0])

    # Extract x and y coordinates from LAZERinfo
    x = [i[0] for i in lazer_info]
    y = [i[1] for i in lazer_info]

    # Plot the lazer_info to the figure
    ax.plot(x, y, 'rx', label='_Hidden', ms=points_size)

    # If a background image is provided, display it
    if BG is not None:
        image_path = BG[0]
        image_str = BG[1]
        im_rotate = 0
        if len(BG) > 2: 
            im_rotate = BG[2]
    
        img = plt.imread(image_path)
        tr = transforms.Affine2D().rotate_deg(im_rotate)
        ax.imshow(img, 
                  extent=[x[0]-image_str[0], x[1]+image_str[1],
                          y[0]+image_str[2], y[1]-image_str[3]],
                  transform = tr + ax.transData)

    # Configure the grid
    ax.grid(grid_on, which='major', color='#D8D8D8', 
            linestyle='-', alpha=0.2, lw=1.5)
    ax.minorticks_on()
    ax.grid(grid_on, which='minor', color='#D8D8D8', linestyle='-', alpha=0.1)
    
    # Optionally reverse the x-axis
    if reverse:
        ax.invert_xaxis()
    # Always reverse the y-axis    
    ax.invert_yaxis()

    # Set x-ticks and labels
    ax.set_xticks(np.arange(x[0]-100,x[0]+260, step=20))

    xticks = ax.get_xticks()
    labelsX = [round(item - x[0]) for item in xticks]
    ax.set_xticklabels(labelsX)

    # Set y-ticks and labels
    ax.set_yticks(np.arange(y[0]-100, y[0]+260, step=20))

    yticks = ax.get_yticks()
    labelsY = [round(item - y[0]) for item in yticks]
    ax.set_yticklabels(labelsY)

    # Set x-axis limits if specified
    if abs(figxlim[0] - figxlim[1]) > 0:
        ax.set_xlim([round(x[0]+figxlim[0]), round(x[0]+figxlim[1])])

    # Set y-axis limits if specified
    if abs(figylim[0] - figylim[1]) > 0:
        ax.set_ylim([round(y[0]+figylim[0]), round(y[0]+figylim[1])])

    # Set axis labels and background color
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_facecolor(BGcolor)

    return ax

def PointsInfoVisualization(ax, lazer_info: list[list[float]], 
                            lineInfo: list[float], H_shift: float, 
                            AOA_Deg: float, **kwargs):

    Origin_LE, Origin_TE, profile2_LE = lazer_info
    o_x,o_y,_ = Origin_LE
    # ``v_start``: starting point vertical distance from origine
    # ``v_length``: vertical length of the line
    v_start,_,v_length,_ = lineInfo

    x3 = kwargs.get('x3', None)
    y3 = kwargs.get('y3', None)
    a3 = kwargs.get('a3', None)
    x4 = kwargs.get('x4', None)
    y4 = kwargs.get('y4', None)
    m4 = kwargs.get('m4', None)
    Theta = kwargs.get('Theta', None)
    dim_size = kwargs.get('dim_size', 30)
    points_size = kwargs.get('points_size', 8)
    text_color = kwargs.get('text_color', 'w')
    arrows_color = kwargs.get('arrows_color', 'w')
    ngtiv_dim_size = kwargs.get('ngtiv_dim_size', dim_size)
    H_shift_dim_size = kwargs.get('H_shift_dim_size', dim_size)
    strt_dist_dim_size = kwargs.get('strt_dist_dim_size', dim_size)
    Chord_ext_dim_size = kwargs.get('Chord_ext_dim_size', dim_size)

    # Horizontally farest point to the origin
    x_start = o_x - H_shift
    x_last = o_x - H_shift
    if Theta is not None:
        x_start += (v_start/np.tan(Theta))
        x_last -= ((v_length-v_start)/np.tan(Theta))

    # Dimensions annotation
    # H-clear line
    if H_shift >= 0: sign = 1; end_lin = x_last
    else:  sign = -1; end_lin = x_start
    
    # middle line for dimensions
    ax.plot([o_x - H_shift - 2 * sign, end_lin - 10 * sign], 
            [o_y + 0.1, o_y + 0.1], '-',
                label='_Hidden', lw=1, color=arrows_color)
    
    # upper line dimensions
    ax.plot([end_lin - 10*sign, x_start - 2 * sign], 
            [o_y + v_start, o_y + v_start], '-',
            label='_Hidden', lw=1, color=arrows_color)
    
    ax.annotate('', xy=(end_lin - 5 * sign, o_y - 0.75), 
                xytext=(end_lin - 5 * sign, o_y + v_start + 0.75),
                color=arrows_color,
                arrowprops=dict(arrowstyle='<|-|>', lw=1,
                                color=arrows_color, 
                                mutation_aspect=4,
                                mutation_scale=10))
    
    # distance from start point to the origin
    ax.text(end_lin - 7 * sign, (2 * o_y + v_start)/2, f'{v_start:0.0f}',
            {'ha': 'center', 'va': 'center'}, size=strt_dist_dim_size,
            color=text_color, rotation=90 * sign)
    
    # lower line dimensions
    ax.plot([end_lin - 10 * sign, x_last - 2 * sign], 
            [o_y - (v_length-v_start), o_y - (v_length - v_start)],
            '-', label='_Hidden', lw=1, color=arrows_color)

    ax.annotate('', xy=(end_lin - 5 * sign, o_y + 0.75), color=arrows_color,
                xytext=(end_lin - 5 * sign, o_y - (v_length - v_start) - 0.75),
                    arrowprops=dict(arrowstyle='<|-|>', lw=1,
                                    color=arrows_color, mutation_aspect=4,
                                    mutation_scale=10))
    
    # distance from last point to the origin
    ax.text(end_lin - 7 * sign, ((2 * o_y-(v_length-v_start))/2),
                f'{v_length-v_start:0.0f}',
                {'ha': 'center', 'va': 'center'}, size=ngtiv_dim_size,
                color=text_color, rotation=90 * sign)

    ax.annotate('', xy=(o_x, o_y), 
                color=arrows_color, xytext=(o_x - H_shift, o_y),
                arrowprops=dict(arrowstyle='<|-|>', lw=1,
                                color=arrows_color,
                                mutation_aspect=0.5))

    # H_shifting
    ax.text(((o_x + o_x - H_shift)/2), o_y - 3, 
            f'{H_shift:0.2f}', {'ha': 'center', 'va': 'center'}, 
            size=H_shift_dim_size, color=text_color)

    if x3 is not None:
        # lengths on chord
        x_coord = [o_x, Origin_TE[0], x3]
        y_coord = [o_y, Origin_TE[1], y3]
        y_coord = [x for _, x in sorted(zip(x_coord, y_coord))]
        ax.plot(sorted(x_coord), y_coord, 'r--', ms=10, label='_Hidden')

        chord_len = np.sqrt((o_x-Origin_TE[0])**2+(o_y-Origin_TE[1])**2)
        x_other = profile2_LE[0] + chord_len * np.cos(np.deg2rad(AOA_Deg))
        y_other = profile2_LE[1] + chord_len * np.sin(np.deg2rad(AOA_Deg))

        ax.plot(x_other, y_other, 'x', label='_Hidden', 
                ms=points_size, color = 'tab:orange')
        ax.plot([Origin_TE[0], x_other],
                [Origin_TE[1], y_other],
                'y--', ms=5, linewidth=0.5, label='_Hidden')
        ax.plot([profile2_LE[0], o_x],
                [profile2_LE[1], o_y],
                'y--', ms=5, linewidth=0.5, label='_Hidden')

        # Chord extension length
        L3 = np.sqrt((o_x-x3)**2+(o_y-y3)**2)
        ax.text(((o_x + x3) / 2) + 2 * sign, ((o_y + y3) / 2) + 2 * sign,
                f"{L3:0.2f}", {'ha': 'center', 'va': 'center'},
                size=Chord_ext_dim_size, color='r',
                rotation = AOA_Deg)
        
        # perpendicular line length from origin to the line
        DegTheta3 = Theta*180/np.pi
        if H_shift < 0  and L3 > chord_len:
            y1 = o_y + v_start
            y2 = o_y - (v_length-v_start)
            m3 = (y1 - y2)/(x_start - x_last)
            m4 = -1/m3
            a3 = y1 - m3 * x_start
            a4 = y_other - m4 * x_other
            x4 = (a3-a4)/(m4-m3)
            y4 = m4*x4+a4
            p4 = np.array([x4, y4])
            L4 = np.linalg.norm(np.array([x_other, y_other]) - p4)
            ax.plot([x_other, x4],
                    [y_other, y4],
                    'y--', ms=5, linewidth=0.5, label='_Hidden')
            
            rect = mpatch.Rectangle((x4, y4), 2, 2, facecolor='y',
                                    angle=270+DegTheta3)
            ax.add_patch(rect)

            ax.text(((x_other+x4)/2)+2,
                    ((y_other+y4)/2)+2, str(round(L4, 2)),
                    {'ha': 'center', 'va': 'center'}, size=30, color='y',
                    rotation=270+DegTheta3)
        else:
            p4 = np.array([x4, y4])
            L4 = np.linalg.norm(profile2_LE[:2] - p4)
            ax.plot([profile2_LE[0], x4],
                    [profile2_LE[1], y4],
                    'y--', ms=5, linewidth=0.5, label='_Hidden')

            rect = mpatch.Rectangle((x4, y4), 2, 2, facecolor='y',
                                    angle=270+DegTheta3)
            ax.add_patch(rect)

            ax.text(((profile2_LE[0]+x4)/2)+2,
                    ((profile2_LE[1]+y4)/2)+2, str(round(L4, 2)),
                    {'ha': 'center', 'va': 'center'}, size=30, color='y',
                    rotation=270+DegTheta3)
    
    return ax
            