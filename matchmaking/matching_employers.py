import numpy as np

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)-

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

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
            s += angle_between
