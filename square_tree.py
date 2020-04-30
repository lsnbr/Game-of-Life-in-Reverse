class SquareTree:
    '''Represents partition of rectangle into as much 2^n by 2^n squares as possible'''


    def __init__(self, shape):
        '''
        shape = (height, width)
        type = 'leaf' | 'quad' | 'vertical' | 'horizontal'

        quad:  tl tr      vertical:  tl      horizontal:  tl tr
               dl dr                 dl
        '''

        self.shape = shape

        if shape == (1, 1):
            self.type = 'leaf'
        else:
            height, width = shape
            height_pow2 = 2 ** (len(bin(height)) - 3)
            width_pow2  = 2 ** (len(bin(width)) - 3)
            tl_shape = tr_shape = dl_shape = dr_shape = None

            if height == height_pow2 and width == width_pow2:
                if height == width:
                    self.type = 'quad'
                    tl_shape = tr_shape = dl_shape = dr_shape = (height // 2, height // 2)
                elif height < width:
                    self.type = 'horizontal'
                    tl_shape = (height, height)
                    tr_shape = (height, width - height)
                else:
                    self.type = 'vertical'
                    tl_shape = (width, width)
                    dl_shape = (height - width, width)
            elif height == height_pow2:
                self.type = 'horizontal'
                tl_shape = (height, width_pow2)
                tr_shape = (height, width - width_pow2)
            elif width == width_pow2:
                self.type = 'vertical'
                tl_shape = (height_pow2, width)
                dl_shape = (height - height_pow2, width)
            else:
                self.type = 'quad'
                min_edge = min(height_pow2, width_pow2)
                tl_shape = (min_edge, min_edge)
                tr_shape = (min_edge, width - min_edge)
                dl_shape = (height - min_edge, min_edge)
                dr_shape = (height - min_edge, width - min_edge)

            if tl_shape: self.tl = SquareTree(tl_shape)
            else: self.tl = None
            if tr_shape: self.tr = SquareTree(tr_shape)
            else: self.tr = None
            if dl_shape: self.dl = SquareTree(dl_shape)
            else: self.dl = None
            if dr_shape: self.dr = SquareTree(dr_shape)
            else: self.dr = None



    def to_str(self, depth=0):

        pad = ' ' * depth
        nd = depth + 1
        if self.type == 'leaf':
            return f'{pad}*'
        if self.type == 'quad':
            return pad + f'\n{pad}'.join((str(self.shape), self.tl.to_str(nd), self.tr.to_str(nd), self.dl.to_str(nd), self.dr.to_str(nd)))
        if self.type == 'vertical':
            return pad + f'\n{pad}'.join((str(self.shape), self.tl.to_str(nd), self.dl.to_str(nd)))
        if self.type == 'horizontal':
            return pad + f'\n{pad}'.join((str(self.shape), self.tl.to_str(nd), self.tr.to_str(nd)))


    def __repr__(self):
        return self.to_str()