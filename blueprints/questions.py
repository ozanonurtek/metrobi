from sanic.blueprints import Blueprint
from sanic import response
from sanic_openapi import doc
from sanic.views import HTTPMethodView
import ast
import asyncio
import datetime

questions_blueprint = Blueprint('Questions', url_prefix='/questions')


class Q1View(HTTPMethodView):
    @doc.summary('Write a function that finds the duplicate items in any given array')
    @doc.consumes({'payload': [str]}, location='body', content_type='application/json')
    @doc.produces({'payload': [str]}, content_type='application/json')
    @doc.response(200, {'payload': [str]}, description='Success')
    async def post(self, request):
        result = await self.find_duplicates(request.json)
        return response.json({'payload': result})

    @staticmethod
    async def find_duplicates(input_array):
        """
        Iterates over input array and finds duplicates. Dictionary and primitive types are supported
        """
        # To store duplicates
        duplicates = []
        if input_array:
            lookup_dictionary = dict()
            for item in input_array:
                if type(item) is dict:
                    # To support dictionaries
                    item = str(item)

                if item in lookup_dictionary:
                    if not lookup_dictionary[item]['is_appended_once']:
                        try:
                            # Try to append as dictionary else it will throw value error
                            duplicates.append(ast.literal_eval(item))
                        except ValueError as value_error:
                            duplicates.append(item)
                        lookup_dictionary[item]['is_appended_once'] = True
                else:
                    lookup_dictionary[item] = {'looked_up': True, 'is_appended_once': False}

        return duplicates


class Q2View(HTTPMethodView):
    @doc.summary('Write an async python function that writes every item in any given array with 1,2,4,8...seconds')
    @doc.consumes({'payload': [str]}, location='body', content_type='application/json')
    @doc.produces({'payload': 'OK'}, content_type='application/json')
    @doc.response(200, {'payload': [str]}, description='Success')
    async def post(self, request):
        """
        This method is completely runs async, so check your terminal after sending request
        """
        print('=== START TIME: {} ==='.format(datetime.datetime.now()))
        await self.seconds(request.json)
        return response.json({'payload': 'OK'})

    @staticmethod
    async def job(sleep_time, item):
        print('TASK CREATED WITH SLEEP TIME: {} - ITEM: {}'.format(sleep_time, item))
        await asyncio.sleep(sleep_time)
        print('ITEM: {} - TIME: {}'.format(item, datetime.datetime.now()))

    async def seconds(self, input_array):
        for index, item in enumerate(input_array):
            asyncio.create_task(self.job(pow(2, index), item))


class Q4View(HTTPMethodView):
    @doc.summary('String brackets open close problem')
    @doc.consumes({'payload': {'payload': str}}, location='body', content_type='application/json')
    @doc.produces({'payload': {'payload': bool}}, content_type='application/json')
    @doc.response(200, {'payload': {'payload': bool}}, description='Success')
    async def post(self, request):
        if 'payload' in request.json:
            result = await self.check_opened_closed_properly(request.json['payload'])
            return response.json({'payload': result})
        return response.json({'payload': False})

    @staticmethod
    async def check_opened_closed_properly(string_to_check):
        # Directly return false if length is not even number
        """
        Checks if given string full of brackets, open and closed properly.
        Returns true for properly closed string, false for vice versa
        P.S: From the examples in question, returns False for characters other than brackets. Passing non-bracket char in
        loop can solve that.
        """
        length = len(string_to_check)
        if length % 2 != 0 or length == 0:
            return False

        # Dictionary of opening: closing parenthesis types
        string_brackets_mapping = {'{': '}', '(': ')', '[': ']'}
        stack = list()

        for letter in string_to_check:
            try:
                stack.append(string_brackets_mapping[letter])
            except KeyError as ke:
                if letter not in string_brackets_mapping.values() or not stack or stack.pop() != letter:
                    return False
        return not stack


class Q5View(HTTPMethodView):
    def __init__(self):
        self.mapping = dict()
        super().__init__()

    @doc.summary('Egg dropping problem')
    @doc.consumes({'payload': {'eggs': int, 'floor': int}}, location='body', content_type='application/json')
    @doc.produces({'payload': {'payload': int}}, content_type='application/json')
    @doc.response(200, {'payload': {'payload': int}}, description='Success')
    async def post(self, request):
        if 'eggs' in request.json and 'floor' in request.json:
            result = self.drop_eggs(request.json['eggs'], request.json['floor'])
            return response.json({'payload': result})
        return response.json({'payload': False})

    def drop_eggs(self, number_of_eggs, number_of_floors):
        """
        Calculates the minimum number of experiments via recursively using memoization, need to find the critical floor
        in worst case:
        If we drop egg from X th floor there are 2 possibilities: eggs break[B] or not break [NB]
        - If [B] we have number_of_eggs = number_of_eggs - 1 and number_of_floors = X - 1
        - IF [NB] we have number_of_eggs = number_of_eggs(since we can reuse the non broken egg) and
        number_of_floors = number_of_floors - X
        """
        # Since we have one egg, we need to try number of floors or 1 floor or no floors
        if number_of_eggs == 1 or number_of_floors == 1 or number_of_floors == 0:
            return number_of_floors

        # To not recalculate the sub problems, using memoization
        if '{}-{}'.format(number_of_eggs, number_of_floors) in self.mapping:
            return self.mapping['{}-{}'.format(number_of_eggs, number_of_floors)]

        minimum = number_of_floors + 1
        # All droppings recursively, take maximum since we try to find worst case in terms of drop
        for floor in range(1, number_of_floors):
            result = max(self.drop_eggs(number_of_eggs - 1, floor - 1),
                         self.drop_eggs(number_of_eggs, number_of_floors - floor))
            if result < minimum:
                minimum = result
        self.mapping['{}-{}'.format(number_of_eggs, number_of_floors)] = minimum + 1
        return minimum + 1


class Q7View(HTTPMethodView):
    class Consumes:
        capacity = int
        carrots = [{'kg': int, 'price': int}]

    @doc.summary('Unlimited number of carrots, fill the bag')
    @doc.consumes({"payload": Consumes}, location='body',
                  content_type='application/json')
    @doc.produces({'payload': int}, content_type='application/json')
    @doc.response(200, {'payload': int}, description='Success')
    async def post(self, request):
        if 'capacity' in request.json and 'carrots' in request.json:
            result = self.get_max_value(request.json['carrots'], request.json['capacity'])
            return response.json({'payload': result})
        return response.json({'payload': 0})

    @staticmethod
    def get_max_value(carrot_types, capacity):
        """
        Using dynamic programming, iterate over all capacities for all carrots
        """
        # Initially zero 1D array
        known_values = [0] * (capacity + 1)
        for increasing_capacity in range(1, capacity + 1):
            for carrot in carrot_types:
                if carrot['kg'] <= increasing_capacity:
                    known_values[increasing_capacity] = max(known_values[increasing_capacity],
                                                            known_values[increasing_capacity - carrot['kg']] + carrot[
                                                                'price'])

        return known_values[capacity]


questions_blueprint.add_route(Q1View.as_view(), '/q1', strict_slashes=True)
questions_blueprint.add_route(Q2View.as_view(), '/q2', strict_slashes=True)
questions_blueprint.add_route(Q4View.as_view(), '/q4', strict_slashes=True)
questions_blueprint.add_route(Q5View.as_view(), '/q5', strict_slashes=True)
questions_blueprint.add_route(Q7View.as_view(), '/q7', strict_slashes=True)
