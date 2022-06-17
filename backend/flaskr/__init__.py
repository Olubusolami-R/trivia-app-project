import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category,db

QUESTIONS_PER_PAGE = 10

def paginate_question(request, questions):
    page = request.args.get("page", 1, type=int)
    beginning = (page - 1) * QUESTIONS_PER_PAGE
    end = beginning + QUESTIONS_PER_PAGE

    f_questions = [question.format() for question in questions]
    current_questions = f_questions[beginning:end]
    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories=Category.query.order_by(Category.id).all()
        categories_dict={}
        for category in categories:
            categories_dict[category.id]=category.type

        if len(categories)==0:
            abort(404)
        return jsonify({'success':True,'categories':categories_dict})

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions',methods=['GET'])
    def get_all_paginated_questions():
        questions=Question.query.order_by(Question.id).all()
        formatted_questions=paginate_question(request,questions)

        if len(formatted_questions)==0:
            abort(404)

        categories=Category.query.order_by(Category.id).all()
        categories_dict={}
        for category in categories:
            categories_dict[category.id]=category.type

        return jsonify({'questions':formatted_questions,'total_questions':len(questions),'categories':categories_dict,'currentCategory':None})
    
    
    
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question=Question.query.get(question_id)
        print(question)
        try:
            question.delete()
            return jsonify({'success':'True'})
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()


    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions',methods=['POST'])
    def create_question():
        data=request.get_json()
        question=Question(question=data['question'],
                            answer=data['answer'],
                            category=data['category'],
                            difficulty=data['difficulty'])
        try:
            question.insert()
            return jsonify({'success':'True'})
        except:
            abort(400)
        finally:
            db.session.close()

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search_results',methods=['POST'])
    def search():
        data=request.get_json()
        searchTerm=data['searchTerm']
        questions=Question.query.filter(Question.question.ilike('%'+searchTerm+'%')).all()
        questions=paginate_question(request,questions)
        return jsonify({'success':True,'questions':questions})
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions',methods=['GET'])
    def get_category_questions(category_id):
        current_category=Category.query.get(category_id)
        questions=Question.query.filter_by(category=category_id).all()
        f_questions=paginate_question(request,questions)
        if len(f_questions)==0:
            abort(404)
        return jsonify({'questions':f_questions,'total_questions':len(questions),'currentCategory':current_category.type})
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes',methods=['POST'])
    def get_quiz():
        data=request.get_json()

        category_id=data['quiz_category']['id']
        previousQuestions=data['previous_questions']

        if category_id==0:
            questions=Question.query.all()
        else:
            questions=Question.query.filter_by(category=category_id).all()

        formatted_questions=[question.format() for question in questions]

        unused_questions=[]

        for question in formatted_questions:
            if question['id'] not in previousQuestions:
                unused_questions.append(question)
    
        if len(unused_questions)==0:
            currentQuestion=None
        else:
            currentQuestion=random.choice(unused_questions)

        return jsonify({'success':True,'question':currentQuestion,})

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success':False,
            'error':404,
            'message':'resource not found'
        }),404
    
    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
            'success':False,
            'error':422,
            'message':'unprocessable'
        }),422

    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
            'success':False,
            'error':400,
            'message':'bad request'
        }),400
    return app

