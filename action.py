from executor import executor


def tap(widget, udid):
    return executor.tap(widget.center.x, widget.center.y, udid)


def swipe(widget, direction, udid):
    """
    swipe action on specific widget
    :param widget: widget under test
    :param direction: swipe direction, 0 for left, 1 for right, 2 for up, 3 for down.
    :param udid: udid of device
    :return:
    """
    width, height = widget.width, widget.height
    center = widget.center
    x1, x2, y1, y2 = center.x, center.y, center.x, center.y
    if direction == 0:
        stripe = width // 4
        x1 -= stripe
        x2 += stripe
    elif direction == 1:
        stripe = width // 4
        x1 += stripe
        x2 -= stripe
    elif direction == 2:
        stripe = height // 4
        y1 += stripe
        y2 -= stripe
    else:
        stripe = height // 4
        y1 -= stripe
        y2 += stripe

    return executor.swipe(int(x1), int(x2), int(y1), int(y2), udid)
