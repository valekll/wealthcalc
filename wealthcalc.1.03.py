# -*- coding: utf-8 -*-
"""
Created on Sun May 19 20:01:48 2019

@author: Valek
"""

'''
Notes:
    Add Monthly Income/Investment/Divestment?
'''

firstyear = True
ilength = 5 #amount of years to keep each investment
icohratio = .9 #investment to cash on hand ratio (how much to invest out of cash on hand)
maxyears = 46 #maximum number of years to track (starts from 0)
inum = 10 #investment columns
spareInc = 40000 #spare income
tim = 0 #total investments made
idatatypes = 4 #number of datatypes for investment data
mininvestment = 10000 #minimum investment
tenm = False #over 10M year
tenmyr = -1 #year it was broken
spareIncCapYr = 100 #year spare income stops coming in
spareIncApp = 000 #space income appreciation (yearly)
invTotal = 0 #total spent investing
invIncTotal = 0 #investment income total
startyear = 22 #year to start accumulating money
appreciation = .05 #yearly appreciation rate
cashflow = .06 #yearly cashflow rate
yearsonloan = 10 #number of years you get loans for
invWealthRatio = .15 #investment to wealth ratio

cidata = [[0 for x in range(inum)] for y in range (idatatypes)] #current investment data (0: income, 1: value, 2: start, 3: end)
im = [[0 for x in range(inum)] for y in range(maxyears)] #investment matrix
itotal = [0 for x in range(maxyears)] #wealth total
coh = [0 for x in range (maxyears)] #cash on hand
wtotal = [0 for x in range(maxyears)] #wealth total


#adds income to cash on hand every year
def income(x):
    if x > 0:
        coh[x] = coh[x - 1]
    #job income
    if x >= startyear and x <= spareIncCapYr:
        if not firstyear:
            global spareInc
            spareInc += spareIncApp
        coh[x] += spareInc
    #investment income
    for y in range(0, inum):
        global invIncTotal
        coh[x] += cidata[0][y]
        invIncTotal += cidata[0][y]
        im[x][y] = (cidata[1][y] / yearsonloan) + im[x - 1][y]
    totalYear(x)

#totals investment matrix and cash on hand per year
def totalYears():
    for x in range(0, maxyears):
        itotal[x] = 0
        wtotal[x] = 0
        wtotal[x] += coh[x]
        for y in range(0, inum):
            itotal[x] += im[x][y] 
        wtotal[x] += itotal[x]
        
#totals a single year for the investment matrix and cash on hand
def totalYear(x):
    itotal[x] = 0
    wtotal[x] = 0
    wtotal[x] += coh[x]
    for y in range(0, inum):
        itotal[x] += im[x][y] 
    wtotal[x] += itotal[x]
    global tenm
    global tenmyr
    if wtotal[x] > 10000000 and not tenm: 
        tenm = True
        tenmyr = x
        
#prints all non-zero values of your wealth accumulation        
def printWealthMatrix(): 
    totalYears()
    for x in range (0, maxyears):
        if wtotal[x] > 0:
            print("Age " + str(x) + ":")
            if itotal[x] > 0:
                print("Investments: " + str(format(itotal[x], ',.2f')))
                for y in range(0, inum):
                    if im[x][y] > 0:
                        print(str(format(im[x][y], ',.2f')), end='\t')
                print("")
            if coh[x] > 0:
                print("Cash on Hand: " + str(format(coh[x], ',.2f')))
            print("Net Worth: " + str(format(wtotal[x], ',.2f') + "\n"))

#prints important statistics            
def printWealthStats():
    totalYears()
    print("Total Investments Made: " + str(tim))
    print("Total Invested: " + str(format(invTotal, ',.2f')))
    print("Average Investment: " + str(format(invTotal / tim, ',.2f')))
    print("Total Income From Investments: " + str(format(invIncTotal, ',.2f')))
    print("Average Yearly Income From Investments: " + str(format(invIncTotal / (maxyears - startyear), ',.2f')))
    if tenm:
        print("Year 10M Broke: " + str(tenmyr))

def printInvestmentData(x, y):
    print("Investment Data for year " + str(x) + ":")
    print("im[" + str(x) + "][" + str(y) + "]: " + str(im[x][y]))
    print("coh[" + str(x) + "]: " + str(coh[x]))
    for i in range (0, idatatypes):
        print("cidata[" + str(i) + "][" + str(y) + "]: " + str(cidata[i][y]))

#checks if there is enough money to make a meaningful investment
def shouldInvest(x):
    if wtotal[x] > 0 and coh[x] / wtotal[x] >= invWealthRatio and coh[x] * icohratio > mininvestment:
        return True
    else:
        return False

#makes an investment with the cash on hand
def invest(x):
    global tim
    tim += 1
    for y in range (0, inum):
        if im[x][y] == 0:
            global invTotal
            im[x][y] = coh[x] * icohratio
            invTotal += im[x][y]
            coh[x] -= coh[x] * icohratio
            cidata[0][y] = im[x][y] * cashflow
            cidata[1][y] = im[x][y] * 3
            cidata[2][y] = x
            cidata[3][y] = x + ilength
            break
        elif y == inum - 1:
            print("***FAILED TO INVEST. MORE COLUMNS NEEDED.***")
        
#exits all invesments that have gone their whole duration
def divest(x):
    for y in range (0, inum):
        if cidata[3][y] == x:
            coh[x] += im[x][y]
            im[x][y] = 0
            for i in range (0, idatatypes):
                cidata[i][y] = 0

#simulates investments over the years
def simInvestments():
    for x in range (0, maxyears): 
        income(x)
        divest(x)
        #make meaningful investments
        if shouldInvest(x):
            invest(x)  
        if coh[x] > 0:
            global firstyear
            firstyear = False
    totalYears()

        
        
simInvestments()
printWealthMatrix()
printWealthStats()
