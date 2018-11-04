class BoundingBox(object):
    """ Bounding box of a sprite to detect collision """
    left = 0
    top = 0
    right = 0
    bottom = 0

    def __init__(self, left=0, top=0, right=0, bottom=0):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    def __eq__(self, other):
        if isinstance(other, BoundingBox):
            return (self.left == other.left and
                    self.top == other.top and
                    self.right == other.right and
                    self.bottom == other.bottom)
        return False

    def __str__(self):
        return '[left:{}, top:{}, right:{}, bottom:{}]'.format(
            self.left, self.top, self.right, self.bottom)

    @staticmethod
    def empty_bbox():
        return BoundingBox()

    def width(self):
        return self.right - self.left

    def height(self):
        return self.bottom - self.top

    def tuple(self):
        """ return a tuple of left, top, right, bottom position """
        return self.left, self.top, self.right, self.bottom