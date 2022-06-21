# Trivia App Documentation


## About the Trivia App
This app is a project from the Udacity Alx-t fullstack nanodegree. Users of the app will be able to view questions and answers from all categories or one category bon the list page. Users can also search for questions.
On the "Add" page which is the second page,the app allows users to add new questions to categories. Lastly, users also get to play a trivia game with questions from all categories or one category on the "Play" page.


## Getting Started
### Pre-requisites and Local Development
Developers running this project should already have python3, pip, postgresql and node installed on their local machines. All code in the backend follow the [PEP 8 style guide](https://www.python.org/dev/peps/pep-0008/). It is also recommended to run the project in a virtual environment. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


### Setting up the database
Ensure postgresql is running on your computer then run the following command to create the trivia database:
```bash
createbd trivia
```
You can now populate the database by running the following from the backend folder:
```bash
psql trivia < trivia.psql
```

You should have the database set up properly on your system. You can verify using the following commands in your terminal:
```bash
psql trivia
\dt 
```

### Backend
After setting up the virtual environment, navigate to the backend folder. In the backend folder, there is a requirements.txt file which should be installed by running the command ```bash
pip install requirements.txt
``` 
or 
```bash 
pip3 install requirements.txt
``` 
in your terminal or command line. After this, all required dependencies should have been installed.

In order to run the project, ensure you have navigated to the backend folder and run the following commands:
```bash 
export FLASKAPP=flaskr
export FLASKENV=development
flask run 
```

The commands put the app in development and also ensure the __init.py__ file in the flaskr folder is used. The project should be running on http://127.0.0.1:5000 on your computer . If you are running windows locally, you can look for the equivalent of the commands for windows in the [Flask documentation](https://flask.palletsprojects.com/en/2.1.x/quickstart/#a-minimal-application)


### Frontend
Ensure you have navigated to the frontend folder, then run the following commands:
```bash 
npm install //run this only once to install the dependencies
npm start  //to run the project
```
After running npm start, the project should be running on http://localhost:3000/ where you will see the trivia interface.


### Tests
To be able to run tests, ensure you're in the backend folder and run the following commands (leave out the first command when running the commands for the first time):
```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
You should update the tests as you make changes to the app backend code.


## API Reference
### Getting Started
1. BaseURL: Currently, this app has no base URL and is running locally. It is being hosted at the default: http://127.0.0.1:5000
2. Authentication: Currently, this app does not use authentication or API keys.


## Error Handling
The API will return 3 major errors when requests do not succeed:
1. 400: Bad request
2. 422: Unprocessable entity
3. 404: Resource not found

Errors are returned as json in the following format:
```json
{
    "success":False,
    "error":400,
    "message":"bad request"
}
```

### API Endpoints

`GET '/categories'`

- Request Arguments: None
- Returns: A success value and an object with a single key, categories, that contains an object of id (key): category_string (value) pairs.
Sample: curl "http://127.0.0.1:5000/categories" \

Sample output:
```bash 
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports", 
    "7": "Fun"
  }, 
  "success": true
}
```


`GET '/questions'`

- Request arguemnts: None
- Returns: A success value, a list of question objects, the total number questions, current category and an object with a single key, categories, that contains an object of id (key): category_string (value) pairs. The results of the request are all paginated in groups of 10.

Sample: curl "http://127.0.0.1:5000/questions?page=1" 

Sample output:
```bash 
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports", 
    "7": "Fun"
  }, 
  "currentCategory": null, 
  "questions": [
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "success": true, 
  "total_questions": 22
}
```


`DELETE '/questions/{question_id}`

This endpoint is use to delete questions from the database. 
- Request Arguments: The id of the question to be deleted(question_id).
- Returns: A success value after deletion from database.
Sample: curl -X DELETE "http://127.0.0.1:5000/questions/16" 

Sample output:
```bash 
{
  "success": true
}
```


`POST '/questions'`

This endpoint is used to create or add questions to the database.
- Request Arguments: None.
- Returns: A success value after successful addition to database.
Sample: curl -X POST -H "Content-Type:application/json" -d '{"question": "How are you?", "answer": "Fine", "difficulty": 1,"category":5}' "http://127.0.0.1:5000/questions" 

Sample output:
```bash 
{
  "success": true
}
```



`POST '/questions/search_results'`

This endpoint is used to sends a post request  to search for a question by a search term.
- Request Arguments: None.
- Returns: A success value and a list of formatted question objects.
Sample: curl -X POST -H "Content-Type:application/json" -d '{"searchTerm":"title"}' "http://127.0.0.1:5000/questions/search_results" 

Sample output:
```bash 
{
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ], 
  "success": true
}
```


`GET '/categories/{category_id}/questions'` 

This endpoint gets the questions associated with the specified category.
- Request Arguments: None
- Returns: A success value, a list of question objects, the total number questions and the current category. The results of the request are all paginated in groups of 10.
Sample: curl "http://127.0.0.1:5000/categories/5/questions" 

Sample output:
```bash 
{
  "currentCategory": "Entertainment", 
  "questions": [
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "busbus", 
      "category": 5, 
      "difficulty": 1, 
      "id": 26, 
      "question": "What's my name?"
    }, 
    {
      "answer": "ashi", 
      "category": 5, 
      "difficulty": 1, 
      "id": 32, 
      "question": "first house?"
    }, 
    {
      "answer": "Fine", 
      "category": 5, 
      "difficulty": 1, 
      "id": 33, 
      "question": "How are you?"
    }
  ], 
  "success": true, 
  "total_questions": 5
}
```


`GET '/quizzes'`
This endpoint sends a post request in order to get the next question for the trivia quiz.
- Request Arguments: None
- Returns: A success value and a single question object.
Sample: curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type:application/json" -d '{"quiz_category":{"id": "1","type": "Science"},"previous_questions":[]}' 

Sample output:
```bash 
{
  "question": {
    "answer": "The Liver", 
    "category": "1", 
    "difficulty": 4, 
    "id": 20, 
    "question": "What is the heaviest organ in the human body?"
  }, 
  "success": true
}
```


## Deployment N/A

## Acknowledgements

To the alx-t team and every alx-t learner staying up till 3 am. We'll make it through.
