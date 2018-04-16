import math




def main():
    fin = open("input.txt","r+")


    # data stored in dictionary of dictionaries of how much this person owes and how much each other person owes them

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
            
    # print current state before any shifting
    PrintPaymentState(data,"Initial Data")
    
    # remove the diagonal
    for key in data.keys():
        data[key]["TheyOweMe"][key]=0
        data[key]["IOweThem"][key]=0
        
    # print current state before any shifting
    PrintPaymentState(data,"Diagonal Removal - don't owe yourself things")
        
    # one-on-one payments
    for key1 in data.keys():
        for key2 in data.keys():
        
            print "\n\nReady to remove overlap : ",key1,"/",key2
        
            data = RemoveOneOnOne(data,key1,key2)

            # print current state before any shifting
            PrintPaymentState(data,key1+"/"+key2+" removal")
        
    # payment in triplets
    for key1 in data.keys():
        for key2 in data.keys():
            for key3 in data.keys():
            
                print "\n\nReorganizing Triplet : ",key1,"/",key2,"/",key3
            
                data = RemoveTriplet(data,key1,key2,key3)
            
    
                PrintPaymentState(data,key1+"/"+key2+"/"+key3+" removal")
        

####################################
        
def PrintPaymentState(dataMatrix, message):

    print "\nSummary : ",message

    header = "(down) owes (right)  |"
    for key1 in sorted(dataMatrix.keys()):
        header += "{0:>10}".format(key1)
        
    headerline=""
    for i in range(len(header)):
        headerline+="-"

    #print "Using IOweThem"
    print header
    print headerline
    for key1 in sorted(dataMatrix.keys()):
    
        line = ""
        line += "{0:<20} |".format(key1)
        
        for key2 in sorted(dataMatrix.keys()):
            line += "{0:10}".format(dataMatrix[key1]["IOweThem"][key2])
        
        print line

#     print "Using TheyOweMe"
#     print header
#     print headerline
#     for key1 in sorted(dataMatrix.keys()):
#         
#         line = ""
#         line += "{0:<20} |".format(key1)
#         
#         for key2 in sorted(dataMatrix.keys()):
#             line += "{0:10}".format(dataMatrix[key2]["TheyOweMe"][key1])
#         
#         print line
        
        
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
        

def RemoveTriplet(dataMatrix,name1,name2,name3):        

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
    
    name1_owes_name2 = dataMatrix[name1]["IOweThem"][name2]
    name1_owes_name3 = dataMatrix[name1]["IOweThem"][name3]

    name2_owes_name1 = dataMatrix[name2]["IOweThem"][name1]
    name2_owes_name3 = dataMatrix[name2]["IOweThem"][name3]

    name3_owes_name1 = dataMatrix[name3]["IOweThem"][name1]
    name3_owes_name2 = dataMatrix[name3]["IOweThem"][name2]


#     print "name1_owes_name2 : ",    name1_owes_name2
#     print "name1_owes_name3 : ",    name1_owes_name3
# 
#     print "name2_owes_name1 : ",    name2_owes_name1
#     print "name2_owes_name3 : ",    name2_owes_name3
# 
#     print "name3_owes_name1 : ",    name3_owes_name1
#     print "name3_owes_name2 : ",    name3_owes_name2

    # there should be at least three of these that are 0 if we have reduced properly
    # N(zero) = 0 --> reduced improperly in previous step
    # N(zero) = 1 --> reduced improperly in previous step
    # N(zero) = 2 --> reduced improperly in previous step
    # N(zero) = 3 --> NEEDS REDUCTION
    # N(zero) = 4 --> reduced maximally
    # N(zero) = 5 --> reduced maximally
    # N(zero) = 6 --> reduced maximally
    
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
    
    if NZero<3:
        print "The reduction in the one-to-one step was not fully done --> CHECK THIS AGAIN"
    elif NZero>=4:
        print "This is reduced maximally, nothing will happen"
    elif NZero==3:
    
        print "Reorganizing this triplet of payments - enter any value to confirm"
        input()
        
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
        
        print "Check that the reorganization was done properly"
        input()
        
        
    
    return dataMatrix
        
        
if __name__== "__main__":
  main()
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  