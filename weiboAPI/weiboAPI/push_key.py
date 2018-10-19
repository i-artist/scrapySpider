uidFile = open('uid.txt','r')
M_file = uidFile.readlines()
# M_file = ["5355347548","3900215081","1889728690","3818859252","1616510481","5355347548","3900215081","1889728690","3818859252","1616510481","5355347548","3900215081","1889728690","3818859252","161651048133333"]

sum = 0
n = 0
uids = ""
for UID in M_file:
    user_id = UID.replace("\n","")
    sum += 1
    n += 1
    uids += user_id + ","
    if sum == 4:
        print(uids+"\n")
        sum = 0
        uids = ""

    if n == len(M_file):
        print(uids+"\n")
