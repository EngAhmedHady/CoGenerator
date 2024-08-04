import numpy as np

def IntersectionPoint(M: list[float], A: list[float],
                      Ref: list[tuple]) -> tuple[tuple[int, int]]:
    """
    Calculate the intersection point between two lines.

    Parameters:
        - **M (list)**: List containing slopes of the two lines.
        - **A (list)**: List containing y-intercepts of the two lines.
        - **Ref (list)**: List containing reference points for each line.

    Returns:
        tuple:
            - A tuple containing: Pint (tuple): Intersection point coordinates
              (x, y).

    Example:
        >>> from __importImages import importSchlierenImages
        >>> instance = importSchlierenImages(f)
        >>> slopes = [0.5, -2]
        >>> intercepts = [2, 5]
        >>> references = [(0, 2), (0, 5)]
        >>> intersection = instance.IntersectionPoint(slopes, intercepts, references)
        >>> print(intersection, angles)

    .. note ::
        - The function calculates the intersection point and angles between two
          lines specified by their slopes and y-intercepts.
        - Returns the intersection point coordinates and angles of the lines in
          degrees.
    """
    from CoGenerator import BCOLOR
    theta1 = np.rad2deg(np.arctan(M[0]))
    theta2 = np.rad2deg(np.arctan(M[1]))

    Xint, Yint = None, None

    if theta1 != 0 and theta2 != 0 and theta1 - theta2 != 0:
        Xint = (A[1] - A[0]) / (M[0] - M[1])
        Yint = M[0] * Xint + A[0]
    elif theta1 == 0 and theta2 != 0:
        Yint = Ref[0][1]
        Xint = (Yint - A[1]) / M[1]
    elif theta2 == 0 and theta1 != 0:
        Xint = Ref[1][0]
        Yint = M[0] * Xint + A[0]
    else:
        print(f'{BCOLOR.WARNING}Warning:{BCOLOR.ENDC}{BCOLOR.ITALIC}Lines are parallel{BCOLOR.ENDC}')

    Pint = (Xint, Yint)
    return Pint

def h_shift_on_chord(AOA, line_angle, line_shift):
    third_angle = 180 - abs(AOA) - abs(line_angle)
    H_shifting1 = line_shift*np.sin(np.deg2rad(third_angle))
    H_shifting = H_shifting1/np.sin(np.deg2rad(line_angle))
    return H_shifting

def inclined_line(LineShiftRepresentation, line_shift, line_angle = np.pi/2, **kwargs):
    AOA = kwargs.get('AOA', np.deg2rad(90-abs(np.rad2deg(line_angle))))

    if LineShiftRepresentation == 'NormalToLine':
        if line_shift >= 0: H_shifting = line_shift / np.sin(line_angle)
        else:
            chord_len = kwargs.get('chord_len', None)
            H_shifting1 = h_shift_on_chord(np.rad2deg(AOA),
                                           np.rad2deg(line_angle),
                                           chord_len)
            H_shifting2 = line_shift / np.sin(line_angle)
            H_shifting = H_shifting2 - H_shifting1
    elif LineShiftRepresentation == 'DistanseOnCord':
        H_shifting = h_shift_on_chord(np.rad2deg(AOA),
                                      np.rad2deg(line_angle),
                                      line_shift)
    elif LineShiftRepresentation == 'HorizontalDistance':
        H_shifting = line_shift

    return H_shifting


def cascade_inc_line_plotting_pram(profile2_LE, profile2_TE,
                                   line_shift, line_slope, line_y_intr, pt_on_line,
                                   **kwargs):
    perp_slope = -1/line_slope if line_slope != 0 else np.inf
    if line_shift >= 0:
        a4 = profile2_LE[1]-perp_slope*profile2_LE[0]
        x4, y4 = IntersectionPoint([line_slope,perp_slope],
                                   [line_y_intr,a4],
                                   [pt_on_line,profile2_LE[:2]])
    else:
        a4 = profile2_TE[1]-perp_slope*profile2_TE[0]
        x4, y4 = IntersectionPoint([line_slope,perp_slope],
                                   [line_y_intr,a4],
                                   [pt_on_line,profile2_TE])

        a5 = profile2_LE[1]-line_slope*profile2_LE[0]
        x5, y5 = IntersectionPoint([line_slope,perp_slope],
                                   [a5,a4],
                                   [profile2_LE[:2],profile2_TE])
        dist_from_origin = (x5, y5)
        perpendicular_intx = (x4, y4)
    return dist_from_origin, perpendicular_intx
