from PyQt5.QtCore import QUrl
from util import get_rgb
from PyQt5.QtWidgets import QFileDialog
from point import Point2D
from typing import List
from graphic_object import GraphicObject


class WavefrontOBJ:
    def __init__( self, default_mtl='default_mtl' ):
        self.path      = None               
        self.mtllibs   = []                
        self.mtls      = [ default_mtl ]    
        self.vertices  = []                  
        self.window    = []                 
        self.objects_name = []              
        self.usemtl = []
        self.new_mtl = []
        self.kd_params = []
        self.objects = {}
            
    def load_obj(self, filename: str, default_mtl='default_mtl'):
        with open( filename, 'r' ) as objf:
            obj = WavefrontOBJ(default_mtl=default_mtl)
            obj.path = filename
            for line in objf:
                toks = line.split()
                if not toks:
                    continue
                if toks[0] == 'v':
                    t = []
                    for v in toks[1:]:
                        if '-' in v:
                            t.append(float(v.replace('\U00002013', '-')))
                        else:
                            t.append(float(v))
                    obj.vertices.append(t)
                elif toks[0] == 'w':
                    indices = [ float(v)-1 for v in toks[1:]]
                    for i in indices:
                        obj.window.append( obj.vertices[int(i)] )
                elif toks[0] == 'o':
                    obj.objects_name.append( toks[1] )
                elif toks[0] == 'p':
                    obj.objects[obj.objects_name[-1]] = [obj.vertices[int(toks[1])]]
                elif toks[0] == 'l':
                    indices = [ float(v)-1 for v in toks[1:]]
                    temp = []
                    for i in indices:
                        temp.append( obj.vertices[int(i)])                             
                    obj.objects[obj.objects_name[-1]] = temp             
                elif toks[0] == 'mtllib':
                    obj.mtllibs.append( toks[1] )
                elif toks[0] == 'usemtl':
                    obj.usemtl.append(toks[1])
                elif toks[0] == 'newmtl':
                    obj.new_mtl.append(toks[1])
                elif toks[0] == 'Kd':
                    obj.kd_params.append(toks[1:])
                
            return obj

    def save_obj(objects_list: List[GraphicObject], w_center: Point2D, w_dimensions: Point2D):
        try:
            temp : List[Point2D] = []
            color_list = []
            filename = QFileDialog.getSaveFileName(filter="OBJ (*.obj)")
            url = QUrl.fromLocalFile(filename[0])
            with open(filename[0] + '.obj', 'w' ) as file:
                for obj in objects_list:
                    for coord in obj.coordinates:
                        if coord in temp:
                            continue
                        else:
                            file.write(f'v {coord.get_x()} {coord.get_y()}\n')
                            temp.append(coord)

                # WINDOW PHASE:

                if not w_center in temp:
                    file.write(f'v {w_center.get_x()} {w_center.get_y()}\n')
                    temp.append(w_center)

                if not w_dimensions in temp:
                    file.write(f'v {w_dimensions.get_x()} {w_dimensions.get_y()}\n')
                    temp.append(w_dimensions)
                
                file.write(f'mtllib {url.fileName()}.mtl\n')
                file.write('o window\n')
                file.write(f'w {temp.index(w_center) + 1} {temp.index(w_dimensions) + 1}\n')

                for obj in objects_list:                
                    # Nome
                    file.write(f'o {obj.name}\n')

                    # Cor
                    if obj.color not in color_list:
                        color_list.append(obj.color)
                    
                    file.write(f'usemtl color{color_list.index(obj.color)}\n')

                    coords_str = ''

                    if len(obj.coordinates) == 1:
                        coords_str += 'p '
                    else:
                        coords_str += 'l '

                    # Coordenadas
                    for coord in obj.coordinates:
                        coords_str += f'{temp.index(coord) + 1} '

                    file.write(f'{coords_str}\n')
            
            with open(filename[0] + '.mtl', 'w' ) as file:
                
                for c in color_list:
                    file.write(f'newmtl color{color_list.index(c)}\n')
                    color = get_rgb(c)
                    file.write('Kd '+' '.join('{:0.6f}'.format(clr) for clr in color)+'\n')

        except:
            pass