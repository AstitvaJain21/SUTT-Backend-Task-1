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




#Cab info
class Cab:
    def __init__(self,driver,seats,destination,time):
        self.driver = driver
        self.seats = seats
        self.destination = destination
        self.time = time

        self.passengers = []
        
#assign
student1 = RideRequest("Rahul", "Delhi","Morning",2)
student2 = RideRequest("Aman", "Delhi","Morning",5)
student3 = RideRequest("Karan", "Jaipur","Evening",3)

cab1 = Cab("Raj",4,"Delhi","Morning")
cab2 = Cab("Mohan",3,"Jaipur","Evening")

#prints
print("CAB POOL MATCHER")

print("\nStudent Information:")

print(student1.name, student1.year)
print(student2.name, student2.year)
print(student3.name, student3.year)

print("\nCab Information:")

print(cab1.driver)
print(cab1.destination)
print(cab1.time)
print(cab1.seats)

print(cab2.driver)
print(cab2.destination)
print(cab2.time)
print(cab2.seats)