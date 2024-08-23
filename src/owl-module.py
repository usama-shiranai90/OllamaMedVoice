import os
import time
from enum import Enum
from random import choice
from dotenv import load_dotenv

import pyaudio
import playsound
from gtts import gTTS
import speech_recognition as sr
from vosk import Model, KaldiRecognizer

# from langchain.prompts import PromptTemplate
# from langchain_openai import OpenAI
# from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI  # OpenAI
from langchain_core.runnables import RunnableSequence
from langchain_core.output_parsers import StrOutputParser

from typing import Optional


class Language(Enum):
    ENGLISH = "en-US"
    CHINESE = "zh-TW"
    KOREAN = "ko-KR"
    JAPANESE = "ja-JP"


def text_generation(text):
    prompt_templates = {
        "social_tech_lab": """
               You are an assistant chatbot named "SocialTechie". Your expertise is 
               exclusively in providing information and advice about anything related to social technology, social impact, and innovation labs. This includes discussions about technology for social good, startups focused on social impact, and related queries. You do not provide information outside of this 
               scope. If a question is not about social technology, respond with, "I specialize only in social technology related queries." 
               Question: {question} 
               Answer:""",

        "grameen": """
               You are an assistant chatbot with expertise in providing information about the Grameen Bank and its related activities. This includes topics like microfinance, social entrepreneurship, and financial inclusion efforts in developing countries. You do not provide information outside of this scope. If a question is not about Grameen Bank or related topics, respond with, "I specialize only in Grameen-related queries."
               Question: {question} 
               Answer:""",

        "medical_questions": """
               You are a medical assistant chatbot named "MedBot". Your expertise is 
               exclusively in answering medical questions. This includes general medical advice, information on medical conditions, and queries related to healthcare. You do not provide information outside of this 
               scope. If a question is not about medical topics, respond with, "I specialize only in medical-related queries." 
               Question: {question} 
               Answer:""",

        "medical_queries": """
               You are a medical assistant chatbot named "MedQ". Your expertise is 
               exclusively in handling medical queries. This includes responding to questions about symptoms, treatment options, and general medical advice. You do not provide information outside of this 
               scope. If a question is not about medical topics, respond with, "I specialize only in medical-related queries." 
               Question: {question} 
               Answer:""",

        "medical_domain": """
               You are an expert chatbot specializing in the medical domain. This includes providing detailed information on medical research, healthcare policies, and clinical practices. You do not provide information outside of this scope. If a question is not about the medical domain, respond with, "I specialize only in medical domain-related queries." 
               Question: {question} 
               Answer:""",

        "questions_related_to_bangladesh": """
               You are a chatbot specializing in questions related to Bangladesh. This includes topics like the culture, history, geography, and socio-economic conditions of Bangladesh. You do not provide information outside of this scope. If a question is not about Bangladesh, respond with, "I specialize only in queries related to Bangladesh." 
               Question: {question} 
               Answer:""",

        "kyushu_university": """
               You are a chatbot specializing in questions related to Kyushu University. This includes information about its programs, admissions, campus life, and research opportunities. You do not provide information outside of this scope. If a question is not about Kyushu University, respond with, "I specialize only in Kyushu University-related queries." 
               Question: {question} 
               Answer:"""
    }
    keyword_to_topic = {
        "social tech lab": "social_tech_lab",
        "grameen": "grameen",
        "medical question": "medical_questions",
        "medical query": "medical_queries",
        "medical domain": "medical_domain",
        "bangladesh": "questions_related_to_bangladesh",
        "kyushu university": "kyushu_university"
    }

    def determine_topic(query: str) -> Optional[str]:
        query_lower = query.lower()
        for keyword, topic in keyword_to_topic.items():
            if keyword in query_lower:
                return topic
        return None

    def get_prompt_template(t: str) -> PromptTemplate:
        return PromptTemplate(
            input_variables=["question"],
            template=prompt_templates.get(t, prompt_templates["social_tech_lab"])
        )

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    topic = determine_topic(text)
    if not topic:
        return "Sorry, I couldn't determine the appropriate topic for your query."

    summarizing_prompt = get_prompt_template(topic)
    summarizing_chain = summarizing_prompt | llm | StrOutputParser()
    print(topic, prompt_templates)
    response_text = summarizing_chain.invoke({'question': text})
    print(response_text)
    return response_text


def self_listen():
    with m as source:
        print("Please say something...")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=None)
            print("Got it! Now to recognize it...")
            return audio
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for a phrase to start.")
            return None


def text_to_speak(text, language=Language.ENGLISH.value):
    if language is Language.ENGLISH.value:
        response = gTTS(text=text, lang='en', tld='com.au')
    else:
        response = gTTS(text=text, lang='ja')

    directory = "raw"
    if not os.path.exists(directory):
        os.makedirs(directory)
    file = os.path.join(directory, "raw.mp3")  # TODO: Change to .wav on LINUX

    try:
        response.save(file)
        playsound.playsound(file)
        # os.system(f"start {file}")
    except PermissionError as e:
        # print("KILLING FILE")
        os.remove(file)
        response.save(file)
        playsound.playsound(file)
    time.sleep(0.5)


def speech_to_text(audio, language=Language.ENGLISH.value):
    audio_data = r.recognize_google(audio, language=language, show_all=True)
    text = ""
    confidence = ""
    if audio_data and "alternative" in audio_data:
        best_match_en = max(audio_data["alternative"], key=lambda x: x.get("confidence", 0))
        text = best_match_en["transcript"]
        confidence = best_match_en.get("confidence", 0)
    return confidence, text


def dynamic_check(audio, up_and_running):
    global default_language, is_started

    english = Language.ENGLISH.value
    japanese = Language.JAPANESE.value

    undetectable = False
    message = ""
    language = default_language
    try:
        confidence, text = speech_to_text(audio, language=language)
        if confidence < 0.60 or (language == Language.JAPANESE.value and confidence <= 0.91):
            print("English text =>", text)
            fallback_language = japanese if language == english else english
            confidence_, text = speech_to_text(audio, language=fallback_language)
            print(f"Recognized {fallback_language}: {text} (Confidence: {confidence_}) != {confidence}")
            language = fallback_language
            default_language = language
            is_started = True
        else:
            print(f"Recognized {language}: {text} (Confidence: {confidence})")
            is_started = True

        # confidence_en, text_en = speech_to_text(audio, language=language)
        # if confidence_en < 0.6:
        #     language = Language.JAPANESE.value
        #     confidence_ja, text_jp = speech_to_text(audio, language=language)
        #     print(f"Recognized Japanese: {text_jp} (Confidence: {confidence_ja})")
        # else:
        #     print(f"Recognized English: {text_en} (Confidence: {confidence_en})")
        # # if language is Language.ENGLISH.value:
        # #     confidence_en, text_en = speech_to_text(audio, language=language)
        # #     if confidence_en < 0.6:
        # #         language = Language.JAPANESE.value
        # #         confidence_ja, text_jp = speech_to_text(audio, language=language)
        # #         print(f"Recognized Japanese: {text_jp} (Confidence: {confidence_ja})")
        # #     else:
        # #         print(f"Recognized English: {text_en} (Confidence: {confidence_en})")
        # #
        # # elif language is Language.JAPANESE.value:
        # #     confidence_ja, text_jp = speech_to_text(audio, language=language)
        # #     if confidence_ja < 0.6:
        # #         language = Language.ENGLISH.value
        # #         confidence_en, text_en = speech_to_text(audio, language=language)
        # #         print(f"Recognized English: {text_en} (Confidence: {confidence_en})")
        # #     else:
        # #         print(f"Recognized Japanese: {text_jp} (Confidence: {confidence_ja})")

        # Change Manually Change
        change_language_words = change_language.get("English") if language == english else change_language.get(
            "Japanese")
        if text.lower() in change_language_words:
            undetectable = True
            is_started = False

        # print("==>", text.lower() in change_language_words, undetectable, is_started, up_and_running)
        if is_started and not up_and_running:
            wake_words_for_language = wake_words.get("English") if language == english else wake_words.get(
                "Japanese")
            # TODO: Correct condition.
            print(language == english, wake_words_for_language, text.lower() in wake_words_for_language)
            if text.lower() in wake_words_for_language:
                is_started, up_and_running = True, True
                print("Wake word detected....")
                if language == english:
                    text_to_speak(choice(greetings_dict.get("English")))
                else:
                    text_to_speak(choice(greetings_dict.get("Japanese")), japanese)
        elif is_started and up_and_running:
            # print("Up and Running Normal conversation in {} = {}".format(language, default_language))
            if default_language == Language.ENGLISH.value:
                response = text_generation(text)
                text_to_speak(response)

    except sr.UnknownValueError:
        message = "Could not understand audio in English or Japanese."
        # undetectable = True

    except sr.RequestError:
        message = "Service error for English or Japanese recognition."
        undetectable = True
    return message, undetectable, up_and_running


def manual_check(audio, language):
    text = ""
    try:
        confidence, text = speech_to_text(audio, language=language)
        print(f"Recognized {language}: {text} (Confidence: {confidence})")
        text = text_generation(text)
    except sr.UnknownValueError:
        text = "Could not understand audio in {}".format(language)
    except sr.RequestError:
        text = "Service error for {} recognition.".format(language)
    finally:
        text_to_speak(text)


def wake_up_call():
    global default_language
    with m as source:
        r.adjust_for_ambient_noise(source)
    # print("Set minimum energy threshold to {}".format(r.energy_threshold))
    up_and_running = False
    while True:
        audio = self_listen()
        if audio:
            message, undetectable, up_and_running = dynamic_check(audio, up_and_running)
            if undetectable:
                text_to_speak(choice(greetings_dict.get("English")))
                break

    print("here we are", undetectable, up_and_running)
    normal_state = False
    if undetectable:  # Manual language checker.
        while True:
            audio = self_listen()
            try:
                text = r.recognize_google(audio)
                print(f"You said: {text}")
                if not text:
                    continue

                if not normal_state:
                    if "english" in text.lower():
                        print("Language selected English")
                        default_language = Language.ENGLISH.value
                        normal_state = True
                    elif "japanese" in text.lower():
                        print("Language selected Japanese")
                        default_language = Language.JAPANESE.value
                        normal_state = True
                else:
                    if default_language == Language.ENGLISH.value:
                        response = text_generation(text)
                        text_to_speak(response)
                    # TODO: To create JAPANESE

            except sr.UnknownValueError:
                pass


if __name__ == "__main__":
    env = load_dotenv()
    name = "Social Tech Lab"
    wake_words = {
        "English": [
            "hey", "hello", "hellos", "hellow"
                                      "hey bot", "hello assistant",
            "wake up",
            "waked up",
            "start up",
            "activate",
            "wake up please",
            "are you there",
            "wake up now",
            "rise and shine",
            "is anyone there?",
            "wake up bot",
        ],
        "Japanese": [
            "起きて",  # Okite - Wake up
            "起動して",  # Kidō shite - Start up
            "目を覚まして",  # Me o samashite - Open your eyes / Wake up
            "反応して",  # Hannō shite - Respond
            "活動を開始して",  # Katsudō o kaishi shite - Start activity
            "動作開始",  # Dōsa kaishi - Begin operation
            "応答して",  # Ōtō shite - Reply
            "目覚めて",  # Mezamete - Wake up
            "スリープ解除",  # Surīpu kaijo - Exit sleep mode
            "起き上がって",  # Okiagatte - Get up
            "始動して",  # Shidō shite - Power on
            "アクティブにして",  # Akutibu ni shite - Become active
            "作動して",  # Sadō shite - Operate
            "起動",  # Kidō - Startup
            "スリープモードを解除",  # Surīpu mōdo o kaijo - Cancel sleep mode
            "起きろ",  # Okiro - Wake up (casual)
            "目を開けて",  # Me o akete - Open your eyes
            "起き上がれ",  # Okiagare - Get up (casual)
            "スタートして",  # Sutāto shite - Start
            "起きよう",  # Okirō - Let’s wake up
            "動き出して",  # Ugokidashite - Start moving
            "こんにちはロボット", "聞いて", "ハローアシスタント", "おーい", "注目",
            "こんにちは", "おはよう", "おはようございます", "もしもし", "やあ", "こんばんは"]
    }
    change_language = {
        "English": [
            "manual", "manual change", "manual changed",
            "change language",
            "switch language",
            "alter language",
            "change the language",
            "switch the language",
            "set language",
            "change language settings",
            "update language",
            "select language",
            "modify language",
            "language options",
            "change to english",
            "change to japanese",
            "switch to english",
            "switch to japanese",
            "change default language",
            "set default language",
            "manually change language",
            "adjust language",
            "change interface language",
            "choose language",
            "change system language",
            "language change",
            "language selection",
            "change to another language",
            "switch the default language",
            "update language settings",
            "set the language",
            "configure language",
            "select a new language",
            "switch language mode",
            "use english",
            "use japanese",
            "language shift",
            "change the spoken language",
        ],
        "Japanese": [
            "言語を変更",  # Gengo o henkō - Change language
            "言語を切り替え",  # Gengo o kirikae - Switch language
            "言語を変えて",  # Gengo o kaete - Change the language
            "言語の変更",  # Gengo no henkō - Language change
            "言語設定を変更",  # Gengo settei o henkō - Change language settings
            "言語の切り替え",  # Gengo no kirikae - Language switch
            "言語を手動で変更",  # Gengo o shudō de henkō - Manually change language
            "新しい言語を設定",  # Atarashī gengo o settei - Set a new language
            "使用言語を変更",  # Shiyō gengo o henkō - Change the language used
            "デフォルト言語を変更",  # Deforuto gengo o henkō - Change the default language
            "インターフェース言語を切り替え",  # Intāfēsu gengo o kirikae - Switch interface language
            "言語を選択",  # Gengo o sentaku - Select language
            "日本語に変更",  # Nihongo ni henkō - Change to Japanese
            "英語に変更",  # Eigo ni henkō - Change to English
            "言語オプションを変更",  # Gengo opushon o henkō - Change language options
            "言語設定を変更してください",  # Gengo settei o henkō shite kudasai - Please change the language settings
            "言語を英語にして",  # Gengo o eigo ni shite - Change the language to English
            "言語を日本語にして",  # Gengo o nihongo ni shite - Change the language to Japanese
            "使用中の言語を変更",  # Shiyō-chū no gengo o henkō - Change the currently used language
            "マニュアルで言語を変えて",  # Manyuaru de gengo o kaete - Change the language manually
        ]
    }
    greetings_dict = {
        "English": [
            f"Welcome to {name}, You have selected English.",
            f"Hey There, Are you excited about {name}? To continue, you have selected English.",
            f"Well, hello there, how's it going today in the {name}? You have selected English."
        ],
        "Japanese": [
            f"{name}へようこそ、あなたは日本語を選択しました。",
            f"こんにちは、{name}に興奮していますか？ 続けるには、日本語を選択しました。",
            f"こんにちは、{name}での今日はどうですか？ あなたは日本語を選択しました。"
        ]
    }

    # response = "What do you know about social tech lab Kyushu university?"
    # # response = text_generation("What do you know about social tech lab Kyushu university?")
    # text_to_speak(response)

    default_language = Language.ENGLISH.value
    is_started = False
    # model_path = "vosk-model-ja-0.22"
    # model = Model(model_path)
    # recognizer = KaldiRecognizer(model, 16000)
    # Set up the speech recognition and text-to-speech engines
    # r = sr.Recognizer()

    r = sr.Recognizer()
    m = sr.Microphone(device_index=2)
    try:
        wake_up_call()
    except KeyboardInterrupt:
        pass
