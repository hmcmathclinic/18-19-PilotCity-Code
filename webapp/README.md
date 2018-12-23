# Website
PilotCity's onboarding and matching platform is hosted at [pilotcity.com](https://pilotcity.com/).

# Matchmaking
The matchmaking algorithm that we use to match employers to classroom aligns employers' and teachers' priorities and skillsets by scoring and comparing the semantic similarity of their onboarding responses. We score semantic similariy by leveraging the GloVe model.

## GloVe Model
We use the GloVe model to obtain a vector representations of each word. We obtain a score of similarity between two words using cosine similarity. The paper introducing the GloVe model can be found [here](https://nlp.stanford.edu/pubs/glove.pdf). The code that calls the GloVe model and computes the cosine similarity between woks is located in [utilities](backend/utilities.py#L79-L84). 

## Scoring a single classroom for a single employer

## Ranking the optimal classrooms for a single employer
Given an employer's uid (unique identifier), our algorithm outputs a list of classroom uids ranked by the scores described above. 

The main file in which this direction of matching takes place can be found in [getRankedClassrooms](backend/getRankedClassrooms.py).

1. Obtain the list of all classroom_ids from firebase by calling the `fetch_all_classrooms` function located in [user_dao_impl](backend/user_dao_impl.py).
2. Compute the score between the employer and each classroom using the `get_score` function in [matching](backend/matching.py)
3. Rank the classrooms from highest to lowest score and return the resulting ranked list.

## Scoring a single employer for a single classroom

## Ranking the optimal employers for a single classroom
Given an classroom's uid (unique identifier), our algorithm outputs a list of employer uids ranked by the scores described above. Note that a classroom's uid is the corresponding teacher's uid appended with the index of the classroom. 

The main file in which this direction of matching takes place can be found in [getRankedEmployers](backend/getRankedEmployers.py).

1. Obtain the list of all employer_ids from firebase by calling the `fetch_all_employers` function located in [user_dao_impl](backend/user_dao_impl.py).
2. Compute the score between the classroom and each employer using the `get_score` function in [matching](backend/matching.py)
3. Rank the employers from highest to lowest score and return the resulting ranked list.

# Changing the database structure
We have built two parsers to change the structure of data in the database. These parser that we used to structure the data in a dictionary structure is located in [parser](backend/parser.py) and the parser that we add coordinates for addresses is located in [coordinate_parser](backend/coordinate_parser.py). 

The steps of creating a parser are:
1. Get the data in the current format by calling the `get_all_users` function in [push](backend/push.py).
2. Make any desired changes to the data structure. 
3. Put data in the appropriate location. For example, if you are changing the format of teacher data, you can call the `put_data_in teachers` function in [push](backend/push.py#L79-L84). Note that this function will overwrite any existing data in the teachers collection. 
