class Library:
    def check_eligibility(self):
        gender = input("Your gender (male/female): ").lower()
        age = int(input("Your age: "))
        if gender == "male":
            if age > 18:
                print("You are eligible")
            else:
                print("You are not eligible")
        elif gender == "female":
            if age > 15:
                print("You are eligible")
            else:
                print("You are not eligible")
        else:
            print("Invalid input")

    def check_odd_even(self):
        num = int(input("Enter a number: "))
        if num % 2 == 0:
            print(f"{num} is an Even number")
        else:
            print(f"{num} is an Odd number")

    def calculate_triangle(self):
        height = int(input("Height: "))
        breadth = int(input("Breadth: "))
        print("Area formula: (height * breadth) / 2")
        area = (height * breadth) / 2
        print(f"Area of triangle: {area}")

        height1 = int(input("Side 1: "))
        height2 = int(input("Side 2: "))
        base = int(input("Base: "))
        perimeter = height1 + height2 + base
        print("Perimeter formula: side1 + side2 + base")
        print(f"Perimeter of triangle: {perimeter}")

    def subfield(self):
        print("Subfields in AI are:")
        subfields = ["Machine Learning", "Neural Networks", "Computer Vision", "Robotics", "Speech Processing", "Natural Language Processing"]
        for field in subfields:
            print(field)

    def student(self):
        sub1 = int(input("Enter marks for subject 1: "))
        sub2 = int(input("Enter marks for subject 2: "))
        sub3 = int(input("Enter marks for subject 3: "))
        sub4 = int(input("Enter marks for subject 4: "))
        sub5 = int(input("Enter marks for subject 5: "))
        total=sub1+sub2+sub3+sub4+sub5
        print("total",total)
        percentage=(total/500)*100
        print("percentage:",percentage)
        
