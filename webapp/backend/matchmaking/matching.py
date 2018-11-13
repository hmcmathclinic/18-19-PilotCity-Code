import numpy as np
import math
import utilities

def get_industry(employer_id):
    return ["Drones", "Robotics"]

def get_product(employer_id):
    return ["Microsoft Hololens", "Robots"]

def get_service(employer_id):
    return ["Metal Fabrication", "Manufacturing"]

def get_flock(employer_id):
    return ["Create", "internet", "application", "transit"]

def get_courses(teacher_id):
    return ["Computer Science", "Spanish", "Physics"]

def get_industry_preferences(teacher_id):
    return ["Gaming", "Data Science"]

def get_tools_tech_skills(teacher_id):
    return ["3D Printing", "Autonomous Technology"]

def get_product_and_service(employer_id):
    products_and_services = get_product(employer_id) + get_service(employer_id)
    return set(products_and_services)

def get_courses_industry_and_tools(teacher_id):
    courses_industry_and_tools = get_courses(teacher_id) + get_industry_preferences(teacher_id) + get_tools_tech_skills(teacher_id)
    return set(courses_industry_and_tools)

def get_score(s1, s2):
    s = 0
    for w1 in s1:
        for w2 in s2:
            # send w1 and w2 to GloVe model
            # square result 
            s += score(w1, w2)**2
    return math.sqrt(s)

def score_teacher(employer_id, teacher_id):
    cit = get_courses_industry_and_tools(teacher_id)
    tools = set(get_tools_tech_skills(teacher_id))

    industry = set(get_industry(employer_id))
    flock = set(get_flock(employer_id))
    product  = set(get_product(employer_id)) 
    service = set(get_service(employer_id)) 

    industry_score = get_score(cit, industry)
    flock_score = get_score(cit, flock)
    product_score = get_score(product, tools)
    servce_score = get_score(service, tools)

    return math.avg(industry_score, flock_score, product_score, servce_score)

