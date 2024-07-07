import pyodbc
import json
import requests

class YandexGPTManager:
    def __init__(self):
        pass
    
    def get_define_context(self, context_for_define, user_question):
        prompt = self.__create_define_prompt(context_for_define, user_question) 
        define_context_result = self.send_prompt(prompt)    

        return define_context_result

    def get_response_user_question(self, context_for_answer, user_question):
        prompt = self.__create_response_prompt(context_for_answer['request_answer'], user_question)
        response_user_question_result = self.send_prompt(prompt)
        
        return response_user_question_result
    
    def get_chance(self, context_for_define, user_question):
        prompt = self.__create_determine_percentage_prompt(context_for_define, user_question)
        response_chance= self.send_prompt(prompt)
        
        return response_chance
    
    def get_response_not_our_area_knowledge(self, user_question):
        prompt = self.__create_response_not_our_area_knowledge_prompt(user_question)
        response_user_question_result = self.send_prompt(prompt)
        
        return response_user_question_result
        

    def send_prompt(self, prompt):
        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Api-Key AQVNy7tzUWsPXbDWnFrVplxqpJ6c6kcpSOPyb3ER"
        }

        response = requests.post(url, headers=headers, json=prompt)
        result = response.text

        return result
    

    def __create_define_prompt(self, requests_text, user_question):
        prompt = {
            "modelUri": "gpt://b1g9kfpcrc3g8ohj3tal/yandexgpt/latest",
            "completionOptions": {
                "stream": False,
                "temperature": 0.3,
                "maxTokens": "2000"
            },
            "messages": [
                {
                    "role": "system",
                    "text": f"""            
                    Ниже представлен нумерованный список запросов.
            
                    Список запросов в CSV формате:

                    {requests_text}
            
                    Выбери только один наиболее подходящий запрос из списка запросов, отправь в ответе только номер запроса.
                    ЗАПОМНИ, ты должен вернуть номер только числом из списка выше, от тебя требуется в ответе только одно число.
                    Не придумывай новые номера запросов. 
                    """
                },
                {
                    "role": "user",
                    "text": f"{user_question}"
                },
            ]
        }
        
        print()
        print(prompt)
        print()

        return prompt
    
    def __create_response_prompt(self, requests_text, user_question):
        prompt = {
            "modelUri": "gpt://b1g9kfpcrc3g8ohj3tal/yandexgpt/latest",
            "completionOptions": {
                "stream": False,
                "temperature": 0.3,
                "maxTokens": "2000"
            },
            "messages": [
                {
                    "role": "system",
                    "text": f"""Представь, что ты сотрудник технической поддержки в компании, к тебе обратился человек со своим вопросом. 
                        Переформулируй "текст ответа" на более простой, человечный язык. 
                        Отправь мне только переформулированный ответ и ничего больше. 
    
                        Текст ответа:

                    
                    {requests_text}. 
                    """
                },
                {
                    "role": "user",
                    "text": f"{user_question}"
                },
            ]
        }
        
        print()
        print(prompt)
        print()

        return prompt
    
    def __create_determine_percentage_prompt(self, requests_text, user_question): # , context_for_role_system
        prompt = {
            "modelUri": "gpt://b1g9kfpcrc3g8ohj3tal/yandexgpt/latest",
            "completionOptions": {
                "stream": False,
                "temperature": 0.3,
                "maxTokens": "2000"
            },
            "messages": [
                {
                    "role": "system",
                    "text": f"""            
                    Ниже представлен нумерованный список запросов.
            
                    Список запросов в CSV формате:

                    {requests_text}
            
                    Напиши в ответе процент шанса что предложенный список запросов сможет ответить на вопрос , отправь в ответе только число процента.
                    ЗАПОМНИ, ты должен вернуть процент только числом , от тебя требуется в ответе только одно число.
                    """
                },
                {
                    "role": "user",
                    "text": f"{user_question}"
                },
            ]
        }
        
        print()
        print(prompt)
        print()

        return prompt
    
    def __create_response_not_our_area_knowledge_prompt(self, user_question):
        prompt = {
            "modelUri": "gpt://b1g9kfpcrc3g8ohj3tal/yandexgpt/latest",
            "completionOptions": {
                "stream": False,
                "temperature": 0.3,
                "maxTokens": "2000"
            },
            "messages": [
                {
                    "role": "system",
                    "text": f"""            
                        Представь, что ты сотрудник технической поддержки в компании, к тебе обратился человек со своим вопросом. 
                        Ответь на его вопрос.
                        Не нужно писать поясняющий текст или приветствия
                        Отправь просто ответ
                    """
                },
                {
                    "role": "user",
                    "text": f"{user_question}"
                },
            ]
        }
        
        print()
        print(prompt)
        print()

        return prompt
    