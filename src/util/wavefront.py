from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QFileDialog
from typing import List

from src.model.point import Point3D
from src.model.graphic_object import GraphicObject, get_rgb
from src.model.enum.graphic_object_enum import GraphicObjectEnum
import os.path

class WavefrontOBJ:
    def __init__( self ):
        self.path      = None               
        self.mtllibs   = []                
        self.mtls      = False    
        self.vertices  = []                  
        self.window    = []                 
        self.objects_name = []              
        self.usemtl = []
        self.new_mtl = []
        self.kd_params = []
        self.objects = {}
        self.filled = []
        self.faces = []
        self.edges = []


    def parse_mtl(self, filename_mtl ):
        if not os.path.exists(filename_mtl):
            self.mtls = False 
            return

        with open( filename_mtl, 'r' ) as objm:
            for line in objm:
                toks = line.split()
                if not toks:
                    continue
                if toks[0] == 'newmtl':
                    self.new_mtl.append(toks[1])
                elif toks[0] == 'Kd':
                    self.kd_params.append(toks[1:])    
   

    def load_obj(self, filename_obj: str, filename_mtl: str):
        
        
        with open( filename_obj, 'r' ) as objf:
            self.path = filename_obj

            for line in objf:
                toks = line.split()

                if not toks:
                    continue
                
                if toks[0] == 'mtllib':
                    self.mtls = True
                    filename_mtl += f'/{toks[1]}'
                    self.parse_mtl(filename_mtl) 

                #Vértice
                if toks[0] == 'v':
                    t = []
                    for v in toks[1:]:
                        if '-' in v:
                            t.append(float(v.replace('\U00002013', '-')))
                        else:
                            t.append(float(v))
                    self.vertices.append(Point3D(t[0],t[1],t[2]))

                #Window
                elif toks[0] == 'w':
                    indices = [ float(v)-1 for v in toks[1:]]
                    for i in indices:
                        self.window.append( self.vertices[int(i)] )

                #Object
                elif toks[0] == 'o':
                    self.objects_name.append( toks[1] )
                
                #Point
                elif toks[0] == 'p':

                    self.objects[self.objects_name[-1]] = [self.vertices[int(toks[1]) - 1]]
                    self.filled.append(False)
                
                #Line
                elif toks[0] == 'l':
                    indices = [ float(v)-1 for v in toks[1:]]
                    indices.append(indices[0])
                    temp = []
                    for i in indices:
                        temp.append( self.vertices[int(i)])                             
                    self.objects[self.objects_name[-1]] = temp
                    self.filled.append(False)
                
                elif toks[0] == 'f':
                    indices = [ int(v)-1 for v in toks[1:]]

                    temp = []
                    for i in range(len(indices)-1):
                        temp.append([indices[i]+1, indices[i+1]+1])  
                    self.edges.append(temp)
                    self.faces.append(indices)
                    self.filled.append(False)           
                    
                elif toks[0] == 'usemtl':
                    self.usemtl.append(toks[1])
  

    def save_obj(objects_list: List[GraphicObject], w_center: Point3D, w_dimensions: Point3D):
        try:
            temp : List[Point3D] = []
            color_list = []
            filename = QFileDialog.getSaveFileName()
            if filename[0] == '':
                return
            url = QUrl.fromLocalFile(filename[0])
            with open(filename[0] + '.obj', 'w' ) as file:
                for obj in objects_list:
                    if obj.type != GraphicObjectEnum.CURVE:
                        for coord in obj.coordinates:
                            if coord in temp:
                                continue
                            else:
                                file.write(f'v {coord.x()} {coord.y()}\n')
                                temp.append(coord)
                    else:
                        for coord in obj.curve_points:
                            if coord in temp:
                                continue
                            else:
                                file.write(f'v {coord.x()} {coord.y()}\n')
                                temp.append(coord)

                # WINDOW PHASE:

                if not w_center in temp:
                    file.write(f'v {w_center.x()} {w_center.y()}\n')
                    temp.append(w_center)

                if not w_dimensions in temp:
                    file.write(f'v {w_dimensions.x()} {w_dimensions.y()}\n')
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
            
                    if obj.type != GraphicObjectEnum.CURVE:
                        coords_str = ''

                        if len(obj.coordinates) == 1:
                            coords_str += 'p '
                        
                        if obj.type == GraphicObjectEnum.WIREFRAME and obj.is_filled:
                            coords_str += 'f '
                        else:
                            coords_str += 'l '

                        # Coordenadas
                        for coord in obj.coordinates:
                            coords_str += f'{temp.index(coord) + 1} '

                        file.write(f'{coords_str}\n')
                    else:
                        for p in range(len(obj.curve_points)-1):
                            coords_str = f'l {temp.index(obj.curve_points[p]) +1} {temp.index(obj.curve_points[p+1]) +1}'
                            file.write(f'{coords_str}\n')
            
            with open(filename[0] + '.mtl', 'w' ) as file:
                
                for c in color_list:
                    file.write(f'newmtl color{color_list.index(c)}\n')
                    color = get_rgb(c)
                    file.write('Kd '+' '.join('{:0.6f}'.format(clr) for clr in color)+'\n')

        except:
            pass