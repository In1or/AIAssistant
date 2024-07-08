from asyncio.windows_events import NULL
from DatabaseManager.DatabaseManager import DatabaseManager
from YandexGPTManager.YandexGPTManager import YandexGPTManager

import json
import time
import re

class AIAssistantRemote:
    def __init__(self):
        self.__db = DatabaseManager()
        self.__model = YandexGPTManager()
        self.__incomplete_context = None
        self.__full_context = None
        self.delay = 0.5
        
    def get_answer(self, query):
        self.__incomplete_context = self.__db.get_incomplete_context()
        incomplete_context_for_prompt = self.__format_incomplete_context_for_prompt(self.__incomplete_context)
        
        print()
        print(incomplete_context_for_prompt)
        print()

        accurate_context = self.__model.get_define_context(incomplete_context_for_prompt, query["question"])
        number_request = self.__extract_number_in_text_from_response(accurate_context)
        
        self.__full_context = self.__db.get_full_context(number_request)
        full_context_for_prompt = self.__format_full_context_for_prompt(self.__full_context)
        
        print()
        print(full_context_for_prompt)
        print()

        time.sleep(self.delay)
        response_chance = self.__model.get_chance(full_context_for_prompt["request_header"], query["question"])
        chance_get_in_out_area_knowledge = self.__extract_number_in_text_from_response(response_chance)
        print(response_chance)
        
        if chance_get_in_out_area_knowledge <= 50:
            time.sleep(self.delay)
            model_response = self.__model.get_response_not_our_area_knowledge(query["question"])
            response_on_user_question = self.__extract_text_from_response(model_response)
            print(model_response)

            print()
            print(f"{chance_get_in_out_area_knowledge}% что вопрос пользователя подходит под нашу область")
            print()
        
            return response_on_user_question  

        time.sleep(self.delay)
        model_response = self.__model.get_response_user_question(full_context_for_prompt, query["question"])
        response_on_user_question = self.__extract_text_from_response(model_response)
        
        print(response_on_user_question)
        
        record = self.__prepare_log_data_record(query, number_request, response_on_user_question)
        self.__db.save_record_on_log_table(record)
        
        return response_on_user_question  

    def __format_incomplete_context_for_prompt(self, incomplete_context):
        incomplete_context_format_for_prompt = {}
        incomplete_context_format_list = json.loads(str(incomplete_context))
        incomplete_context_format_for_prompt = [{'ts_request_number': item['ts_request_number'], 'request_header': item['ts_query']} for item in incomplete_context_format_list]
        
        requests_text = "\n".join([f'{item["ts_request_number"]:2},"{item["request_header"]}"' for item in incomplete_context_format_for_prompt])
        
        return requests_text
        
    def __format_full_context_for_prompt(self, data):
        structured_data = {
            'ts_request_number': data["ts_request_number"],
            'request_header': data['ts_query'],
            'request_answer': data['ts_answer']
        }
    
        return structured_data

    def __extract_number_in_text_from_response(self, data):
        json_data = json.loads(data)
        number_request = json_data["result"]["alternatives"][0]["message"]["text"]

        numbers = re.findall(r'\d+', number_request)

        return int(numbers[0]) if numbers else None
    
    def __extract_text_from_response(self, data):
        json_data = json.loads(data)
        number_request = json_data["result"]["alternatives"][0]["message"]["text"]

        return number_request
    
    def __prepare_log_data_record(self, user, number_request, answer_on_user_question):
        print(user["username"])
        print(user["user_firstname"])
        username = user["username"] 
        if (user["username"] == None):
            username = user["user_firstname"]
        
        record = (username, user["question"], number_request, answer_on_user_question)
        
        return record