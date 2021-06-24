# INE5420 2021.1 - Computação Gráfica (UFSC)
Sistema básico de Computação Gráfica 2D da disciplina INE5420 - UFSC. 
O programa apresenta o display file para 2D capaz de representar pontos, segmentos de retas e polígonos. Cada objeto possui um nome, um tipo e sua lista de coordenadas de tamanho variável dependendo de seu tipo. O programa executa a transformação de viewport em 2D, funções de Panning/navegação 2D e funções de Zooming.

## Requisitos
- Python3 3.6.5
- PyQt 5.0

## Como utilizar
A adição de um novo objeto (Ponto, Reta, Wireframe) é feita através dos atalhos *Shift + A* ou *Ctrl + A*. Para adicionar um objeto deve-se atribuir um nome, selecionar seu tipo e descrever suas coordenadas, conforme padrão a seguir (sem espaços entre as coordenadas):
- Ponto: (X<sub>0</sub>,Y<sub>0</sub>)
- Reta: (X<sub>0</sub>,Y<sub>0</sub>),(X<sub>1</sub>,Y<sub>1</sub>)
- Wireframe: (X<sub>0</sub>,Y<sub>0</sub>),(X<sub>1</sub>,Y<sub>1</sub>), ..., (X<sub>n</sub>,Y<sub>n</sub>)

## Atalhos

```
Shift + A, Ctrl + A: Adicionar um novo objeto
Ctrl + Q: Encerrar o programa
Ctrl + +: Zoom In
Ctrl + -: Zoom Out
```
## Execução

Para rodar o programa, no diretório **src** executar:

```
python main.py
```

## Alunos
- Maria Eduarda de Melo Hang (17202304)
- Ricardo Giuliani (17203922)  
