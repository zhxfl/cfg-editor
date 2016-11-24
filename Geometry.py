from PyQt4.QtCore import *
import math

def InterPoint(u1, u2, v1, v2):
    x0 = 1.0 * u1.x()
    x1 = 1.0 * u2.x()
    x2 = 1.0 * v1.x()
    x3 = 1.0 * v2.x()
    y0 = 1.0 * u1.y()
    y1 = 1.0 * u2.y()
    y2 = 1.0 * v1.y()
    y3 = 1.0 * v2.y()

    if y3 == y2:
        y3 = y2 + 1
    if x3 == x2:
        x3 = x2 + 1
    if x1 == x2:
        x2 == x1 + 1
    if y1 == y2:
        y2 == y1 + 1

    y = ((y0-y1)*(y3-y2)*x0 + (y3-y2)*(x1-x0)*y0 + (y1-y0)*(y3-y2)*x2 + (x2-x3)*(y1-y0)*y2 ) / ( (x1-x0)*(y3-y2) + (y0-y1)*(x3-x2) );
    x = x2 + (x3-x2)*(y-y2) / (y3-y2);
    return QPoint(x, y)


def PointToLineInterPoint(u1, u2, v1):
    x1 = u1.x()
    x2 = u2.x()
    x3 = v1.x()

    y1 = u1.y()
    y2 = u2.y()
    y3 = v1.y()
    if x1 == x2:
        x1 = x2 + 1
    k = 1.0 * (y1 - y2) / (x1 - x2)
    b = y1 - k * x1
    if k == 0:
        k = 0.0000001
    k1 = -1.0 / k
    b1 = y3 - k1 * x3
    if b == b1:
        b = b1 + 1
    x4 = -1.0 * (b - b1) / (k - k1)
    y4 = k1 * x4 + b1
    return QPoint(x4, y4)

def IsSegmentIntersect(p1, p2, p3, p4):
    d1 = Cross(p3, p4, p1)
    d2 = Cross(p3, p4, p2)
    d3 = Cross(p1, p2, p3)
    d4 = Cross(p1, p2, p4)
    if d1 * d2 < 0 and d3 * d4 < 0:
        return True
    elif d1 == 0 and OnSegment(p3, p4, p1):
        return True
    elif d2 == 0 and OnSegment(p3, p4, p2):
        return True
    elif d3 == 0 and OnSegment(p1, p2, p3):
        return True
    elif d4 == 0 and OnSegment(p1, p2, p4):
        return True
    else:
        return False

def Cross(p1, p2, p3):
    d1 = QPoint(p3.x() - p1.x(), p3.y() - p1.y())
    d2 = QPoint(p2.x() - p1.x(), p2.y() - p1.y())
    return d1.x() * d2.y() - d1.y() * d2.x()

def OnSegment(p1, p2, p3):
    x_min = 0
    x_max = 0
    y_min = 0
    y_max = 0
    if p1.x() < p2.x():
        x_min = p1.x()
        x_max = p2.x()
    else:
        x_min = p2.x()
        x_max = p1.x()

    if p1.y() < p2.y():
        y_min = p1.y()
        y_max = p2.y()
    else:
        y_min = p2.x()
        y_max = p1.x()
    if p3.x() < x_min or p3.x() > x_max or p3.y() < y_min or p3.y() > y_max:
        return False
    else:
        return True


def GetDistance(p1, p2):
    x1 = p1.x() - p2.x()
    y1 = p1.y() - p2.y()
    return math.sqrt(x1 * x1 + y1 * y1)

def getDistance(p1, p2):
    x1 = p1.x() - p2.x()
    y1 = p1.y() - p2.y()
    return math.sqrt(x1 * x1 + y1 * y1)

def GetMidPoint(p1, p2):
    return QPoint((p1.x() + p2.x()) / 2, (p1.y() + p2.y()) / 2)

def ClockWise(VectorObj, nAngle):
    x = VectorObj.x()
    y = VectorObj.y()
    cosa = math.cos(nAngle)
    sina = math.sin(nAngle)
    #print 'cosa', 'sina'
    return QPoint(x * cosa - y * sina, x * sina + y * cosa)

def AntiClockWise(VectorObj, nAngle):
    x = VectorObj.x()
    y = VectorObj.y()
    cosa = math.cos(nAngle)
    sina = math.sin(nAngle)
    return QPoint(y * sina + x * cosa, -x * sina + y * cosa)

def GetPointByVectorAndLegth(VectorObj, nLen):
    VX = VectorObj.x()
    VY = VectorObj.y()
    AX = 0
    AY = 0
    L = nLen
    AX = math.sqrt(L * L * VX * VX / (VY * VY + VX * VX))
    AY = math.sqrt(L * L * VY * VY / (VY * VY + VX * VX))
    if VX < 0:
        AX = -AX
    if VY < 0:
        AY = -AY
    return QPoint(AX, AY)

def GetUnitVector(VectorObj):
    x = VectorObj.x()
    y = VectorObj.y()
    c = math.sqrt(x * x + y * y)
    return QPointF(x / c, y / c)