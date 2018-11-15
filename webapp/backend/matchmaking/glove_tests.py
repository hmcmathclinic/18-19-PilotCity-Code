import random


Employer1 = {'Industry': ['Drones', 'Mixed Reality', 'Agriculture'], 'Product': 'Self Driving Car', 'Service': '', 'Flock': 'engage students to create a novel algorithm to navigate a random maze and analyze uncurated data'}

Teacher1 = {'Courses': '', 'Industry': '', 'Tools': ''}

def create_teacher(courses, industry, tools):
    teacher_d = {'Courses': courses, 'Industry': industry, 'Tools': tools}
    return teacher_d

def create_employer(industry, product, service, flock):
    employer_d = {'Industry': industry, 'Product': product, 'Service': service, 'Flock': flock}
    return employer_d

all_courses = {
    'cs': ['Introduction to Computer Science', 'Introduction to computing using Python', 'Principles of Computer Science', 'AP Computer Science'],
    'eng': ['Introduction to Engineering', 'Engineering and design', 'Basics of Engineering'],
    'lang': ['AP English Literature', 'English and Language', 'Spanish 1&2', 'Fiction writing'],
    'math': ['Pre-Calculus', 'Geometry', 'Trigonometry', 'Calculus', 'AP Calculus AB'],
    'hist': ['World history', 'U.S. history', 'U.S. Government'] 
} 

all_industries = ['Drones', 'Robotics', 'Gaming', 'Lifestyle', 'Data Science', 'Sustainability', 'Space', 'Artificial intelligence', 'Automotive', 'Bioprinting', 'Data', 'Drones', 'Gaming', 'Healthcare', 'Internet of Things', 'Lifestyle', 'Manufacturing', 'Mapping', 'Mixed Reality', 'Networking', 'Sensors', 'Shipping', 'Transport', 'Virtual Reality', 'County Covernance', 'Laboratory', 'Municipality', 'Public Safety']

all_skills = ['3D Printing', 'Electronics', 'Virtual Reality', 'Robotics', 'Mixed Reality', 'Space', 'Autonomous Technology', 'Drones', 'Cloud networking', 'Metal Fabrication', 'Game Design', 'Vinyl Cutting', 'Energy Efficiency', 'Data Software', 'Sensors', 'Internet of Things', 'Economic Development']

all_products = ['Mixed Reality Head Mounted Display', 'Microsoft Hololens']

all_services = ['Metal Fabrication', 'Contract Manufacturing', 'Electron Beam Welding']

def create_teacher_set(n, seed):
    '''
    returns a list of n teachers 
    '''
    random.seed(seed)
    teacher_list = []
    for i in range(n):
        subject = random.choice(list(all_courses.keys()))

        num_courses = 1 # random.randint(1,3)
        # seed += 1
        courses = random.sample(all_courses[subject], num_courses)

        num_indus = random.randint(1,5)
        # seed += 1
        industries = random.sample(all_industries, num_indus)

        num_skills = random.randint(1,6)
        # seed += 1
        skills = random.sample(all_skills, num_skills)
        
        teacher_list.append(create_teacher(courses, industries, skills))
    return teacher_list



#tests
#print(create_teacher_set(4,3))
