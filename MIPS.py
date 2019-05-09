##################################
# MIPS Processor by Nigel Jacobs #
# April 2019                     #
##################################

##################################
# Add - performs binary addition #
##################################

def Add(a, b):
    result = '' 
    carry = 0
    for o in range(15, -1, -1): 
        r = carry 
        r += 1 if a[o] == '1' else 0
        r += 1 if b[o] == '1' else 0
        result = ('1' if r % 2 == 1 else '0') + result 
        carry = 0 if r < 2 else 1     
    if carry !=0 : result = '1' + result 
    return result

###################################
# B2D - converts binary string to #
# a decimal string                #
###################################

def B2D(num):
    numb = int(num)
    binary1 = numb
    decimal, i, n = 0, 0, 0
    while(numb != 0): 
        dec = numb % 10
        decimal = decimal + dec * pow(2, i) 
        numb = numb//10
        i += 1
    return decimal

###################################
# B2H - converts binary string to #
# a hexadecimal string            #
###################################

def B2H(binary):
    hans = 0
    ah =""
    for k in range(0, 16, 4):
        if binary[k] == '1':
            hans = hans + 8
        if binary[k+1] == '1':
            hans = hans + 4
        if binary[k+2] == '1':
            hans = hans + 2
        if binary[k+3] == '1':
            hans = hans + 1
        
        if hans > 9:
            ch = chr(hans + 55)
            ah += ch
        else:
            ah += str(hans)                
    return ah

#################################################
# I_Format - performs I-format MIPS Instruction #
# (lw, sw, addi, bne, beq)                      #
#################################################

def I_Format(dec, regst, mems, pc):
    op = int(dec[0:6], 2)
    rs = int(dec[6:11],2)
    rt = int(dec[11:16],2)
    imm = int(dec[-16:], 2)
    j = bin(int(regst[rs],16))[2:].zfill(16)
    k = bin(int(regst[rt],16))[2:].zfill(16)
    l = bin(imm)[2:].zfill(16)
    bans = ""
    if op == 35:
        print("lw ${}, {}(${})".format(rt,imm,rs))
        bans = Add(j,l)
        ans = mems[B2D(bans)]
        print("${} = {}".format(rt, ans))
        regst[rt] = ans
    elif op == 43:
        print("sw ${}, {}(${})".format(rt,imm,rs))
        bans = Add(j,l)
        ans = regst[B2D(bans)]
        print("mem[{}] = {}".format(rt, ans))
        mems[rt] = ans
    elif op == 4:
        print("beq ${},${}, {}".format(rs,rt,imm))
        if regst[rs] == regst[rt]:
            pc = imm  
    elif op == 5:
        print("bne ${},${}, {}".format(rs,rt,imm))
        if regst[rs] != regst[rt]:
            pc = imm
    elif op == 8:
        print("addi ${},${}, {}".format(rt,rs,imm))
        bans = Add(j,l)
        ans = B2H(bans)
        print("${} = {}".format(rt, ans))
        regst[rt] = ans
    return None

#################################################
# R_Format - performs R-format MIPS Instruction #
# (and, or, add, sub)                           #
#################################################   

def R_Format(d, regs):
    rd = int(d[16:21],2)
    rs = int(d[6:11],2)
    rt = int(d[11:16],2)
    func = int(d[-6:], 2)
    j = bin(int(regs[rs],16))[2:].zfill(16)
    k = bin(int(regs[rt],16))[2:].zfill(16)
    bans = ""
    if func == 36:
        print("and ${},${},${}".format(rd,rs,rt))
        for i in range(0,16):
            n = int(j[i]) & int(k[i])
            bans += str(n)
    elif func == 37:
        print("or ${},${},${}".format(rd,rs,rt))
        for i in range(0,16):
            n = int(j[i]) | int(k[i])
            bans += str(n)
    elif func == 32:
        print("add ${},${},${}".format(rd,rs,rt))
        bans = Add(j,k)
    elif func == 34:
        print("sub ${},${},${}".format(rd,rs,rt))
        result = '' 
        carry = 0
        for i in range(15, -1, -1): 
            s = int(j[i]) - int(k[i])
            if s < 0:
                if carry == 0:
                    carry = 1
                    result = result + "1"
                else:
                    result = result + "0"
            elif s == 0:
                if carry == 0:
                    result = result + "0"
                    carry = 0   
                else:
                    result = result + "1" 
            i = i - 1
            if carry>0:
                result = result + "1"
        bans = result
    else:
        print("This operation is not included in this program.")
    print(bans)
    ans = B2H(bans)
    print("${} = {}".format(rd, ans))
    regs[rd] = ans
    return None

###################################################
# PrintRegisters - prints what is inside registers#
# and memory locations                            #
###################################################

def PrintRegisters(regis, memz, pc):
    for item in range(len(regis)):
        print("${} = {}         mem[{}] = {}".format(item, regis[item], item, memz[item]))
    print(" ")
    print("PC = {}".format(pc))
    return None

################
# Driver Code  #
################

reg = ['0000','0009', '002A', '0014', '0003', 'FF12', '0076', 'FFC8', '0003', '0025','C062', '0056', 'FF29']
mem = ['4100','0101', '0102', '0103', '0104', '0105', '0106', '0107', '0008', '0109', '0110', '0111', '0112']
PC = '13'
PrintRegisters(reg, mem, PC)
end = False
while end == False:
    hex = input("Please enter a hexadecimal: ")
    n = bin(int(hex,16))[2:].zfill(32)
    print(n)
    if '1' in n[0:6]:
        I_Format(n, reg, mem, PC)
    else:
        R_Format(n, reg)
    print(" ")
    PrintRegisters(reg, mem, PC)
    print(" ")
    con = input("Would you like to do another operation?(Y/N): ")
    while con != 'Y' and con != 'N':
        con = input("Please enter a valid value: ")
    if con == 'N':
        end = True
