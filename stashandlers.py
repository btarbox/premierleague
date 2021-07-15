from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name, get_intent_name, get_slot, get_slot_value
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.interfaces.alexa.presentation.apla import RenderDocumentDirective

from ask_sdk_model.ui import SimpleCard, StandardCard, Image
from ask_sdk_model import Response
import shared
from shared import extra_cmd_prompts, variedPrompts, doc, noise, noise2, noise3, noise_max_millis, noise2_max_millis, noise3_max_millis
import logging
import random
from random import randrange
import re
import boto3

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# doc = "doc://alexa/apla/documents/unchanged_template_from_tools"
# noise  = "https://btbscratch.s3.amazonaws.com/FootballCrowdSound.mp3"
# noise2 = "https://btbscratch.s3.amazonaws.com/SoccerStadiumSoundEffect.mp3"
# noise3 = "https://btbscratch.s3.amazonaws.com/SportsStadiumCrowdCheering.mp3"
# noise_max_millis = 4 * 60 * 1000
# noise2_max_millis = 40 * 1000
# noise3_max_millis = 40 * 1000

class GoalsHandler(AbstractRequestHandler):
    """Handler for GoldenBootIntent."""

    def can_handle(self, handler_input):
        logger.info("in can_handle GoalsHandler")
        logger.info("intent_name is " + get_intent_name(handler_input))
        return (is_intent_name("GoldenBootIntent")(handler_input))


    def handle(self, handler_input):
        logger.info("In GoalsHandler")
        if "goals" in extra_cmd_prompts:
            del extra_cmd_prompts["goals"]
        goal_phrases = ["the players with the most goals are,","the highest scorers are, ","the top scorers are"]
        intro = random_phrase(0,2, goal_phrases)
        
        speech, card_text = load_stats(5, "goldenboot", ", with ", " has ", "  ", 1, 2, 4)
        speech = intro + speech + ',' + random_prompt()
        
        image_url = "https://duy7y3nglgmh.cloudfront.net/Depositphotos_goal.jpg"
        card = StandardCard(title="Premier League", text=card_text, image=Image(small_image_url=image_url, large_image_url=image_url))
        handler_input.response_builder.ask(speech).set_card( card ).add_directive(
              RenderDocumentDirective(
                token= "tok",
                document = {"type" : "Link", "src"  : doc},
                datasources = {"user": {"name": speech},"crowd": {"noise": noise,"start": str(randrange(0, noise_max_millis))}
                }
            )
        )
        return handler_input.response_builder.response


class ListTeamNamesHandler(AbstractRequestHandler):
    """Handler for ListTeamNamesIntent."""

    def can_handle(self, handler_input):
        logger.info("in can_handle ListTeamNamesHandler")
        return (is_intent_name("ListTeamNamesIntent")(handler_input))

    def handle(self, handler_input):
        logger.info("In ListTeamNamesHandler")
        team_name_phrases = ["We recognize the following team names","These are the teams in the best league in the world","The best teams are"]
        intro = random_phrase(0,2, team_name_phrases)
        speech  = ',,Arsenal, Aston Villa, Brentford, Brighton and Hove Albion, Burnley, Chelsea, Crystal Palace,'
        speech += 'Everton, Leeds, Leicester City, Liverpool, Manchester City, Manchester United, Newcastle United,'
        speech += 'Norwich City, Southampton, Tottenham Hotspur, Watford, West Ham United and Wolverhamton Wandereres,,'
        speech += 'You can also refer to teams by their nicknames like gunners or toffees'
        speech = intro + speech
        
        handler_input.response_builder.speak(speech).ask(speech).set_card(SimpleCard("Team Names", intro + speech))
        return handler_input.response_builder.response


class CleanSheetsHandler(AbstractRequestHandler):
    """Handler for CleanSheetsIntent."""

    def can_handle(self, handler_input):
        logger.info("in can_handle CleanSheetsHandler")
        return (is_intent_name("CleanSheetsIntent")(handler_input))

    def handle(self, handler_input):
        logger.info("In CleanSheetsHandler")
        if "cleansheets" in extra_cmd_prompts:
            del extra_cmd_prompts["cleansheets"]
        clean_phrases = ["the goalkeepers with the most clean sheets are,","the most clean sheets go to, ", "the keepers with the most clean sheets are"]
        intro = random_phrase(0,2, clean_phrases)
        
        speech, card_text = load_stats(5, "cleansheets", ", with ", " has ", "  ", 1, 2, 4)
        speech = intro + speech + ',' + random_prompt()
        
        image_url = "https://duy7y3nglgmh.cloudfront.net/Depositphotos_keeper.jpg"
        card = StandardCard(title="Premier League", text=card_text, image=Image(small_image_url=image_url, large_image_url=image_url))
        handler_input.response_builder.ask(speech).set_card(card).add_directive(
              RenderDocumentDirective(
                token= "tok",
                document = {"type" : "Link", "src"  : doc},
                datasources = {"user": {"name": speech},"crowd": {"noise": noise2,"start": str(randrange(0, noise2_max_millis))}
                }
            )
        )        
        return handler_input.response_builder.response


class FoulsHandler(AbstractRequestHandler):
    """Handler for FoulsIntent."""

    def can_handle(self, handler_input):
        logger.info("in can_handle FoulsHandler")
        return (is_intent_name("FoulsIntent")(handler_input))

    def handle(self, handler_input):
        logger.info("In FoulsHandler")
        if "fouls" in extra_cmd_prompts:
            del extra_cmd_prompts["fouls"]
        foul_phrases = ["the players with the most fouls are,","the most fouls were committed by, ","the top foulers were,"]
        intro = random_phrase(0,2, foul_phrases)
        
        speech, card_text = load_stats(5, "fouls", ", with ", " has ", "  ", 1, 2, 4)
        speech = intro + speech + ',' + random_prompt()
        
        image_url = "https://duy7y3nglgmh.cloudfront.net/Depositphotos_fouls.jpg"
        card = StandardCard(title="Premier League", text=card_text, image=Image(small_image_url=image_url, large_image_url=image_url))
        handler_input.response_builder.ask(speech).set_card(card).add_directive(
              RenderDocumentDirective(
                token= "tok",
                document = {"type" : "Link", "src"  : doc},
                datasources = {"user": {"name": speech},"crowd": {"noise": noise3,"start": str(randrange(0, noise3_max_millis))}
                }
            )
        )         
        return handler_input.response_builder.response


class YellowCardHandler(AbstractRequestHandler):
    """Handler for YellowCardIntent."""

    def can_handle(self, handler_input):
        logger.info("in can_handle YellowCardHandler")
        return (is_intent_name("YellowCardIntent")(handler_input))

    def handle(self, handler_input):
        logger.info("In YellowCardHandler")
        if "yellowcards" in extra_cmd_prompts:
            del extra_cmd_prompts["yellowcards"]
        yellow_phrases = ["the players with the most yellow cards are,", "the most cautioned players are, ", "the most booked players are,"]
        intro = random_phrase(0,2, yellow_phrases)
        
        speech, card_text = load_stats(5, "yellowcards", ", with ", " has ", "  ", 1, 2, 4)
        speech = intro + speech + ',' + random_prompt()
        
        image_url = "https://duy7y3nglgmh.cloudfront.net/yellowcard.png"
        card = StandardCard(title="Premier League", text=card_text, image=Image(small_image_url=image_url, large_image_url=image_url))
        handler_input.response_builder.ask(speech).set_card(card).add_directive(
              RenderDocumentDirective(
                token= "tok",
                document = {"type" : "Link", "src"  : doc},
                datasources = {"user": {"name": speech},"crowd": {"noise": noise3,"start": str(randrange(0, noise3_max_millis))}
                }
            )
        )        
        return handler_input.response_builder.response


class RedCardHandler(AbstractRequestHandler):
    """Handler for RedCardIntent."""

    def can_handle(self, handler_input):
        logger.info("in can_handle RedCardHandler")
        return (is_intent_name("RedCardIntent")(handler_input))

    def handle(self, handler_input):
        logger.info("In RedCardHandler")
        if "redcards" in extra_cmd_prompts:
            del extra_cmd_prompts["redcards"]
        red_phrases = ["the players with the most red cards are,","the most ejected players are, ","the players leaving their teams playing short the most are, "]
        intro = random_phrase(0,2, red_phrases)
        
        speech, card_text = load_stats(5, "redcards", ", with ", " has ", "  ", 1, 2, 4)
        speech = intro + speech + ',' + random_prompt();
        
        image_url = "https://duy7y3nglgmh.cloudfront.net/redcard.png"
        card = StandardCard(title="Premier League", text=card_text, image=Image(small_image_url=image_url, large_image_url=image_url))
        handler_input.response_builder.ask(speech).set_card(card).add_directive(
              RenderDocumentDirective(
                token= "tok",
                document = {"type" : "Link", "src"  : doc},
                datasources = {"user": {"name": speech},"crowd": {"noise": noise3,"start": str(randrange(0, noise3_max_millis))}
                }
            )
        )        
        return handler_input.response_builder.response


class TouchesHandler(AbstractRequestHandler):
    """Handler for TouchesIntent."""

    def can_handle(self, handler_input):
        logger.info("in can_handle TouchesHandler")
        return (is_intent_name("TouchesIntent")(handler_input))

    def handle(self, handler_input):
        logger.info("In TouchesHandler")
        if "touches" in extra_cmd_prompts:
            del extra_cmd_prompts["touches"]
        touch_phrases = ["the players with the most touches are,","the players touching the ball the most are, ", "the most touches go to, "]
        intro = random_phrase(0,2, touch_phrases)
        
        speech, card_text = load_stats(5, "touches", ", with ", " has ", "  ", 1, 2, 4)
        speech = intro + speech + ',' + random_prompt()
        
        image_url = "https://duy7y3nglgmh.cloudfront.net/Depositphotos_touches.jpg"
        card = StandardCard(title="Premier League", text=card_text, image=Image(small_image_url=image_url, large_image_url=image_url))
        handler_input.response_builder.ask(speech).set_card(card).add_directive(
              RenderDocumentDirective(
                token= "tok",
                document = {"type" : "Link", "src"  : doc},
                datasources = {"user": {"name": speech},"crowd": {"noise": noise,"start": str(randrange(0, noise1_max_millis))}
                }
            )
        )       
        return handler_input.response_builder.response


class TacklesHandler(AbstractRequestHandler):
    """Handler for TacklesIntent."""

    def can_handle(self, handler_input):
        logger.info("in can_handle TacklesHandler")
        return (is_intent_name("TacklesIntent")(handler_input))

    def handle(self, handler_input):
        logger.info("In TacklesHandler")
        if "tackles" in extra_cmd_prompts:
            del extra_cmd_prompts["tackles"]
        tackles_phrases = ["the players with the most tackles are,","the players tackling the most are, ", "the most tackles go to, "]
        intro = random_phrase(0,2, tackles_phrases)
        
        speech, card_text = load_stats(5, "tackles", ", with ", " has ", "  ", 1, 2, 4)
        speech = intro + speech + ',' + random_prompt()
        
        image_url = "https://duy7y3nglgmh.cloudfront.net/tackles.png"
        card = StandardCard(title="Premier League", text=card_text, image=Image(small_image_url=image_url, large_image_url=image_url))
        handler_input.response_builder.ask(speech).set_card(card).add_directive(
              RenderDocumentDirective(
                token= "tok",
                document = {"type" : "Link", "src"  : doc},
                datasources = {"user": {"name": speech},"crowd": {"noise": noise2,"start": str(randrange(0, noise2_max_millis))}
                }
            )
        )       
        return handler_input.response_builder.response


class RefereesHandler(AbstractRequestHandler):
    """Handler for RefereesIntent."""

    def can_handle(self, handler_input):
        logger.info("in can_handle RefereesHandler")
        return (is_intent_name("RefereesIntent")(handler_input))

    def handle(self, handler_input):
        logger.info("In RefereesHandler")
        if "referees" in extra_cmd_prompts:
            del extra_cmd_prompts["referees"]
        referees_phrases = ["the most used referees are, ","the referees who've called the most games are, ","the referees in charge of the most games are,  "]
        intro = random_phrase(0,2, referees_phrases)
        
        speech, card_text = load_stats(5, "referees", " ", " yellow cards and ", " red cards", 0, 3, 2)
        speech = intro + speech + ','
        speech = speech + random_prompt()
        
        image_url = "https://duy7y3nglgmh.cloudfront.net/Depositphotos_referee.jpg"
        card = StandardCard(title="Premier League", text=card_text, image=Image(small_image_url=image_url, large_image_url=image_url))
        handler_input.response_builder.ask(speech).set_card(card).add_directive(
              RenderDocumentDirective(
                token= "tok",
                document = {"type" : "Link", "src"  : doc},
                datasources = {"user": {"name": speech},"crowd": {"noise": noise2,"start": str(randrange(0, noise2_max_millis))}
                }
            )
        )         
        return handler_input.response_builder.response


def random_phrase(low, high, phrases):
    return phrases[randrange(low, high)];


def random_prompt():
    return variedPrompts[randrange(0, 3)] + suggest();
  
    
def pluralize(count, noun, ess):
    if int(count) == 1:
        return count + " " + noun
    else:
        return count + " " + noun + ess
        

def bla():
    logger.info("at function in statshandler")
    logger.info(shared.this_is_shared)
    
def load_suggestions():
    extra_cmd_prompts["touches"]      = ". you can also ask about touches"
    extra_cmd_prompts["fouls"]        = ". you can also ask about fouls"
    extra_cmd_prompts["tackles"]      = ". you can also ask about tackles"
    extra_cmd_prompts["stadiums"]     = ". you can also ask about Premier League stadiums by name"
    extra_cmd_prompts["referees"]     = ". you can also ask about referees"
    extra_cmd_prompts["fixtures"]     = ". you can also ask about fixtures"
    extra_cmd_prompts["results"]      = ". you can also ask about last weeks results"
    extra_cmd_prompts["teamfixtures"] = ". you can also ask about fixtures for a team"
    extra_cmd_prompts["teamresults"]  = ". you can also ask about results for a team"
    extra_cmd_prompts["relegation"]   = ". you can also ask about relegation"
    extra_cmd_prompts["redcards"]     = ". you can also say red cards"
    extra_cmd_prompts["yellowcards"]  = ". you can also say yellow card"
    extra_cmd_prompts["cleansheets"]  = ". you can also ask about clean sheets"
    extra_cmd_prompts["goals"]        = ". you can also ask about goals"

def suggest():
    suggestions_left = len(extra_cmd_prompts)
    logger.info("There are {} suggestions remaining".format(suggestions_left))
    sugs = " "
    if suggestions_left > 0:
        key,value = random.choice(list(extra_cmd_prompts.items()))
        #del extra_cmd_prompts[key]
        logger.info("suggesting " + value)
        return value
    else:
        load_suggestions()    
    return ""

def strip_emotions(str):
    try:
        index = str.index("<")
        index2 = str.index(">")
        str2 = str[:index] + str[index2+1:]
        return str2.replace("</amazon:emotion>","")
    except:
        return str

def get_excitement_prefix(index):
    ''' speak with excitement or disappointment but with some randomness '''
    
    high_or_medium = "high" if randrange(0,2)==0 else "medium"
    medium_or_low = "medium" if randrange(0,2)==0 else "low"
    
    if index < 5:
        return '<amazon:emotion name="excited" intensity="{}">'.format(high_or_medium)
    elif index < 10:
        return '<amazon:emotion name="excited" intensity="{}">'.format(medium_or_low)
    elif index < 15:
        return '<amazon:emotion name="disappointed" intensity="{}">'.format(medium_or_low)
    else:
        return '<amazon:emotion name="disappointed" intensity="high">'.format(high_or_medium)
        
        
def get_excitement_suffix():
    return '</amazon:emotion>'


def normalize_score(score):
    if score.find(" to ") != -1:
        res = score.split(" ")
        if res[2] > res[0]:
            score = res[2] + " " + res[1] + " " + res[0]
        score = score.replace("0", "nil")
        return score
    else:
        return score

    
def get_one_line(noun1, article1, noun2, article2, noun3, article3):
    found_number_or_none = re.search("[0-9]", noun1)
    found_number = False if found_number_or_none is None else True
    
    found_nil = noun1.find('nil')
    
    noun3 = normalize_score(noun3)
    if found_number or found_nil != -1:
        return noun1 + "<break time='350ms'/>" + noun2
    else:
        return noun1 + article1 + noun2 + article2 + noun3 + article3 + ","


def load_stats(number, filename, article1, article2, article3, firstCol, secondCol, thirdCol):
    say = ""
    card_text = ""
    s3 = boto3.client("s3")
    bucket = "bpltables"
    logger.info('try to open file ' + bucket + ":" + filename)
    resp = s3.get_object(Bucket=bucket, Key=filename)
    body_str = resp['Body'].read().decode("utf-8")
    logger.info("converted streaming_body to string")
    logger.info(body_str)
    n = body_str.split("\n")
    oneCard = n[0].split(',')
    
    for index in range(0,number):
        oneCard = n[index].split(',')
        third = oneCard[thirdCol] if thirdCol > -1 else ""
        new_text = get_one_line(oneCard[firstCol], article1, oneCard[secondCol], article2, third, article3)
        say = say + ", " + new_text
        card_text = card_text + new_text + "\n"
        logger.info("building at index {} {}".format(index, say))
    return (say, strip_emotions(card_text))
