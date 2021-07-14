import numpy as np
#from collections import defaultdict
from webcolors import rgb_to_name

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
            
def load_obj( filename: str, default_mtl='default_mtl', triangulate=False ) -> WavefrontOBJ:

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

def save_obj( objects_list, filename: str ) -> WavefrontOBJ:
    # objects_list -> lista de objetos do display file
    temp = []
    with open( filename, 'w' ) as file:
        for obj in objects_list:
            vtx_list  = ' '.join([str(c) for c in obj.coordinates])
            file.write(f'v {vtx_list}\n')
            temp.append(obj.coordinates)
        file.write('mtllib sample.mtl\n')
        for obj in objects_list:
            file.write(f'o {obj.name}\n')
            file.write(f'usemtl {(obj.color).colorName()}\n')



        #self.name = name
        #self.type = type
        #self.coordinates = coordinates
        #self.color = color