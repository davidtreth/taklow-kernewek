class word(object):
    def __init__(self,w,POS,cat,gender,english):
    # store data on a word
        self.w = w
        self.POS = POS
        self.cat = cat
        if self.POS == "noun":
            self.gender = gender 
        else:
            self.gender = "0"
	self.english=english    
    def appendtofile(self,filename):
        f = open(filename,"a")
        string = self.w + "," + self.POS + "," + self.gender + "," + self.cat + "," + self.english+"\n"
        f.write(string)

#pasty = word("pasti","noun","food","m")



#pasty.appendtofile("keskows5_food.txt")
