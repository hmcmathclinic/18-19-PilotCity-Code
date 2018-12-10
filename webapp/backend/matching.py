import numpy as np
import math
import utilities
from user_dao_impl import UserDaoImpl

class Matching:

    def __init__(self, employer_id, classroom_id):
        self.dao = UserDaoImpl()
        self.utilities = utilities.Utils()
        self.employer_id = employer_id
        self.classroom_id = classroom_id
        self.employer_data = self.dao.fetch_employer_data(employer_id)
        self.classroom_data = self.dao.fetch_classroom_data(classroom_id)
        self.teacher_id = self.classroom_data["teacher_uid"]
        self.teacher_data = self.dao.fetch_teacher_data(self.teacher_id) 

    def get_industry(self):
        return self.employer_data["selected_industry_keywords"]

    def get_product(self):
        return self.employer_data["selected_product_keywords"]

    def get_service(self):
        return self.employer_data["selected_service_keywords"]

    def get_flock(self):
        return self.employer_data["selected_challenge_keywords"]

    def get_all_courses_taught(self):
        classes = []
        for classroom in self.teacher_data["classes"]:
            classes.append(classroom["coursename"])
        return classes

    def get_course_name(self):
        return self.classroom_data["coursename"]

    def get_industry_preferences(self):
        return self.teacher_data["selected_industry_keywords"]

    def get_tools_tech_skills(self):
        return self.teacher_data["selected_skills_keywords"]

    def get_score(self, s1, s2):
        s = 0
        for phrase1 in s1:
            for phrase2 in s2:
                s_inner = 0
                num_pairs = 0
                for w1 in phrase1.split():
                    for w2 in phrase2.split():
                        ss = self.utilities.score(w1.lower(), w2.lower())
                        if ss != 2:
                            s_inner += ss
                            num_pairs += 1
                if num_pairs != 0:
                    s_inner = s_inner/num_pairs
                else: 
                    s_inner = 0
                s += s_inner**2
                #print(s)
        return math.sqrt(s)

    def score_classroom(self):
        # Teacher data
        all_courses = self.get_all_courses_taught()
        course = set(self.get_course_name())
        industry_preferences = set(self.get_industry_preferences())
        tools = set(self.get_tools_tech_skills())

        # Employer data
        industry = set(self.get_industry())
        product  = set(self.get_product()) 
        service = set(self.get_service()) 
        flock = set(self.get_flock())

        industry_score_tools = self.get_score(tools, industry)
        industry_score_industry = self.get_score(industry_preferences, industry)
        industry_score_all_courses = self.get_score(all_courses, industry)
        industry_score_coursename = self.get_score(course, industry)
        industry_score = 0.4*industry_score_industry + 0.3*industry_score_coursename + 0.2*industry_score_tools + 0.1*industry_score_all_courses;

        flock_score_tools = self.get_score(tools, flock)
        flock_score_industry = self.get_score(industry_preferences, flock)
        flock_score_all_courses = self.get_score(all_courses, flock)
        flock_score = 0.5*flock_score_tools + 0.3*flock_score_industry + 0.2*flock_score_all_courses
        
        product_score = self.get_score(product, tools)
        service_score = self.get_score(service, tools)

        if service_score == 0 and product_score != 0:
            return 0.5*industry_score + 0.1*flock_score + 0.4*product_score
        
        elif service_score != 0 and product_score == 0:
            return 0.5*industry_score + 0.1*flock_score + 0.4*service_score
        
        elif product_score != 0 and service_score != 0:
            return 0.5*industry_score + 0.1*flock_score + 0.2*product_score + 0.2*service_score
        else:
            return 0.7*industry_score + 0.3*flock_score 

    def score_employer(self):
        # Teacher data
        course = set(self.get_course_name())
        industry_preferences = set(self.get_industry_preferences())
        tools = set(self.get_tools_tech_skills())

        # Employer data
        industry = set(self.get_industry())
        product  = set(self.get_product()) 
        service = set(self.get_service()) 
        flock = set(self.get_flock())


        course_score_industry = self.get_score(course, industry)
        course_score_flock = self.get_score(course, flock)
        course_score = 0.8*course_score_industry + 0.2*course_score_flock

        industry_preferences_score_industry = self.get_score(industry_preferences, industry)
        industry_preferences_score_flock = self.get_score(industry_preferences, flock)
        industry_preferences_score = 0.8*industry_preferences_score_industry + 0.2*industry_preferences_score_flock

        tools_score_industry = self.get_score(tools, industry)
        tools_score_flock = self.get_score(tools, flock)
        tools_score_product = self.get_score(tools, product)
        tools_score_service = self.get_score(tools, service)
        
        if tools_score_service == 0 and tools_score_product != 0:
            tools_score = 0.5*tools_score_industry + 0.1*tools_score_flock + 0.4*tools_score_product
        
        elif tools_score_service != 0 and tools_score_product == 0:
            tools_score = 0.5*tools_score_industry + 0.1*tools_score_flock + 0.4*tools_score_service
        
        elif tools_score_product != 0 and tools_score_service != 0:
            tools_score = 0.5*tools_score_industry + 0.1*tools_score_flock + 0.2*tools_score_product + 0.2*tools_score_service
        else:
            tools_score = 0.7*tools_score_industry + 0.3*tools_score_flock


        return (course_score + industry_preferences_score + tools_score)/3.0

def main():
    classroom = sys.argv[1]
    employer = sys.argv[2]
    match = Matching(employer,classroom)
    print("Classroom score is ", match.score_classroom())
    print("Employer score is ", match.score_employer())

if __name__ == '__main__':
    main()