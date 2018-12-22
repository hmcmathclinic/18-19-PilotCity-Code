# Website
PilotCity's onboarding and matching platform is hosted at [pilotcity.com](https://pilotcity.com/).

# Matchmaking
The matchmaking algorithm that we use to match employers to classroom aligns employers' and teachers' priorities and skillsets by scoring and comparing the semantic similarity of their onboarding responses. We score semantic similariy by leveraging the GloVe model, which scores words for semantic similarity.

## GloVe Model

## Scoring a single classroom for a single employer

## Ranking the optimal classrooms for a single employer
Given an employer's uid (unique identifier), our algorithm outputs a list of classroom uid's ranked by the scores described above. 

The main file in which this direction of matching takes place can be found in [getRankedClassrooms](backend/getRankedClassrooms.py).

1. Obtain the list of all classroom_ids from firebase by calling the `fetch_all_classrooms` function located in [push](backend/fetch_all_classrooms).
2. Compute the score for each classroom (TODO: insert section link).
3. Rank the classrooms from highest to lowest score (TODO: confirm). 
4. TODO: describe how to send a request for this.

## Scoring a single employer for a single classroom

## Ranking the optimal employers for a single classroom
Given a classroom's uid (unique identifier), our algorithm outputs a list of employer uids ranked by the scores described above. Note that the teacher's uid appended with the index at which the teacher entered the clas

The main file in which this direction of matching takes place can be found in [getRankedEmployers](backend/getRankedEmployers.py).

1. Obtain the list of all classroom_ids from firebase by calling the `fetch_all_classrooms` function located in [push](backend/fetch_all_classrooms).
2. Compute the score for each classroom (TODO: insert section link).
3. Rank the classrooms from highest to lowest score (TODO: confirm). 
4. TODO: describe how to send a request for this.


# Making changes to the database structure (parser)

# Tasks:
- [x] task1
- [ ] task2
- [ ] task3
