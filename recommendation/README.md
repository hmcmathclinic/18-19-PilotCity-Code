# Website
PilotCity's onboarding and matching platform is hosted at [pilotcity.com](https://pilotcity.com/).

# Matchmaking
The matchmaking algorithm that we use to match employers to classroom aligns employers' and teachers' priorities and skillsets by scoring and comparing the semantic similarity of their onboarding responses. We score semantic similarity by leveraging the GloVe model.

## GloVe Model
We use the GloVe model to obtain a vector representations of each word. We obtain a score of similarity between two words using cosine similarity. The paper introducing the GloVe model can be found [here](https://nlp.stanford.edu/pubs/glove.pdf). The code that calls the GloVe model and computes the cosine similarity between words is located in [utilities](backend/utilities.py#L79-L84). 

## Scoring a single classroom for a single employer
We score a single classroom from the persective of a single employer use the `score_classroom` function in [matching](backend/matching.py#L68-L109). 

The steps of scoring a single classroom from the perspective of a single employer are:
1. Collect the words associated with an employer's industry, service, product, and their vision for their participation with PilotCity into the sets `industry`, `service`, `product`, and `flock` respectively. 
2. Collect the words associated with a classroom's city, the courses that the classroom's teacher offers, the course name, the industry preferences of the teacher, and the tools, technologies, and skills taught in the classroom into the sets `city_teacher`, `all_courses`, `course`, `industry_preferences`, and `tools`. 
3. Compute the score between different sets using the `get_score` function in [matching](backend/matching.py#L48-L66).  This function returns the square root of the sum of the squared score between every pairwise word. That is, if A = {a1, a2, a3} and B = {b1, b2}, `get_score(A, B)` returns sqrt(score(a1, b1)^2 + score(a1, b2)^2 + score(a2, b1)^2 + score(a2, b2)^2 + score(a3, b1)^2 + score(a3, b2)^2). We decided to align the different higher level categories in the following way:
    - `industry_score` is a weighted sum of the scores between `industry` and `tools`, `industry_preferences`, `all_courses`, and `course`
    - `flock_score` is a weighted sum of the scores between `flock` and `tools`, `industry_preferences`, and all courses
    - `product_score` is the score between `product` and `tools`
    - `service_score` is the score between `service` and `tools`
    - `city_score` is 1 if the classroom and employer are in the same city and 0 otherwise. 
4. Compute the final score between the employer and classroom, a weighted combination of `industry_score`, `flock_score`, `product_score`, `service_score`, and `city_score `. Note that these weights can be changed at any time as long as the sum of the weights is 1. 

## Ranking the optimal classrooms for a single employer
Given an employer's uid (unique identifier), our algorithm outputs a list of classroom uids ranked by the scores described above. 

The main file in which this direction of matching takes place can be found in [getRankedClassrooms](backend/getRankedClassrooms.py).

1. Obtain the list of all classroom_ids from firebase by calling the `fetch_all_classrooms` function located in [user_dao_impl](backend/user_dao_impl.py).
2. Compute the score between the employer and each classroom using the `score_classroom` function in [matching](backend/matching.py).
3. Rank the classrooms from highest to lowest score and return the resulting ranked list.

## Scoring a single employer for a single classroom
We score a single employer from the persective of a single classroom use the `score_employer` function in [matching](backend/matching.py#L113-L154). 

The steps of scoring a single employer from the perspective of a single classroom are:
1. Collect the words associated with a classroom's city, the course name, the industry preferences of the teacher, and the tools, technologies, and skills taught in the classroom into the sets `city_teacher`, `course`, `industry_preferences`, and `tools`. 
2. Collect the words associated with an employer's industry, service, product, and their vision for their participation with PilotCity into the sets `industry`, `service`, `product`, and `flock` respectively. 
3. Compute the score between different sets using the `get_score` function in [matching](backend/matching.py#L48-L66).  This function returns the square root of the sum of the squared score between every pairwise word. That is, if A = {a1, a2, a3} and B = {b1, b2}, `get_score(A, B)` returns sqrt(score(a1, b1)^2 + score(a1, b2)^2 + score(a2, b1)^2 + score(a2, b2)^2 + score(a3, b1)^2 + score(a3, b2)^2). We decided to align the different higher level categories in the following way:
    - `course_score` is a weighted sum of the scores between `course` and `industry` and `flock`
    - `industry_preferences_score` is a weighted sum of the scores between `industry_preferences` and `industry`, `flock`, `product`, and `service`
    - `tools_score` is a weighted combination of the scores between `tools` and `industry`, `flock`, `product`, and `service`.
    - `city_score` is 1 if the classroom and employer are in the same city and 0 otherwise. 
4. Compute the final score between the classroom and employer, a weighted combination of `course_score`, `industry_preferences_score`, `tools_score`, and `city_score `. Note that these weights can be changed at any time as long as the sum of the weights is 1. 


## Ranking the optimal employers for a single classroom
Given an classroom's uid (unique identifier), our algorithm outputs a list of employer uids ranked by the scores described above. Note that a classroom's uid is the corresponding teacher's uid appended with the index of the classroom. 

The main file in which this direction of matching takes place can be found in [getRankedEmployers](backend/getRankedEmployers.py).

1. Obtain the list of all employer_ids from firebase by calling the `fetch_all_employers` function located in [user_dao_impl](backend/user_dao_impl.py).
2. Compute the score between the classroom and each employer using the `get_score` function in [matching](backend/matching.py).
3. Rank the employers from highest to lowest score and return the resulting ranked list.

# Changing the database structure
We have built two parsers to change the structure of data in the database. These parser that we used to structure the data in a dictionary structure is located in [parser](backend/parser.py) and the parser that we add coordinates for addresses is located in [coordinate_parser](backend/coordinate_parser.py). 

The steps of creating a parser are:
1. Get the data in the current format by calling the `get_all_users` function in [push](backend/push.py).
2. Make any desired changes to the data structure. 
3. Put data in the appropriate location. For example, if you are changing the format of teacher data, you can call the `put_data_in teachers` function in [push](backend/push.py#L79-L84). Note that this function will overwrite any existing data in the teachers collection. 

# Running code:
Don't forget to run `pip install -r requirements.txt` to install the relevant dependencies

# Steps to deploy code to Kubernetes.
0. Get service key for PilotCity Firestore DB, copy into `webapp/backend` directory and rename as `service_account.json`
1. Install docker
2. Install gcloud SDK (https://cloud.google.com/sdk/install)
3. Run `gcloud init`, sign in as pilotcity and choose the project "backend-dot-pilotcity"
4. Run `gcloud container clusters get-credentials matchmaking-cluster --zone us-west1-a`
5. Run `gcloud auth configure-docker`
6. Run `chmod u+x ./build.sh`(Run this once on any shell script to make the script executable )
7. Run `./build.sh` to build and push docker images to GCR
8. Run `./down.sh` to shut down any running instance of the backend service.
9. Run `./up.sh` to restart the backend service.
