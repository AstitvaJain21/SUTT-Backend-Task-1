import json
#using heap as it is more easy than a list and has better in-built functions
import heapq

waiting_list = []
counter = 0
#student ride request
class RideRequest:
    def __init__(self,name,destination,time,year,order):
        self.name = name
        self.destination = destination
        self.time = time
        self.year = year
        self.order = order

#Taking input from User
def add_request():
    print("Add ride request")
    name = input("Enter Name:").title()
    destination = input("Destination(Delhi/Jaipur):").title()
    time = input("Time(Morning/Afternoon/Evening/Night):").title()
    try:
        year = int(input("Enter Year(1-5):"))
    except ValueError:
        print("Invalid Year.Please enter a number")
        return

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

    #Adding a order to each request in case of same year
    global counter
    counter = counter + 1
    student = RideRequest(name,destination,time,year,counter)

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
    queues = build_priority_queue(waiting_list)
    print("Preveiw Matches")
    for cab in cabs:
        if cab.has_left:
            continue

        print(f"\nDriver:{cab.driver}")
        print(f"Trip Details:{cab.destination} & {cab.time}")
        
        available_seats = cab.seats - len(cab.passengers)
        
        #making priority list for cab;s trip details
        trip = (cab.destination,cab.time)
        priority_queue = queues.get(trip,[])
        
        if available_seats <= 0:
            print("Cab is Already full")
            continue

        #selecting student as per priority
        selected = heapq.nsmallest(available_seats,priority_queue)

        if len(selected) == 0:
            print("No eligible students")
        else:
            print("Selected students:",len(selected))

            for entry in selected:
                student = entry[2]
                print(student.name)

def build_priority_queue(waiting_list):
    #making a dictionary queue which will store a priority list for each trip
    queues = {}
    for student in waiting_list:
        #making a tuple trip which stores student's trip details
        trip = (student.destination,student.time)

        #create a key for each trip with value as priority list
        if trip not in queues:
            queues[trip] = []

        #adding each student acc to trip details
        heapq.heappush(queues[trip],(-student.year,student.order,student))
        #using -student.year as heap sorts in ascending order
    
    return queues

def dispatch_cabs(cabs,waiting_list):
    #we want the user to chose which cab will leave and when
    print("Available cabs:")

    #using enumarate helps in getting both index and the value
    for i,cab in enumerate(cabs):
        if not cab.has_left:
            print(f"{i+1}. {cab.driver} | Trip:{cab.destination} , {cab.time} | Seats: {cab.seats}")

    #taking input of which cab has to leave
    try:
        choice = int(input("Enter the cab number to dispatch:"))
    except ValueError:
        print("Please enter a valid number")
        return

    #verification of cab number
    if choice < 1 or choice > len(cabs):
        print("Invalid cab number")
        return

    cab = cabs[choice - 1]

    if cab.has_left:
        print("Cab has already departed")
        return

    queues = build_priority_queue(waiting_list)
    trip = (cab.destination,cab.time)
    priority_queue = queues.get(trip,[])

    available = cab.seats - len(cab.passengers)
    selected = heapq.nsmallest(available,priority_queue)

    if available <= 0:
        print("Cab is full")
        return
    
    if len(selected) == 0:
        print("No students availablefor this trip")
        return

    for entry in selected:
        student = entry[2]

        cab.passengers.append(student)
        waiting_list.remove(student)

    cab.has_left = True
    print("Cab dispatched succesfully")

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
    print("4. Dispatch Cab")
    print("5. Quit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_request()

    elif choice == "2":
        view_requests()

    elif choice == "3":
            preview_matches(cabs,waiting_list)

    elif choice == "4":
        dispatch_cabs(cabs,waiting_list)

    elif choice == "5":
            print("Thanks")
            break

    else:
        print("Invalid choice. Please try again.")

