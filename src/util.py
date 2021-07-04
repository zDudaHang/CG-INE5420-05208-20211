def parse(text: str) -> list:
    values = []
    number = ''
    i = 0

    while i < len(text):
        # print(f'Procurando por ( {text[i]}')
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