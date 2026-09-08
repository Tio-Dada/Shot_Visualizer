import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_court(ax=None, color='black', lw=2, outer_lines=False):
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 11))
    #X-limits: -250 to 250
    #Y-limits: -47.5 to 422.5
    ax.set_xlim(-250, 250)
    ax.set_ylim(-47.5, 422.5)

    # Draw the hoop
    hoop = patches.Circle((0, 0), radius=7.5, linewidth=1.5, fill=False, color='black', zorder=3)
    ax.add_patch(hoop)

    # Draw the backboard
    backboard = patches.Rectangle((-30, -7.5), 60, 1, linewidth=2, color='black', zorder=3)
    ax.add_patch(backboard)

    # Draw the paint
    paint = patches.Rectangle((-80, -47.5), 160, 190, linewidth=2, fill=False, color='black', zorder=3)
    ax.add_patch(paint)

    # Draw the free throw circle
    free_throw_top_half = patches.Arc((0, 142.5), 120, 120, theta1=0, theta2=180, linewidth=2, fill=False, color='black', zorder=3)
    free_throw_bottom_half = patches.Arc((0, 142.5), 120, 120, theta1=180, theta2=360, linewidth=2, linestyle='dashed', fill=False, color='black', zorder=3)
    ax.add_patch(free_throw_top_half)
    ax.add_patch(free_throw_bottom_half)

    # Draw the corner three-point lines
    cornerline_left = plt.Line2D([-220, -220], [-47.5, 89.5], linewidth=2, color='black', zorder=3)
    cornerline_right = plt.Line2D([220, 220], [-47.5, 89.5], linewidth=2, color='black', zorder=3)
    ax.add_line(cornerline_left)
    ax.add_line(cornerline_right)

    # Draw the three-point arc
    three_point_arc = patches.Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=2, color='black', zorder=3)
    ax.add_patch(three_point_arc)

    # Draw the restricted area
    restricted_area = patches.Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=2, color='black', zorder=3)
    ax.add_patch(restricted_area)

    # Draw Outer court boundary
    outer_boundary = patches.Rectangle((-250, -47.5), 500, 470, linewidth=2, fill=False, color='black', zorder=3)
    ax.add_patch(outer_boundary)

    # Draw center court circles
    outer_center_circle = patches.Arc((0, 422.5), 120, 120, theta1=180, theta2=360, linewidth=2, fill=False, color='black', zorder=3)
    inner_center_circle = patches.Arc((0, 422.5), 40, 40, theta1=180, theta2=360, linewidth=2, fill=False, color='black', zorder=3)
    ax.add_patch(outer_center_circle)
    ax.add_patch(inner_center_circle)

    ax.set_aspect('equal', adjustable='box')
    ax.set_axis_off()
    return ax

#draw_court(ax=None, color='black', lw=2, outer_lines=False)
#plt.show()