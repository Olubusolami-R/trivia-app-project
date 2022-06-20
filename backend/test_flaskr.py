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
        self.new_question = {"question": "How are youuu?", "answer": "Fine", "difficulty": 1,"category":5}
        self.new_category={"id":'4',"type":"sports"}
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
    
    # def test_delete_question(self):
    #     res=self.client().delete('/questions/7') #this assumes that there is a question with id 2
    #     data=json.loads(res.data)
    #     self.assertEqual(res.status_code,200)
    #     self.assertEqual(data['success'],True)

    def test_delete_invalid_question(self):
        res=self.client().delete('/questions/10000')
        data=json.loads(res.data)
        self.assertEqual(res.status_code,422)
        self.assertEqual(data['success'],False)

    # def test_create_question(self):
    #     res=self.client().post('/questions',json=self.new_question)
    #     data=json.loads(res.data)
    #     self.assertEqual(res.status_code,200)
    #     self.assertEqual(data['success'],True)
    
    def test_search_questions(self):
        res=self.client().post('/questions/search_results',json={'searchTerm':'title'})
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'])
    
    def test_get_category_questions(self):
        res=self.client().get("/categories/5/questions") #the use of number 5 assumes there is a category with id 5 in the test database
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['currentCategory'])
    
    def test_get_404_invalid_category_questions(self):
        res=self.client().get("/categories/1000/questions") 
        data=json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
    
    def test_get_quiz(self):
        res=self.client().post('/quizzes',json={'quiz_category':self.new_category,'previous_questions':[]}) 
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['question'])

if __name__ == "__main__":
    unittest.main()