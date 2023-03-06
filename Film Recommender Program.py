import csv, difflib
from collections import Counter

usersViewingHistory = []

def loginProcedure():
    print ("Welcome back, please log in below...")
    with open('Registered Users.csv', 'r') as infile:
        reader = csv.reader(infile)
        users = {rows[0]:rows[1] for rows in reader}
    global existingUsername, existingPassword
    existingUsername = input("Please enter your username... ")
    existingPassword = input("Please enter your password... ")
    if (existingUsername in users) and (existingPassword == users[existingUsername]):
        print ("Login successful.")
    else:
        print ("Login details not recognised.")
        exit()

def addFilmsToViewingHistory():
    global usersViewingHistory
    seenFilmsQuantity = int(input("How many of these films have you seen since the last login - "))
    print("Please enter the number code for each of these films. Press enter after each entry.")        
    for i in range(seenFilmsQuantity):
        seenFilmCode = input("> ")
        with open('Films.csv') as filmsFile:
            reader = csv.DictReader(filmsFile)
            for row in reader:
                if seenFilmCode == row['Code']:
                    print ("You have selected: ", row['Film'])
                    usersViewingHistory.extend([row['Film']])
                    with open('Viewing History for {}.txt'.format(existingUsername), 'a') as open_file: 
                        open_file.write("{}\n".format(row['Film']))
        
print ("Welcome to the Python Film Recommender Program. \nPlease select an option from below.\n")
print ("1  - Register as a new user.")#DONE
print ("2  - Login as an existing user and see your last 10 viewed films.")#DONE
print ("3  - Login as an existing user and see some film suggestions.")
print ("4A - Login as an existing user and search for films using year.")#DONE
print ("4B - Login as an existing user and search for films using title.")#DONE
print ("4C - Login as an existing user and see the full list of available films.")#DONE
print ("4D - Login as an existing user and search for films using genre.")#DONE

menuChoice = input("\n> ")

if menuChoice == "1":
    print ("Welcome new user! Please answer the questions below to make an account...")
    newUsername = input("Please pick a username - ")
    newPassword = input("Please pick a complex password - ")
    
    while any(character.isdigit() for character in newPassword) == False or any(character.isupper() for character in newPassword) == False:
        print ("That password is too weak! Please try again below... ")
        newPassword = input("Please pick a complex password - ")

    newUser = (newUsername + "," + newPassword + "\n")

    f = open('Registered Users.csv', 'a')
    f.write(newUser)
    f.close()
    print ("New user profile created!")

    previouslyViewedFilms = open('Viewing History for {}.txt'.format(newUsername), 'w')
    previouslyViewedFilms.close()   

elif menuChoice == "2":
    loginProcedure()
    print ("Here are your most recently viewed films...")
    previouslyViewedFilms = open('Viewing History for {}.txt'.format(existingUsername), 'r')
    last10Films = previouslyViewedFilms.readlines()[-10:]
    last10Films = "".join(last10Films)
    print (last10Films)
    
elif menuChoice == "3":
    loginProcedure()
    usersFavouriteGenres = []
    f = open('Viewing History for {}.txt'.format(existingUsername), 'r')
    eachFilm = f.readlines()
    f.close()
    eachFilm = [filmHistory.strip('\n') for filmHistory in eachFilm]
    for i in range(len(eachFilm)):
        with open('Films.csv') as csvfile:
            filmReader = csv.DictReader(csvfile)
            for row in filmReader:    
                if eachFilm[i] == row['Film']:
                    usersFavouriteGenres.append(row['Genre1'])
                    usersFavouriteGenres.append(row['Genre2'])
                    usersFavouriteGenres.append(row['Genre3'])

    print ("Here are the genres you appear to enjoy - ")
    uniqueGenresList = []
    [uniqueGenresList.append(i) for i in usersFavouriteGenres if i not in uniqueGenresList]
    print (uniqueGenresList)
    print ("Here are some films you may like - ")
    with open('Films.csv') as csvfile:
        filmReader = csv.DictReader(csvfile)
        for row in filmReader:
            if row['Genre1'] in uniqueGenresList and row['Genre2'] in uniqueGenresList and row['Genre3'] in uniqueGenresList:
                print ("You may also like - ", row['Film'])    

elif menuChoice == "4A" or menuChoice == "4a":
    loginProcedure()
    typedYear = input("What year would you like to search from - ")
    with open('Films.csv') as csvfile:
        filmReader = csv.DictReader(csvfile)
        for row in filmReader:
            if typedYear == row['Year']:
                print ("We have found - ", row['Code'], row['Film'])
        addFilmsToViewingHistory()
                
elif menuChoice == "4B" or menuChoice == "4b":
    loginProcedure()
    typedFilm = input("Type in a film you wish you find... ").upper()
    with open('Films.csv') as csvfile:
        filmReader = csv.DictReader(csvfile)
        for row in filmReader:
            percentageMatch = difflib.SequenceMatcher(None, typedFilm, row['Film'])
            result = round(percentageMatch.ratio()*100, 2)        
            if result > 50:
                print ("We have found - ", row['Code'], row['Film'])
        addFilmsToViewingHistory()
                     
elif menuChoice == "4C" or menuChoice == "4c":
    loginProcedure()
    with open('Films.csv') as csvfile:
        filmReader = csv.DictReader(csvfile)
        for row in filmReader:
            print ("We have found - ", row['Code'], row['Film'])
        addFilmsToViewingHistory()
            
elif menuChoice == "4D" or menuChoice == "4d":
    loginProcedure()
    typedGenre = input("What genre would you like to search from - ").upper()
    with open('Films.csv') as csvfile:
        filmReader = csv.DictReader(csvfile)
        for row in filmReader:
            if typedGenre == row['Genre1'] or typedGenre == row['Genre2'] or typedGenre == row['Genre3']:
                print ("We have found - ", row['Code'], row['Film'])
        addFilmsToViewingHistory()    
else:
    print ("That was not a valid option.")
    exit()
