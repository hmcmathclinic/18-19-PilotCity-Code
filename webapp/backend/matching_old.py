import numpy as np
import math
import utilities
from user_dao_impl import UserDaoImpl
import time 

class Matching:


    def __init__(self, employer_id, teacher_id):
        self.dao = UserDaoImpl()
        self.employer_id = employer_id
        self.teacher_id = teacher_id
        self.employer_data = self.dao.fetch_employer_data(employer_id)
        self.teacher_data = self.dao.fetch_teacher_data(teacher_id)


    def get_industry(self):
        return self.employer_data["selected_industry_keywords"]
 
    def get_product(self):
        return self.employer_data["selected_product_keywords"]
 
    def get_service(self):
        return self.employer_data["selected_service_keywords"]
 
    def get_flock(self):
        return self.employer_data["selected_challenge_keywords"]


    def get_courses(self):
        classes = []
        for classroom in self.teacher_data["classes"]:
            classes.append(classroom["coursename"])
        return classes


    def get_industry_preferences(self):
        return self.teacher_data["selected_industry_keywords"]


    def get_tools_tech_skills(self):
        return self.teacher_data["selected_skills_keywords"]
 
    def get_product_and_service(self):
        products_and_services = self.get_product() + self.get_service()
        return set(products_and_services)


    def get_courses_industry_and_tools(self):
        courses_industry_and_tools = self.get_courses() + self.get_industry_preferences() + self.get_tools_tech_skills()
        return set(courses_industry_and_tools)


    def get_industry_and_flock(self):
        industry_and_flock = self.get_industry() + self.get_flock()
        return set(industry_and_flock)
 
    def get_industry_product_service_and_flock(self):
        industry_product_service_and_flock = self.get_industry() + self.get_product() + self.get_service() + self.get_flock()
        return set(industry_product_service_and_flock)
 

    def get_score(self, s1, s2):
        s = 0
        start = time.time()
        for phrase1 in s1:
            for phrase2 in s2:
                s_inner = 0
                num_pairs = 0
                for w1 in phrase1.split():
                    for w2 in phrase2.split():
                        ss = utilities.score(w1.lower(), w2.lower())
                        if ss != 2:
                            s_inner += ss
                            num_pairs += 1
                if num_pairs != 0:
                    s_inner = s_inner/num_pairs
                else: 
                    s_inner = 0
                s += s_inner**2
            #print(s)
        end = time.time()
        print("nested for loops runtime - {}".format(end - start))
        return math.sqrt(s)

    def score_teacher(self):
        # Teacher data
        cit = self.get_courses_industry_and_tools()
        tools = set(self.get_tools_tech_skills())

        # Employer data
        industry = set(self.get_industry())
        product  = set(self.get_product()) 
        service = set(self.get_service()) 
        flock = set(self.get_flock())

        industry_score = self.get_score(cit, industry)
        flock_score = self.get_score(cit, flock)
        product_score = self.get_score(product, tools)
        service_score = self.get_score(service, tools)

        return (industry_score + flock_score + product_score + service_score) / 4.0


    def score_employer(self):
        # Teacher data
        courses = set(self.get_courses())
        industry_preferences = set(self.get_industry_preferences())
        tools = set(self.get_tools_tech_skills())
        # Employer data
        industry_and_flock = self.get_industry_and_flock()
        industry_product_service_and_flock = self.get_industry_product_service_and_flock()
        courses_score = self.get_score(courses, industry_and_flock)
        industry_preferences_score = self.get_score(industry_preferences, industry_and_flock)
        tools_score = self.get_score(tools, industry_product_service_and_flock)
        return (courses_score + industry_preferences_score + tools_score)/3.0

def main():
    teacher = sys.argv[1]
    employer = sys.argv[2]
    match = Matching(teacher, employer)
    print("Teacher score is ", match.score_teacher())
    print("Employer score is ", match.score_employer())

if __name__ == '__main__':
     main()