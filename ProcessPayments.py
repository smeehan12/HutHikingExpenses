##########################################
#
# For sorting out hiking expenses
#
# Author : Sam Meehan
#
# Input : text file that is formatted as
#     name1  total_payed_1
#     name2  total_payed_2
#     name3  total_payed_3
#     ...
#
# This will perform the reduction to the minimal amount of payments required to equalize everyone to have payed the same as everyone else
#
#
#
##########################################
import argparse
import math
import os.path

def main():


    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest="input", default="input.txt")

    results = parser.parse_args()
    print "input : ",results.input
    
    if os.path.exists(results.input)==False:
        print "That input file does not exist : ",results.input
        return

    fin = open(results.input,"r+")

    #########################################
    # data will be stored in dictionary with one key per individual with the following fiels
    # 'TotalPayed' [double]     : total amount of money payed by that individual
    # 'TheyOweMe'  [dictionary] : dictionary of the other people in the group and how much they owe me
    # 'IOweThem'   [dictionary] : dictionary of the other people in the group and how much I owe them
    #########################################
    
    data = {}

    for line in fin.readlines():

        if len(line.strip().split())<2:
            print "DONE READING DATA"
            print "Last line was : ",line.strip()
            break
        
        name  = line.strip().split()[0]
        total = float(line.strip().split()[1])
    
        data[name]={}
    
        data[name]["TotalPayed"] = total
    
    # check the initial info
    for key in data.keys():
        print "name={0:10}   info={1:50}".format(key,data[key])
            
            
    NPeople = len(data.keys())

    print "How many people were on the trip : ",NPeople
    
    # make the user validate the info
    print "Does the raw info above look correct? - enter any character to proceed"
    input()
            
    # make the entry for how much every else owes you and how much you owe them
    for key1 in data.keys():
        data[key1]["TheyOweMe"]={}
        data[key1]["IOweThem"]={}
    
        # calculate initial value that other people owe me
        for key2 in data.keys():
            data[key1]["TheyOweMe"][key2] = int(math.ceil(data[key1]["TotalPayed"]/NPeople))
    
        # calculate initial value that I owe to other people
        for key2 in data.keys():
            data[key1]["IOweThem"][key2] = int(math.ceil(data[key2]["TotalPayed"]/NPeople))
    
    
    # check the initial info
    for key1 in data.keys():
        print "==========================="
        print key1
        print " TotalPayed : ",data[key1]["TotalPayed"]
        print " Owes ----"
        for key2 in data.keys():
            print "  {0:10}  {1:10}".format(key2,data[key1]["IOweThem"][key2])
        print " Is Owed By----"
        for key2 in data.keys():
            print "  {0:10}  {1:10}".format(key2,data[key1]["TheyOweMe"][key2])
        print "==========================="
            
    # make the user validate the info
    print "Does the processed info look correct? - enter any character to proceed"
    input()
            
    # print current state before any shifting
    PrintPaymentState(data,"Initial Data")
    
    # make the user validate the info
    print "Does the payment matrix look correct? - enter any character to proceed"
    input()
    
    #################################################################
    # STEP 0 - remove the diagonal
    # It makes no sense to pay back yourself
    #################################################################
    print "STEP0 : Removing the diagonal portion where one pays themselves"
    for key in data.keys():
        data[key]["TheyOweMe"][key]=0
        data[key]["IOweThem"][key]=0
        
    # print current state before any shifting
    PrintPaymentState(data,"Diagonal Removal - don't owe yourself things")

    # make the user validate the info
    print "Does the payment matrix look correct? - enter any character to proceed"
    input()

    #################################################################
    # STEP 1 - remove the one-to-one payment
    # No sense to pay me 40 and then me pay you back 20
    #################################################################
    for key1 in data.keys():
        for key2 in data.keys():
        
            print "\n\nReady to remove overlap : ",key1,"/",key2
        
            data = RemoveOneOnOne(data,key1,key2)

            # print current state before any shifting
            PrintPaymentState(data,key1+"/"+key2+" removal")
        
    #################################################################
    # STEP 2 - remove the payments between three individuals
    # I bit more complicated but reduces the money shifting between
    # three people
    #################################################################
    for key1 in data.keys():
        for key2 in data.keys():
            for key3 in data.keys():
            
                print "\n\nReorganizing Triplet : ",key1,"/",key2,"/",key3
            
                performedReordering,data = RemoveTriplet(data,key1,key2,key3)
            
                PrintPaymentState(data,key1+"/"+key2+"/"+key3+" removal")
            
                if performedReordering:
                    print "STEP2 - Check that the reorganization was done properly - enter any character to proceed"
                    input()

############################################################################################################

########################################################
#
# Prints the payment matrix of who owe's who what
#
########################################################
def PrintPaymentState(dataMatrix, message, debug=False):

    print "\nSummary : ",message

    header = "(down) owes (right)  |"
    for key1 in sorted(dataMatrix.keys()):
        header += "{0:>10}".format(key1)
        
    headerline=""
    for i in range(len(header)):
        headerline+="-"

    if debug:
        print "Using IOweThem"

    print header
    print headerline
    for key1 in sorted(dataMatrix.keys()):
    
        line = ""
        line += "{0:<20} |".format(key1)
        
        for key2 in sorted(dataMatrix.keys()):
            line += "{0:10}".format(dataMatrix[key1]["IOweThem"][key2])
        
        print line

    if debug:
        print "Using TheyOweMe"
        print header
        print headerline
        for key1 in sorted(dataMatrix.keys()):
        
            line = ""
            line += "{0:<20} |".format(key1)
        
            for key2 in sorted(dataMatrix.keys()):
                line += "{0:10}".format(dataMatrix[key2]["TheyOweMe"][key1])
        
            print line
        
########################################################
#
# Removes the payments from one-on-one payments
# So if person1 owes person2 30CHF and
# person2 owes person1 50CHF, then after this,
# person2 will only owe person1 20CHF
#
########################################################
def RemoveOneOnOne(dataMatrix, name1, name2):

    print "name1 : ",name1
    print "name2 : ",name2

    name1_owes_name2 = dataMatrix[name1]["IOweThem"][name2]
    name2_owes_name1 = dataMatrix[name1]["TheyOweMe"][name2]
    
    print "name1_owes_name2 : ",name1," owes ",name2," - ",name1_owes_name2
    print "name2_owes_name1 : ",name2," owes ",name1," - ",name2_owes_name1

    if name1_owes_name2 > name2_owes_name1:
        print "CASE1"
        name1_owes_name2 = name1_owes_name2 - name2_owes_name1
        name2_owes_name1 = 0
        
    elif name1_owes_name2 < name2_owes_name1:
        print "CASE2"
        name2_owes_name1 = name2_owes_name1 - name1_owes_name2
        name1_owes_name2 = 0
        

    elif name1_owes_name2 == name2_owes_name1:
        print "CASE3"
        name1_owes_name2 = 0
        name2_owes_name1 = 0

    else:
        print "*********** CHECK ME ************"
        
    print "new-name1_owes_name2 : ",name1," owes ",name2," - ",name1_owes_name2
    print "new-name2_owes_name1 : ",name2," owes ",name1," - ",name2_owes_name1
        
    dataMatrix[name1]["TheyOweMe"][name2] = name2_owes_name1
    dataMatrix[name1]["IOweThem"][name2]  = name1_owes_name2

    dataMatrix[name2]["TheyOweMe"][name1] = name1_owes_name2
    dataMatrix[name2]["IOweThem"][name1]  = name2_owes_name1

    return dataMatrix
        
########################################################
#
# This removes the triplet payments, so if 
# p1 owes p2 40CHF
# p2 owes p3 20CHF
# p1 owes p3 15CHF
#
# then after this, it should only be the case that
# p1 owes p2 20CHF
# p1 owes p3 35CHF
#
# It is necessary that the one-on-one reduction (above) be performed first
# or else this will complain to you
#
########################################################
def RemoveTriplet(dataMatrix,name1,name2,name3,debug=False):        

    ########################
    # rank the people as
    # p1 : 
    #  - pays p2
    #  - pays p3
    # p2 : 
    # - is payed by p1
    # - pays p2
    # p3 : 
    # - is payed by p1
    # - is payed by p2
    ########################
    
    name1_owes_name2 = dataMatrix[name1]["IOweThem"][name2]
    name1_owes_name3 = dataMatrix[name1]["IOweThem"][name3]

    name2_owes_name1 = dataMatrix[name2]["IOweThem"][name1]
    name2_owes_name3 = dataMatrix[name2]["IOweThem"][name3]

    name3_owes_name1 = dataMatrix[name3]["IOweThem"][name1]
    name3_owes_name2 = dataMatrix[name3]["IOweThem"][name2]

    if debug:
        print "name1_owes_name2 : ",    name1_owes_name2
        print "name1_owes_name3 : ",    name1_owes_name3

        print "name2_owes_name1 : ",    name2_owes_name1
        print "name2_owes_name3 : ",    name2_owes_name3

        print "name3_owes_name1 : ",    name3_owes_name1
        print "name3_owes_name2 : ",    name3_owes_name2

    ########################
    # there should be at least three of these that are 0 if we have reduced properly
    # N(zero) = 0 --> reduced improperly in previous step
    # N(zero) = 1 --> reduced improperly in previous step
    # N(zero) = 2 --> reduced improperly in previous step
    # N(zero) = 3 --> NEEDS REDUCTION
    # N(zero) = 4 --> reduced maximally
    # N(zero) = 5 --> reduced maximally
    # N(zero) = 6 --> reduced maximally
    ########################
    
    NZero = 0
    
    if name1_owes_name2==0:
        NZero+=1
    if name1_owes_name3==0:
        NZero+=1
    if name2_owes_name1==0:
        NZero+=1
    if name2_owes_name3==0:
        NZero+=1
    if name3_owes_name1==0:
        NZero+=1
    if name3_owes_name2==0:
        NZero+=1
    
    print "NZeros = ",NZero
    
    # to pass to the outside world for printing
    performedReordering = False
    
    if NZero<3:
        print "The reduction in the one-to-one step was not fully done --> CHECK THIS AGAIN"
    elif NZero>=4:
        print "This is reduced maximally, nothing will happen"
    elif NZero==3:
    
        # to pass to the outside world for printing
        performedReordering=True
    
        print "Reorganizing this triplet of payments - you will be asked to confirm the correctness"
        
        # reorder the people 
        p1="X"
        p2="X"
        p3="X"
        
        if name1_owes_name2==0 and name1_owes_name3==0:
            p3=name1
        elif (name1_owes_name2==0 and name1_owes_name3!=0) or (name1_owes_name2!=0 and name1_owes_name3==0):
            p2=name1
        elif name1_owes_name2!=0 and name1_owes_name3!=0:
            p1=name1
        else:
            print "HOW DID YOU GET HERE?"
            
            
        if name2_owes_name1==0 and name2_owes_name3==0:
            p3=name2
        elif (name2_owes_name1==0 and name2_owes_name3!=0) or (name2_owes_name1!=0 and name2_owes_name3==0):
            p2=name2
        elif name2_owes_name1!=0 and name2_owes_name3!=0:
            p1=name2
        else:
            print "HOW DID YOU GET HERE?"
        
        if name3_owes_name1==0 and name3_owes_name2==0:
            p3=name3
        elif (name3_owes_name1==0 and name3_owes_name2!=0) or (name3_owes_name1!=0 and name3_owes_name2==0):
            p2=name3
        elif name3_owes_name1!=0 and name3_owes_name2!=0:
            p1=name3
        else:
            print "HOW DID YOU GET HERE?"
            
        print "Owes both people  : ",p1
        print "Owes only one     : ",p2
        print "Gets paid by both : ",p3
        
        # different cases to keep all payments positive
        if dataMatrix[p1]["IOweThem"][p2]>=dataMatrix[p2]["IOweThem"][p3]:
            p1_owes_p2 = dataMatrix[p1]["IOweThem"][p2]-dataMatrix[p2]["IOweThem"][p3]
            p1_owes_p3 = dataMatrix[p1]["IOweThem"][p3]+dataMatrix[p2]["IOweThem"][p3]
            p2_owes_p3 = 0
            p2_owes_p1 = 0
            p3_owes_p1 = 0
            p3_owes_p2 = 0
        else:
            p1_owes_p2 = 0
            p1_owes_p3 = dataMatrix[p1]["IOweThem"][p3]+dataMatrix[p1]["IOweThem"][p2]
            p2_owes_p3 = dataMatrix[p2]["IOweThem"][p3]-dataMatrix[p1]["IOweThem"][p2]
            p2_owes_p1 = 0
            p3_owes_p1 = 0
            p3_owes_p2 = 0
        
        # now set these equal to the actual values in the matrix given the names
        # modifying the matrix
        dataMatrix[p1]["IOweThem"][p2] = p1_owes_p2
        dataMatrix[p1]["IOweThem"][p3] = p1_owes_p3
        dataMatrix[p2]["IOweThem"][p1] = p2_owes_p1
        dataMatrix[p2]["IOweThem"][p3] = p2_owes_p3
        dataMatrix[p3]["IOweThem"][p1] = p3_owes_p1
        dataMatrix[p3]["IOweThem"][p2] = p3_owes_p2

        dataMatrix[p1]["TheyOweMe"][p2] = p2_owes_p1
        dataMatrix[p1]["TheyOweMe"][p3] = p3_owes_p1
        dataMatrix[p2]["TheyOweMe"][p1] = p1_owes_p2
        dataMatrix[p2]["TheyOweMe"][p3] = p3_owes_p2
        dataMatrix[p3]["TheyOweMe"][p1] = p1_owes_p3
        dataMatrix[p3]["TheyOweMe"][p2] = p2_owes_p3
        
    return performedReordering,dataMatrix
        
        
if __name__== "__main__":
  main()
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  