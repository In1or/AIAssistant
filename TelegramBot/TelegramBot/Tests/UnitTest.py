from asyncio.windows_events import NULL
from AIAssistant.AIAssistant import AIAssistantRemote
from DatabaseManager.DatabaseManager import DatabaseManager
from YandexGPTManager.YandexGPTManager import YandexGPTManager

# from TelegramBot import TelegramBot

import telebot
import unittest
import json
from unittest import mock, TestCase

# python -m unittest UnitTest.py

class UnitTest(unittest.TestCase):
    def setUp(self):
        self.__assistant = AIAssistantRemote()
        self.__db = DatabaseManager()
        self.__model = YandexGPTManager()
        
    def tearDown(self):
        
        pass
    
    def test_incomplete_full_context(self):
        incomplete_context = self.__db.get_incomplete_context()

        with open('TestData/incompleteContext.txt', 'r') as file:
            expected_result = file.read()

        self.assertEqual(incomplete_context, expected_result, "Ошибка в получении неполного контекста")
        

    def test_valid_request_number_get_full_context(self):
        full_context = self.__db.get_full_context(1)
        
        with open('TestData/fullContext.txt', 'r') as file:
            expected_result = json.load(file)
            
        self.assertDictEqual(full_context, expected_result, "Ошибка в получении полного контекста")
            
    def test_save_record_on_log_table(self):
        record = ("urik", "chto delat esli tu urik?", 32, "ya ne mogu vam pomoch, obrashaites eshe")
        status = self.__db.save_record_on_log_table(record)
        
        self.assertTrue(status, "Ошибка при сохранении записи в таблицу логов")


    def test_extract_generated_number_response(self):
        
        with open('TestData/generatedNumberResponse.txt', 'r') as file:
            expected_result = json.load(file)
            
        self.assertEqual('44', expected_result["result"]["alternatives"][0]["message"]["text"], "Ошибка при извлечении номера вопроса")

    def test_extract_generated_response(self):
        
        with open('TestData/generatedResponse.txt', 'r') as file:
            expected_result = json.load(file)
        
        if (expected_result["result"]["alternatives"][0]["message"]["text"] is not NULL ):
            check = True

        self.assertTrue(check, "Ошибка при извлечении сгенерированного ответа")

    def test_crate_define_prompt(self):
        
        context = self.__db.get_incomplete_context()
        
        provide_context = self.__assistant._AIAssistantRemote__format_incomplete_context_for_prompt(context)
        
        prompt = self.__model._YandexGPTManager__create_define_prompt(provide_context, "Актуализация")
        
        with open('TestData/promptDefine.txt', 'w', encoding='utf-8') as file:
            file.write(str(prompt))

        # with open('TestData/expectedPromptDefine.txt', 'w', encoding='utf-8') as file:
        #     file.write(str(prompt))
            
        with open('TestData/expectedPromptDefine.txt', 'r', encoding='utf-8') as file:
            expected_prompt = file.read()

        with open('TestData/promptDefine.txt', 'r', encoding='utf-8') as file:
            prompt = file.read()
        
        self.assertMultiLineEqual(prompt, expected_prompt, "error")