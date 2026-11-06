import json

#student ride request
class RideRequest:
    def __init__(self,name,destination,time,year):
        self.name = name
        self.destination = destination
        self.time = time
        self.year = year

waiting_list = []

#Taking input from User
def add_request():
    print("Add ride request")
    name = input("Enter Name:")
    destination = input("Destination(Delhi/Jaipur):").title()
    time = input("Time(Morning/Afternoon/Evening/Night):").title()
    try:
        year = int(input("Enter Year(1-5):"))
    except ValueError:
        print("Invalid Year.Please enter a number")

    #Verification
    if destination not in ["Jaipur","Delhi"]:
        print("Invalid Destination")
        return

    if time not in ["Morning","Afternoon","Evening","Night"]:
        print("Invalid Time")
        return

    if year < 1 or year > 5:
        print("Year must be between 1 to 5")
        return

    student = RideRequest(name,destination,time,year)

    waiting_list.append(student)

    print("Request Accepted")

def view_requests():
    
    if len(waiting_list) == 0:
        print("No students waiting.")
        return

    for student in waiting_list:
        print(f"{student.name} | {student.destination} | {student.time} | Year {student.year}")

#Cab info
class Cab:
    def __init__(self,driver,seats,destination,time):
        self.driver = driver
        self.seats = seats
        self.destination = destination
        self.time = time
        self.has_left = False
        self.passengers = []

#importing cab data from json file
def load_cabs():
    cabs = []

    try:
        with open("cab.json", "r") as file:
            data = json.load(file)
            for item in data:
                #creating a cab object from json data
                cab = Cab(item["driver"],item["seats"],item["destination"],item["time"])
                cabs.append(cab)
    except FileNotFoundError:
        print("Cab data file is missing")

    return cabs

#matching students with cab
def preview_matches(cabs,waiting_list):
    print("Preveiw Matches")
    for cab in cabs:
        if cab.has_left:
            continue

        print(f"\nDriver:{cab.driver}")
        print(f"Trip Details:{cab.destination} & {cab.time}")
        eligible_students = []
        available_seats = cab.seats - len(cab.passengers)

        if available_seats <= 0:
            print("Cab is Already full")
            continue
        
        for student in waiting_list:
            if cab.destination == student.destination and cab.time == student.time:
                eligible_students.append(student)

        selected_students = eligible_students[0:available_seats]
        if len(selected_students) == 0:
            print("No eligible students")
        else:
            print("Selected students:",len(selected_students))
            for student in selected_students:
                print(student.name)


cabs = load_cabs()
print("Available cabs:")
for cab in cabs:
    print(f"{cab.driver} | {cab.destination} | {cab.time} | Seats:{cab.seats}")


# Main menu
while True:
    print("Cab pool matcher")
    print("1. Add ride request")
    print("2. View waiting students")
    print("3. Preview cab matches")
    print("4. Quit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_request()

    elif choice == "2":
        view_requests()

    elif choice == "3":
            preview_matches(cabs,waiting_list)

    elif choice == "4":
        print("Thanks")
        break

    else:
        print("Invalid choice. Please try again.")

