import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        self.new_question = {"question": "How are you?", "answer": "Fine", "difficulty": 1,"category":5}
        self.invalid_question={"question": "", "answer": "", "difficulty": 1,"category":5}
        
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res=self.client().get('/categories')
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['categories'])

    def test_404_if_get_specific_category(self):
        res=self.client().get('/categories/5')
        data=json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)

    def test_get_paginated_questions(self):
        res=self.client().get('/questions')
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))

    def test_get_404_beyond_valid_pages(self):
        res=self.client().get('/questions?page=5000')
        data=json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
    
    def test_delete_question(self):
        res=self.client().delete('/questions/16')       #change the question id after each execution
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)

    def test_422_if_question_does_not_exist(self):
        res=self.client().delete('/questions/10000')
        data=json.loads(res.data)
        self.assertEqual(res.status_code,422)
        self.assertEqual(data['success'],False)

    def test_create_question(self):
        res=self.client().post('/questions',json=self.new_question)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
    
    def test_400_if_new_question_is_invalid(self):
        res=self.client().post('/questions',json=self.invalid_question)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['success'],False)

    def test_search_questions(self):
        res=self.client().post('/questions/search_results',json={'searchTerm':'title'})
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'])
    
    def test_404_if_wrong_search_route(self):
        res=self.client().post('/questions/search_results/5',json={'searchTerm':'title'})
        data=json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)

    def test_get_category_questions(self):
        res=self.client().get("/categories/5/questions") 
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['currentCategory'])
    
    def test_404_questions_category_does_not_exist(self):
        res=self.client().get("/categories/1000/questions") 
        data=json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
    
    def test_get_quiz(self):
        res=self.client().post('/quizzes',json={'previous_questions': [], 'quiz_category': {"type": "Science", "id": "1"}}) 
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['question'])
    
    def test_400_if_bad_request_for_quiz(self):
        res=self.client().post('/quizzes',json={}) 
        data=json.loads(res.data)
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],"bad request")
if __name__ == "__main__":
    unittest.main()