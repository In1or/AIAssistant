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
        url = "<url>"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Api-Key <Api key>"
        }

        response = requests.post(url, headers=headers, json=prompt)
        result = response.text

        return result
    

    def __create_define_prompt(self, requests_text, user_question):
        prompt = {
            "modelUri": "<uri>",
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
            "modelUri": "<uri>",
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
    
    def __create_determine_percentage_prompt(self, requests_text, user_question):
        prompt = {
            "modelUri": "<uri>",
            "completionOptions": {
                "stream": False,
                "temperature": 0.3,
                "maxTokens": "2000"
            },
            "messages": [
                {
                    "role": "system",
                    "text": f"""            
                    Запрос:

                    {requests_text}
                 
                    Определи в процентах от 1 до 100, НАЗОВЁМ ЭТО ЧИСЛО ВЕРОЯТНОСТЬЮ, насколько запрос соответствует вопросу пользователя, 
                    сравнивай контекст вопроса пользователя и запроса.
                    Отправь в ответе только число процентов, без знака процента %.
                    ЗАПОМНИ, ты должен отправить мне именно ВЕРОЯТНОСТЬ, насколько запрос соответствует вопросу пользователя.
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
            "modelUri": "<uri>",
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
    