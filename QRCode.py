import sys 
import stdio 
from qrcodelib import get_error_codewords, get_format_information_bits
import stddraw

def main():
    
    #get message to be encoded

    sEncoded = stdio.readAll().rstrip('\n')

    #turn message into 8 bit message 
    arrBit = [] # to be used for real layout
    sBit = ''
    arrBitInts = []
    
    for I in range(len(sEncoded)):
        sBit = sBit + format(ord(sEncoded[I]), '08b') #one byte binary 
        arrBit.append(format(ord(sEncoded[I]), '08b'))
        
    sErrBits = sBit
    
    #create message length byte 
    lenByte = format(len(sEncoded), '08b') #8 bit binary

   
    

    sBit = '0100' + lenByte + sBit + '0000'

    #get length of message 
    lenBit = len(sBit)


    #checks to ensure validity 

    #check for too few arguments
    if len(sys.argv) < 5:
        stdio.writeln('ERROR: Too few arguments')
        quit()
    #check for too many arguments
    if len(sys.argv) > 5:
        stdio.writeln('ERROR: Too many arguments')
        quit()
        
    #assign variables
    encoding_arg = (sys.argv[1])
    n_size = (sys.argv[2])
    pp_size = (sys.argv[3])
    al_size = (sys.argv[4])
    
    arrTiming = [1, 0, 1, 0, 1, 0, 1, 0, 1]
    
    #check encoding argument

    if not str(sys.argv[1]).isdigit() or int(sys.argv[1]) >= 32 or int(sys.argv[1]) < 0:
        stdio.writeln('ERROR: Invalid encoding argument: ' + str(encoding_arg))
        quit()
    
    #create 5 bit encoding parameter

    encPar = ''

    encPar = format(int(encoding_arg), '05b')
        
    encoding_arg = encPar

        
    #check size argument

    if not str(sys.argv[2]).isdigit() or int(n_size) < 10 or int(n_size) > 48 : 
        stdio.writeln('ERROR: Invalid size argument: ' + str(n_size))
        quit()

    #check position pattern validity 

    if not str(sys.argv[3]).isdigit() or int(pp_size) < 4 or int(pp_size) % 2 != 0:
        stdio.writeln('ERROR: Invalid position pattern size argument: ' + str(pp_size))
        quit()
        
    #check allignment pattern validity 

    if not str(sys.argv[4]).isdigit() or int(al_size) < 1 or (int(al_size) - 1) % 4 != 0:
        stdio.writeln('ERROR: Invalid alignment pattern size argument: ' + str(al_size))
        quit()
    
    if encoding_arg[1] == '1':
        if int(n_size) != 25:
            stdio.writeln('ERROR: Invalid size argument: ' + str(n_size))
            quit()
        elif int(pp_size) != 8:
            stdio.writeln('ERROR: Invalid position pattern size argument: ' + str(pp_size))
            quit()
        elif int(al_size) != 5:
            stdio.writeln('ERROR: Invalid alignment pattern size argument: ' + str(al_size))
            quit()
            
        
    #check out of bounds
    if int(n_size) % 2 == 0:
        bPos = int(pp_size) >= int(n_size) // 2
    else:
        bPos = int(pp_size) > int(n_size) // 2
    if int(al_size) > int(n_size) - (int(n_size) - int(pp_size) - 1) or bPos:
        stdio.writeln('ERROR: Alignment/position pattern out of bounds')
        quit()
        
     #check that there is enough space for encoded message
    if encoding_arg[1] == '1':
        if len(sErrBits) > 208 or len(sEncoded) > 255: 
            stdio.writeln('ERROR: Payload too large')
            quit()
    elif encoding_arg[1] == '0':
        if lenBit > (int(n_size) ** 2 - (int(pp_size) ** 2) * 3 - int(al_size) ** 2) or len(sEncoded) > 255:
            stdio.writeln('ERROR: Payload too large')
            quit()
    
    n_size = int(sys.argv[2])
    pp_size = int(sys.argv[3])
    al_size = int(sys.argv[4])
    
    
        
    #arrays for padding bits and terminator 

    arrPadding = [1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1]
    arrTer = [0, 0, 0, 0]
    
    sErrBits = '0100' + lenByte + sErrBits + '0000'
    
    if len(sErrBits) < 224: 
        sErrBits = sErrBits + '00000000'
    counter = 0
    while len(sErrBits) < 224: 
        sErrBits = sErrBits + str(arrPadding[counter])
        counter += 1
        if counter == len(arrPadding):
            counter = 0
            
    arrBitInts = []
    for I in range(len(sErrBits) // 8):
        string = ''
        for J in range(8):
            string = string + sErrBits[I * 8  + J]
        arrBitInts.append(string)
    
    for I in range(len(arrBitInts)):
        arrBitInts[I] = int(arrBitInts[I], 2)
        
        
    

    #masking pattern and boolean associated with said pattern
    sMask = ''

    for I in range(2, len(encoding_arg)):
        sMask = sMask + encoding_arg[I]
        
    def booleanCreate(y, x):
        if sMask == '000':
            if 1 == 0:
                return(True)
            else:
                return(False)
        elif sMask == '001':
            if y % 2 == 0:
                return(True)
            else:
                return(False)
        elif sMask == '010':
            if x % 3 == 0:
                return(True)
            else:
                return(False)
        elif sMask == '011':
            if (x + y) % 3 == 0:
                return(True)
            else:
                return(False)
        elif sMask == '100':
            if (x // 3 + y // 2) % 2 == 0:
                return(True)
            else:
                return(False)
        elif sMask == '101':
            if (x * y) % 2 + (x * y) % 3 == 0:
                return(True)
            else:
                return(False)
        elif sMask == '110':
            if ((x * y) % 2 + (x * y) % 3) % 2 == 0:
                return(True)
            else:
                return(False)
        elif sMask == '111':
            if ((x + y) % 2 + (x * y) % 3) % 2 == 0:
                return(True)
            else:
                return(False)    

    #creation of grid to be used 

    arrGrid = [[0 for i in range(0, n_size)] for j in range(0, n_size)]

    #intitialise position pattern 

    if pp_size % 4 == 0:
        arr = [[0 for i in range(pp_size)] for j in range(pp_size)]

        for row in range(0, len(arr) - 1):
            for col in range(0, len(arr) - 1):
                if row % 2 == 0 and row == col:
                    for row in range(col, len(arr) - col - 1):
                        arr[row][col] = 1
                        arr[col][row] = 1
                        arr[len(arr) - col - 2][row] = 1
                        arr[row][len(arr) - col - 2] = 1
                    
        arr[pp_size // 2 - 1][pp_size// 2 - 1] = 1
    else: 
        arr = [[1 for i in range(pp_size)] for j in range(pp_size)]

        for row in range(0, len(arr) - 1):
            for col in range(0, len(arr) - 1):
                if row % 2 == 0 and row == col:
                    for row in range(col, len(arr) - col - 1):
                        arr[row][col] = 0
                        arr[col][row] = 0
                        arr[len(arr) - col - 2][row] = 0
                        arr[row][len(arr) - col - 2] = 0
                    
        arr[pp_size // 2 - 1][pp_size// 2 - 1] = 1

    #top right position pattern

    arrNE = [[0 for i in range(pp_size)] for j in range(pp_size)]
    for row in range(0,len(arr)):
        for col in range(0, len(arr)):
            arrNE[row][col] = arr[row][pp_size - 1 - col]

    #bottom left position pattern 
    arrSE = [[0 for i in range(pp_size)] for j in range(pp_size)]

    for row in range(0,len(arr)):
        for col in range(0, len(arr)):
            arrSE[row][col] = arr[pp_size - 1 - row][col]

    #allignment pattern 
    arrAll = [[0 for i in range(al_size)] for j in range(al_size)]

    for row in range(0, len(arrAll)):
            for col in range(0, len(arrAll)):
                if row % 2 == 0 and row == col:
                    for row in range(col, len(arrAll) - col):
                        arrAll[row][col] = 1
                        arrAll[col][row] = 1
                        arrAll[len(arrAll) - col - 1][row] = 1
                        arrAll[row][len(arrAll) - col - 1] = 1

    #putting markers onto grid 
    #addition of 1 size results in esuring space for position patterns and formatting regions 

    for y in range(pp_size):
        for x in range(pp_size):
            arrGrid[y][x] = '*'
            
    for y in range(pp_size):
        for x in range(pp_size):
            arrGrid[y][n_size - x - 1] = '*'
            
    for y in range(pp_size):
        for x in range(pp_size):
            arrGrid[n_size - y - 1][x] = '*'

    #allignment size markers 
    for y in range(al_size):
        for x in range(al_size):
            arrGrid[n_size - pp_size - 1 + y][n_size - pp_size - 1 + x] = '*'
            
    #timing strip markers        

    #placing information onto qr code followed up by padding bits for snake pattern

    if encoding_arg[1] == '0':
        
        y = 0 
        count = 0 
        terCount = 0
        padCount = 0
        while y < n_size:
            for x in range(0, n_size):
                if count < lenBit:
                    if y % 2 == 0:
                        if arrGrid[y][x] != '*':
                            arrGrid[y][x] = int(sBit[count])
                            count += 1
                    else: 
                        if arrGrid[y][n_size - x - 1] != '*':
                            arrGrid[y][n_size - x - 1] = int(sBit[count])
                            count += 1
                else:
                    if arrGrid[y][x] != '*' and y % 2 == 0:
                        if padCount == len(arrPadding):
                            padCount = 0
                        arrGrid[y][x] = arrPadding[padCount]
                        padCount += 1
                    elif arrGrid[y][n_size - x - 1] != '*' and y % 2 != 0:
                        if padCount == len(arrPadding):
                            padCount = 0
                        arrGrid[y][n_size - x - 1] = arrPadding[padCount]
                        padCount += 1    
            
            y = y + 1              
         #masking pattern

        for y in range(n_size):
            for x in range(n_size):
                if booleanCreate(y, x) == True:
                    if arrGrid[y][x] == 1:
                        arrGrid[y][x] = 0
                    elif arrGrid[y][x] == 0:
                        arrGrid[y][x] = 1
    if encoding_arg[1] == '1':
        #placing format information region blockers 
        
        xp = pp_size
        for y in range(0, pp_size + 1):
            arrGrid[y][xp] = '*'
            arrGrid[xp][y] = '*'
        
            
        for y in range(pp_size, pp_size + 1):
            for x in range(pp_size):
                arrGrid[y][n_size - x - 1] = '*'
            
        for y in range(pp_size):
            for x in range(pp_size, pp_size + 1):
                arrGrid[n_size - y - 1][x] = '*'
                
        #placing timing strip markers 
        
        p = pp_size - 2
        
        for I in range(pp_size, pp_size + 9):
            arrGrid[p][I] = 'T'
            arrGrid[I][p] = 'T'
            
        #place information by real layout
        intCount = 0 
        sIntro = '0100'+ lenByte 
        bitCount = 0
        count = 7
        col = 0
        row = 0
        terCount = 0
        padCount = 0
        padBits = 0
        errCount = 0
       
        arrError = get_error_codewords(arrBitInts, 16)
        for I in range(len(arrError)):
            arrError[I] = format((arrError[I]), '08b')
            
        for I in range(len(arrError)):
            sErrBits = sErrBits + arrError[I]
            
        count = 0
        
        #encoded message 
        while col < n_size:    
            while row < n_size and bitCount < len(sErrBits) - 1:
                if col < 18:
                    if col % 4 == 0:
                        if arrGrid[n_size - row - 1][n_size - col - 1] != 'T' and arrGrid[n_size - row - 1][n_size - col - 1] != '*':    
                            arrGrid[n_size - row - 1][n_size - col - 1] = sErrBits[count]
                            count += 1
                            if count == len(sErrBits):
                                break
                            
                                
                        if arrGrid[n_size - row - 1][n_size - col - 2] != 'T' and arrGrid[n_size - row - 1][n_size - col - 2] != '*': 
                            arrGrid[n_size-row-1][n_size-col-2] = sErrBits[count]
                            count += 1
                            if count == len(sErrBits):
                                break
                            
                    if col % 4 != 0 and col % 2 == 0:
                        if arrGrid[row][n_size - col - 1] != 'T' and arrGrid[row][n_size - col - 1] != '*': 
                            arrGrid[row][n_size - col - 1] = sErrBits[count]
                            count += 1
                            if count == len(sErrBits):
                                break
                                
                        if arrGrid[row][n_size- col - 2] != 'T' and arrGrid[row][n_size - col - 2] != '*': 
                            arrGrid[row][n_size-col-2] = sErrBits[count]
                            count += 1
                            if count == len(sErrBits):
                                break
                elif col > 18:
                    if (col - 2) % 4 == 0:
                        if arrGrid[n_size - row - 1][n_size - col] != 'T' and arrGrid[n_size - row - 1][n_size - col] != '*': 
                             
                            arrGrid[25 - row - 1][25 - col] = sErrBits[count]
                            count += 1
                            if count == len(sErrBits):
                                break
                            
                                
                        if arrGrid[25 - row - 1][25 - col - 1] != 'T' and arrGrid[25 - row - 1][25 - col - 1] != '*': 
                            arrGrid[25-row-1][25-col-1] = sErrBits[count]
                            count += 1
                            if count == len(sErrBits):
                                break
                            
                    if (col - 2) % 4 != 0 and (col - 2) % 2 == 0:
                        if arrGrid[row][25 - col] != 'T' and arrGrid[row][25 - col] != '*': 
                            arrGrid[row][25 - col] = sErrBits[count]
                            count += 1
                            if count == len(sErrBits):
                                break
                                
                        if arrGrid[row][25- col - 1] != 'T' and arrGrid[row][25 - col - 1] != '*': 
                            arrGrid[row][25-col-1] = sErrBits[count]
                            count += 1
                            if count == len(sErrBits):
                                break
                       
                if bitCount >= len(arrBit):
                    break    
                row += 1
            col += 2
            row = 0
                
        
        #masking pattern
        
        for y in range(n_size):
            for x in range(n_size):
                if booleanCreate(y, x) == True:

                    if str(arrGrid[y][x]) == '1':
                        (arrGrid[y][x]) = '0'
                    elif str(arrGrid[y][x]) == '0':
                        arrGrid[y][x] = '1'
                  
        #generate information patterns 
    
        formPat = get_format_information_bits(encoding_arg[0] + encoding_arg[1], encoding_arg[2] + encoding_arg[3] + encoding_arg[4])
        #place information patterns
        #least to middle 
        
        p = pp_size
        fCount = 0
        fAlt = 0
        for y in range(0, pp_size + 1):
            if arrGrid[y][p] != 'T':
                arrGrid[y][p] = formPat[14 - fCount]
                fCount += 1
                
        for y in range(0, pp_size):
            arrGrid[p][n_size - 1 - y] = formPat[14 - fAlt]
            fAlt += 1
          
        for y in range(0, pp_size):
            if arrGrid[p][p - y - 1] != 'T':
                arrGrid[p][p - y - 1] = formPat[14- fCount]
                
                fCount += 1
        
        for y in range(0, pp_size - 1):
            if arrGrid[n_size - p + y][p] != 'T':
                arrGrid[n_size - p + y + 1][p] = formPat[14 - fAlt]
                fAlt += 1
                
        #place timing strip information 
        for I in range(len(arrTiming)):
            arrGrid[p - 2][p + I] = arrTiming[I]
            arrGrid[p + I][p - 2] = arrTiming[I]
        
        #placing dark spot 
        arrGrid[17][8] = '1'
   
    
                
    #placing position patterns and allignment patterns
    
    for y in range(0, pp_size):
        for x in range(0, pp_size):
            arrGrid[y][x] = arr[y][x]
            arrGrid[y][n_size - pp_size + x] = arrNE[y][x]
            arrGrid[n_size - pp_size + y][x] = arrSE[y][x]
    for y in range(0, al_size):
        for x in range(0, al_size):
            arrGrid[n_size - pp_size - 1 + y][n_size - pp_size - 1 + x] = arrAll[y][x]
            
    #output
    if encoding_arg[0] == '0':
        
        for y in range(n_size):
            string = ''
            for x in range(n_size):
                string = string + ' ' + str(arrGrid[y][x])

            stdio.writeln(string)
            
    if encoding_arg[0] == '1':
        stddraw.setCanvasSize(500, 500)

        stddraw.setXscale(0, n_size + 8)
        stddraw.setYscale(0, n_size + 8)
        #size of squares relative to scale
        for y in range(n_size):
            for x in range(n_size):
                if str(arrGrid[y][x]) == '1':
                    stddraw.setPenColor(stddraw.BLACK)
                elif str(arrGrid[y][x]) == '0':
                    stddraw.setPenColor(stddraw.WHITE)
                stddraw.filledSquare(x + 4, n_size - y + 4, 0.505)
                
        
        stddraw.save('output.png')
    
if __name__ == "__main__":
    main()       
     
    

