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
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response
    
    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories=Category.query.order_by(Category.id).all()
        if len(categories)==0:
            abort(404)
        categories_dict={}
        #render in the required key-value format
        for category in categories: 
            categories_dict[category.id]=category.type
        return jsonify({'success':True,'categories':categories_dict})

    @app.route('/questions',methods=['GET'])
    def get_paginated_questions():
        questions=Question.query.order_by(Question.id).all()
        formatted_questions=paginate_question(request,questions)
        if(len(formatted_questions)==0):
            abort(404) #no questions for that page
        categories=Category.query.order_by(Category.id).all()
        categories_dict={}
        for category in categories:
            categories_dict[category.id]=category.type
        return jsonify({'success':True,'questions':formatted_questions,'total_questions':len(questions),'categories':categories_dict,'currentCategory':None})

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question=Question.query.get(question_id)
        try:
            question.delete()
            return jsonify({'success':True})
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    @app.route('/questions',methods=['POST'])
    def create_question():
        data=request.get_json()
        question=Question(question=data['question'],
                            answer=data['answer'],
                            category=data['category'],
                            difficulty=data['difficulty'])
        try:
            question.insert()
            return jsonify({'success':True})
        except:
            abort(422)
        finally:
            db.session.close()

    @app.route('/questions/search_results',methods=['POST'])
    def search():
        data=request.get_json()
        searchTerm=data['searchTerm']
        try:
            questions=Question.query.filter(Question.question.ilike('%'+searchTerm+'%')).all()
            questions=paginate_question(request,questions)
            return jsonify({'success':True,'questions':questions})
        except:
            abort(422)
   
    @app.route('/categories/<category_id>/questions',methods=['GET'])
    def get_category_questions(category_id):
        current_category=Category.query.get(category_id)
        if current_category==None: #the category does not exist
            abort(404)
        questions=Question.query.filter_by(category=category_id).all()
        f_questions=paginate_question(request,questions)
        return jsonify({'success':True,'questions':f_questions,'total_questions':len(questions),'currentCategory':current_category.type})
   
    @app.route('/quizzes',methods=['POST'])
    def get_quiz():
        try:
            data=request.get_json()
            category_id=data['quiz_category']['id']
            previousQuestions=data['previous_questions']
            print(data['quiz_category'],previousQuestions)
            if category_id==0:
                questions=Question.query.all()
            else:
                questions=Question.query.filter_by(category=category_id).all()

            formatted_questions=[question.format() for question in questions]

            unused_questions=[] #to store questions that have not been answered

            for question in formatted_questions: #filtering unused questions
                if question['id'] not in previousQuestions:
                    unused_questions.append(question) 
        
            if len(unused_questions)==0:
                currentQuestion=None 
                #This means all questions have been exhausted (or did not exist at all) and will 
                # propel a forced end to the trivia quiz on the frontend.
            else:
                currentQuestion=random.choice(unused_questions)

            return jsonify({'success':True,'question':currentQuestion,})
        except:
            abort(400)
        

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

