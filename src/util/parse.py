from typing import Union, List

from src.model.point import Point2D

def parse(text: str) -> Union[None, List[Point2D]]:
    if (len(text) == 0):
        return None
    try:
        values = _parse(text)
    except IndexError:
        return None
        
    if values == None:
        return None

    coordinates : list[Point2D] = []
    
    for i in range(0, len(values)-1, 2):
        coordinates.append(Point2D(float(values[i]), float(values[i+1])))

    return coordinates
    
def _parse(text: str) -> Union[None, List[str]]:
    values = []
    number = ''
    i = 0

    while i < len(text):
        if text[i] == '(':
            # Avanca um
            i += 1

            # Se ver um sinal de menos, adicione e nunca mais deixe outro passar
            if text[i] == '-':
                # Guarde no numero
                number += text[i]
                # Avance
                i += 1

            # Eh necessario encontrar um numero antes de encontrar a virgula
            if text[i].isnumeric():
                number += text[i]
                i += 1
            else: 
                return None
            
            # Enquanto nao encontrar uma virgula, adicione os caracteres ao numero
            foundFirstFracionaryPart = False
            while text[i] != ',':
                # Se for um numero, adicione e avance
                if text[i].isnumeric():
                    number += text[i]
                    i += 1
                # Se for o ponto da parte fracionaria, adicione e nunca mais deixe passar outro '.'
                elif text[i] == '.' and not foundFirstFracionaryPart:
                    number += text[i]
                    foundFirstFracionaryPart = True
                    i += 1
                else:
                    return None
            
            # Avance depois de achar ','
            i += 1
            values.append(number)
            number = ''

            if text[i] == '-':
                number += text[i]
                i += 1
            
            # Eh necessario encontrar um numero antes de encontrar o ')'
            if text[i].isnumeric():
                number += text[i]
                i += 1
            else: 
                return None
            
            foundSecondFracionaryPart = False
            while text[i] != ')':
                if text[i].isnumeric():
                    number += text[i]
                    i += 1
                elif text[i] == '.' and not foundSecondFracionaryPart:
                    number += text[i]
                    foundSecondFracionaryPart = True
                    i += 1
                else:
                    return None
            
            values.append(number)
            number = ''

            # Se chegou no final da sentenca, pare
            if i == len(text) - 1:
                break
            # Caso contrario, avance e verifique se existe uma ',' para continuar
            else:
                i += 1
                if text[i] == ',':
                    i += 1
                    # Se chegou no final da sentenca, estah errado
                    if i >= len(text) - 1:
                        return None
                # Se nao houver uma virgula, a sentenca estah errada
                else:
                    return None
        else:
            return None  
    return values  