import keskows5_word

# files storing wordlists
# 1 food - keskows5_food.txt
# 2 vegtables - keskows5_veg.txt
# 3 meat - keskows5_meat.txt
# 4 drink - keskows5_drink.txt
# 5 buildings - keskows5_buildings.txt
# 6 animals - keskows5_animals.txt
# 7 people - keskows5_people.txt
# 8 transport (drive) - keskows5_trans1.txt
# 9 transport (ride) - keskows5_trans2.txt
# 10 readable - keskows5_readable.txt

cats = ["food","veg","meat","drink","buildings","animals","people","transport1","transport2","readable","animalsubject"]
wordlist_files = ["keskows5_food.txt","keskows5_veg.txt","keskows5_meat.txt","keskows5_drink.txt","keskows5_buildings.txt","keskows5_animals.txt","keskows5_people.txt","keskows5_trans1.txt","keskows5_trans2.txt","keskows5_readable.txt","keskows5_verbsanimalsubject.txt"]
w = ""
m =0
while w != "0":
    m = m + 1
    w = raw_input("Enter word - ")
    if w == "0":
        break
    POS = raw_input("Part of speech (noun/verb/adj) - ")
    n = 1
    if POS == "noun":
        gender = raw_input("Gender (m/f/c). c=collective noun Enter 0 for non-nouns - ")
    else:
        gender = str(0)
    english = raw_input("Enter word's English translation - ")
    if POS == "verb":
        a = raw_input("Can an animal perform this action? (y/n)")
	if a == "y":
	   vars()[str(m)] = keskows5_word.word(w,POS,cats[10],gender,english)   
	   vars()[str(m)].appendtofile(wordlist_files[10])

    while n != 0:
        category = raw_input("Category to add it into (1=food, 2=vegetables,3=meat,4=drink,5=buildings,6=animals,7=people,8=transport(drive),9=transport(ride),10=readable. Enter 0 to stop adding categories -")
        n = int(category)
        if n != 0:
            cat = n -1
            vars()[str(m)] = keskows5_word.word(w,POS,cats[cat],gender,english)
            vars()[str(m)].appendtofile(wordlist_files[cat])
    
