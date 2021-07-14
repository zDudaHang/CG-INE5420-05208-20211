from PyQt5 import QtGui
from PyQt5.QtWidgets import QFileDialog
from util import get_color_name
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
        self.objects = {}
            
    def load_obj(filename: str, default_mtl='default_mtl'):
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
                
            return obj

    def save_obj(objects_list: List[GraphicObject]):
        try:
            temp : List[Point2D] = []
            filename = QFileDialog.getSaveFileName(filter="OBJ (*.obj)")
            with open(filename[0], 'w' ) as file:
                for obj in objects_list:
                    for coord in obj.coordinates:
                        if coord in temp:
                            continue
                        else:
                            file.write(f'v {coord.get_x()} {coord.get_y()}\n')
                            temp.append(coord)
                
                for obj in objects_list:                
                    # Nome
                    file.write(f'o {obj.name}\n')

                    # Cor
                    file.write(f'usemtl {get_color_name(obj.color)}\n')

                    coords_str = ''

                    if len(obj.coordinates) == 1:
                        coords_str += 'p '
                    else:
                        coords_str += 'l '

                    # Coordenadas
                    for coord in obj.coordinates:
                        coords_str += f'{temp.index(coord) + 1} '

                    file.write(f'{coords_str}\n')
        except:
            pass