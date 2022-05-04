import csv
cats = ["food","veg","meat","drink","buildings","animals","people","transport1","transport2","readable","animalsubject"]
wordlist_files = ["keskows5_food.txt","keskows5_veg.txt","keskows5_meat.txt","keskows5_drink.txt","keskows5_buildings.txt","keskows5_animals.txt","keskows5_people.txt","keskows5_trans1.txt","keskows5_trans2.txt","keskows5_readable.txt","keskows5_verbsanimalsubject.txt"]

food = []
veg = []
meat = []
drink = []
buildings = []
animals = []
people = []
transport1 = []
transport2 = []
readable = []
verbs_animalsubject = []

food_g = []
veg_g = []
meat_g = []
drink_g = []
buildings_g = []
animals_g = []
people_g = []
transport1_g = []
transport2_g = []
readable_g = []

food_v = []
veg_v = []
meat_v = []
drink_v = []
buildings_v = []
animals_v = []
people_v = []
transport1_v = []
transport2_v = []
readable_v = []

food_a = []
veg_a = []
meat_a = []
drink_a = []
buildings_a = []
animals_a = []
people_a = []
transport1_a = []
transport2_a = []
readable_a = []

food_n_e = []
veg_n_e = []
meat_n_e = []
drink_n_e = []
buildings_n_e = []
animals_n_e = []
people_n_e = []
transport1_n_e = []
transport2_n_e = []
readable_n_e = []

food_v_e = []
veg_v_e = []
meat_v_e = []
drink_v_e = []
buildings_v_e = []
animals_v_e = []
people_v_e = []
transport1_v_e = []
transport2_v_e = []
readable_v_e = []

food_a_e = []
veg_a_e = []
meat_a_e = []
drink_a_e = []
buildings_a_e = []
animals_a_e = []
people_a_e = []
transport1_a_e = []
transport2_a_e = []
readable_a_e = []
verbs_animalsubject_e = []

nouns_all = [food,veg,meat,drink,buildings,animals,people,transport1,transport2,readable]
nouns_all_g = [food_g,veg_g,meat_g,drink_g,buildings_g,animals_g,people_g,transport1_g,transport2_g,readable_g]
verbs_all = [food_v,veg_v,meat_v,drink_v,buildings_v,animals_v,people_v,transport1_v,transport2_v,readable_v,verbs_animalsubject]
adj_all = [food_a,veg_a,meat_a,drink_a,buildings_a,animals_a,people_a,transport1_a,transport2_a,readable_a]
english_nouns_all = [food_n_e,veg_n_e,meat_n_e,drink_n_e,buildings_n_e,animals_n_e,people_n_e,transport1_n_e,transport2_n_e,readable_n_e]
english_verbs_all = [food_v_e,veg_v_e,meat_v_e,drink_v_e,buildings_v_e,animals_v_e,people_v_e,transport1_v_e,transport2_v_e,readable_v_e,verbs_animalsubject_e]
english_adj_all = [food_a_e,veg_a_e,meat_a_e,drink_a_e,buildings_a_e,animals_a_e,people_a_e,transport1_a_e,transport2_a_e,readable_a_e]


for i in wordlist_files:
    reader = csv.reader(file(i),delimiter = ',',skipinitialspace=True)
    for row in reader:
        w = row[0]
        POS = row[1]
        gender = row[2]
        cat = row[3]
	english = row[4]
        for c in range(len(cats)):
            if cat == cats[c]:
                if POS == "noun":
                    nouns_all[c].append(w)
                    nouns_all_g[c].append(gender)
		    english_nouns_all[c].append(english)			
                if POS == "verb":
                    verbs_all[c].append(w) 
		    english_verbs_all[c].append(english)
		if POS == "adj":
                    adj_all[c].append(w) 
		    english_adj_all[c].append(english)			
#print nouns_all
#print verbs_all
#print adj_all
