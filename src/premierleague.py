# -*- coding: utf-8 -*-
"""Python version of PremierLeague."""

import random
import logging
import pprint
import json
import boto3
from random import randrange
import random
import re

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name, get_intent_name, get_slot, get_slot_value
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response


SKILL_NAME = "PremierLeague"
HELP_MESSAGE = "Say get table, a team name or nickname, red cards, yellow cards, clean sheets, golden boot, fixtures, results, relegation, referees, stadiums by name, touches, fouls and tackles"
HELP_REPROMPT = "What can I help you with?"
STOP_MESSAGE = "Okay, see you next time!"
FALLBACK_MESSAGE = "The PremierLeague skill can't help you with that. What can I help you with?"
FALLBACK_REPROMPT = 'What can I help you with?'
EXCEPTION_MESSAGE = "Sorry. I cannot help you with that."


sb = SkillBuilder()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
WELCOME_MESSAGE = "Welcome to Python PremierLeague"
table_data = []
table_index = 0
variedPrompts = ["Say get table, or say a team name ", "Ask about the table or a team", "Say a command ", "We can tell you about teams or the table"]

class WelcomeHandler(AbstractRequestHandler):
    """Handler for StartIntent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        logger.info("in can_handle StartHandler")
        return (is_request_type("LaunchRequest")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In WelcomeHandler")
        load_suggestions()
        load_main_table()
        logger.info("first place is {} and last place is {}".format(table_data[0][0], table_data[19][0]))
        speech = WELCOME_MESSAGE + ' Say get table, or say a team name '
        handler_input.response_builder.speak(speech).ask(speech).set_card(SimpleCard("Hello PremierLeague", speech))
        return handler_input.response_builder.response

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
        
        handler_input.response_builder.speak(speech).ask(speech).set_card(SimpleCard("Goals", card_text))
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
        speech  = ',,Arsenal, Aston Villa, Bournemouth, Brighton and Hove Albion, Burnley, Chelsea, Crystal Palace,'
        speech += 'Everton, Leicester City, Liverpool, Manchester City, Manchester United, Newcastle United,'
        speech += 'Norwich City, Sheffield United, Southampton, Tottenham Hotspur, Watford, West Ham United and Wolverhamton Wandereres,,'
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
        
        handler_input.response_builder.speak(speech).ask(speech).set_card(SimpleCard("Goals", card_text))
        return handler_input.response_builder.response


class ResultsHandler(AbstractRequestHandler):
    """Handler for ResultsIntent."""

    def can_handle(self, handler_input):
        logger.info("in can_handle ResultsHandler")
        return (is_intent_name("ResultsIntent")(handler_input))

    def handle(self, handler_input):
        logger.info("In ResultsHandler")
        if "results" in extra_cmd_prompts:
            del extra_cmd_prompts["results"]
        result_phrases = ["the results for the last match week were, ","last weeks results were ","last week saw  "]
        intro = random_phrase(0,2, result_phrases)
        
        speech, card_text = load_stats(10, "prevWeekFixtures", "  ", "  ", "  ", 0, 2, 1)
        speech = intro + speech + ',' + random_prompt();
        
        handler_input.response_builder.speak(speech).ask(speech).set_card(SimpleCard("Results", card_text))
        return handler_input.response_builder.response


class FixturesHandler(AbstractRequestHandler):
    """Handler for FixturesIntent."""

    def can_handle(self, handler_input):
        logger.info("in can_handle FixturesHandler")
        return (is_intent_name("FixturesIntent")(handler_input))

    def handle(self, handler_input):
        logger.info("In FixturesHandler")
        if "fixtures" in extra_cmd_prompts:
            del extra_cmd_prompts["fixtures"]
        fixture_phrases = ["the fixtures for the current upcoming match week are,", "next week we'll see", "the next games are,"]
        intro = random_phrase(0,2, fixture_phrases)
        
        speech, card_text = load_stats_ng(10, "fixtures2", " versus ", " ", "  ", 0, 2, -1)
        speech = intro + speech + ',' + random_prompt()
        
        handler_input.response_builder.speak(speech).ask(speech).set_card(SimpleCard("Fixtures", card_text))
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
        
        handler_input.response_builder.speak(speech).ask(speech).set_card(SimpleCard("Fouls", card_text))
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
        
        handler_input.response_builder.speak(speech).ask(speech).set_card(SimpleCard("Yellow Cards", card_text))
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
        
        handler_input.response_builder.speak(speech).ask(speech).set_card(SimpleCard("Red Cards", card_text))
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
        
        handler_input.response_builder.speak(speech).ask(speech).set_card(SimpleCard("Touches", card_text))
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
        
        handler_input.response_builder.speak(speech).ask(speech).set_card(SimpleCard("Tackles", card_text))
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
        handler_input.response_builder.speak(speech).ask(speech).set_card(SimpleCard("Referees", card_text))
        return handler_input.response_builder.response


class TeamHandler(AbstractRequestHandler):
    """Handler for TeamIntent."""

    def can_handle(self, handler_input):
        logger.info("in can_handle TeamHandler")
        logger.info("intent_name is " + get_intent_name(handler_input))
        return (is_intent_name("TeamIntent")(handler_input))

    def handle(self, handler_input):
        logger.info("In TeamHandler")
        reload_main_table_as_needed()
        slot = get_slot(handler_input, "plteam")
        dict = slot.resolutions.to_dict()
        success = dict['resolutions_per_authority'][0]["status"]["code"]
        if success == 'ER_SUCCESS_MATCH':
            team_id = dict['resolutions_per_authority'][0]["values"][0]["value"]["id"]
            team_name = dict['resolutions_per_authority'][0]["values"][0]["value"]["name"]
            logger.info("found team {} {}".format(team_id, team_name))
            this_team_index = find_team_index(team_id)
            if this_team_index == -1:
                logger.info("could not find team")
            else:
                speech = "You asked about " + team_name + ", their form is "
                form = say_place(this_team_index + 1) + " with " + pluralize(table_data[this_team_index][WINS_INDEX], "win", 's') + ", "
                form = form + pluralize(table_data[this_team_index][DRAWS_INDEX], " draw", 's') + ", "
                form = form + pluralize(table_data[this_team_index][LOSSES_INDEX], " loss", 'es') + ", "
                form = form + pluralize(table_data[this_team_index][GOALS_FOR_INDEX], " goal", 's') + " scored, "
                form = form + pluralize(table_data[this_team_index][GOALS_AGAINST_INDEX], " goal", 's') + " allowed, "
                form = form + " for a goal difference of " + table_data[this_team_index][GOAL_DIFF_INDEX] + ", and "
                form = form + pluralize(table_data[this_team_index][POINTS_INDEX], " point", 's') + ", "
                form = get_excitement_prefix(this_team_index) + form + get_excitement_suffix()
                speech = speech + form + random_prompt()
        else:
            err_msg = "could not find team with that name, please try again or ask us for a list of team names"
            logger.info(err_msg)
            speech = err_msg
        
        handler_input.response_builder.speak(speech).ask(speech).set_card(SimpleCard("Hello PremierLeague", speech))
        return handler_input.response_builder.response


class RelegationHandler(AbstractRequestHandler):
    """Handler for RelegationIntent."""

    def can_handle(self, handler_input):
        logger.info("in can_handle RelegationHandler")
        return (is_intent_name("RelegationIntent")(handler_input))

    def handle(self, handler_input):
        logger.info("In RelegationHandler")
        if "relegation" in extra_cmd_prompts:
            del extra_cmd_prompts["relegation"]
        relegation_phrases = ["in the relegation zone ","facing relegation","in danger "];
        thisPhrase = random_phrase(0,2, relegation_phrases);
        speech = "the teams currently " + thisPhrase + " are " + build_relegation_fragment();
        speech = speech + ',' + random_prompt()
        
        handler_input.response_builder.speak(speech).ask(speech).set_card(SimpleCard("Hello PremierLeague", speech))
        return handler_input.response_builder.response


class TableHandler(AbstractRequestHandler):
    """Handler for TableIntent."""

    def can_handle(self, handler_input):
        logger.info("in can_handle TableHandler")
        return (is_intent_name("TableIntent")(handler_input))

    def handle(self, handler_input):
        logger.info("In TableHandler")
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["table_index"] = 5
        handler_input.attributes_manager.session_attributes = session_attr
        
        table_index = 0
        speech = 'The first five teams in the table are ' + build_table_fragment(table_index) + ' Would you like to hear more?'
        
        handler_input.response_builder.speak(speech).ask(speech).set_card(SimpleCard("Hello PremierLeague", speech))
        return handler_input.response_builder.response


class YesHandler(AbstractRequestHandler):
    """Handler for YesIntent."""

    def can_handle(self, handler_input):
        logger.info("in can_handle YesHandler")
        return (is_intent_name("AMAZON.YesIntent")(handler_input))

    def handle(self, handler_input):
        logger.info("In YesHandler")
        session_attr = handler_input.attributes_manager.session_attributes
        current_table_index = session_attr.get('table_index', "")
        logger.info("current_table_index is {}".format(current_table_index))
        if current_table_index < 15:
            speech = 'The next five teams in the table are ' + build_table_fragment(current_table_index) + ' Would you like to hear more?'
            session_attr["table_index"] = current_table_index + 5
        else:
            speech = 'The last five teams in the table are ' + build_table_fragment(current_table_index) + random_prompt()
            session_attr["table_index"] = 0
        handler_input.attributes_manager.session_attributes = session_attr

        handler_input.response_builder.speak(speech).ask(speech).set_card(SimpleCard("Hello PremierLeague", speech))
        return handler_input.response_builder.response


class NoHandler(AbstractRequestHandler):
    """Handler for NoIntent."""

    def can_handle(self, handler_input):
        logger.info("in can_handle NoHandler")
        return (is_intent_name("AMAZON.NoIntent")(handler_input))

    def handle(self, handler_input):
        logger.info("In NoHandler")
        speech = random_prompt();
        handler_input.response_builder.speak(speech).ask(speech).set_card(SimpleCard("Hello PremierLeague", speech))
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")

        handler_input.response_builder.speak(HELP_MESSAGE).ask(
            HELP_REPROMPT).set_card(SimpleCard(
                SKILL_NAME, HELP_MESSAGE))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In CancelOrStopIntentHandler")

        handler_input.response_builder.speak(STOP_MESSAGE)
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for Fallback Intent.

    AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")

        handler_input.response_builder.speak(FALLBACK_MESSAGE).ask(
            FALLBACK_REPROMPT)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")

        logger.info("Session ended reason: {}".format(
            handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response


# Exception Handler
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.info("In CatchAllExceptionHandler")
        logger.error(exception, exc_info=True)

        handler_input.response_builder.speak(EXCEPTION_MESSAGE).ask(
            HELP_REPROMPT)

        return handler_input.response_builder.response


# Request and Response loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the alexa requests."""
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.debug("Alexa Request: {}".format(
            handler_input.request_envelope.request))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the alexa responses."""
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.debug("Alexa Response: {}".format(response))


# Register intent handlers
#sb.add_request_handler(GetNewFactHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(WelcomeHandler())
sb.add_request_handler(RelegationHandler())
sb.add_request_handler(TableHandler())
sb.add_request_handler(YesHandler())
sb.add_request_handler(NoHandler())
sb.add_request_handler(TeamHandler())
sb.add_request_handler(ListTeamNamesHandler())
#sb.add_request_handler(StadiumHandler())
sb.add_request_handler(RefereesHandler())
sb.add_request_handler(GoalsHandler())
sb.add_request_handler(TouchesHandler())
sb.add_request_handler(FoulsHandler())
sb.add_request_handler(TacklesHandler())
sb.add_request_handler(CleanSheetsHandler())
sb.add_request_handler(RedCardHandler())
sb.add_request_handler(YellowCardHandler())
sb.add_request_handler(FixturesHandler())
sb.add_request_handler(ResultsHandler())

# Register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# TODO: Uncomment the following lines of code for request, response logs.
# sb.add_global_request_interceptor(RequestLogger())
# sb.add_global_response_interceptor(ResponseLogger())

# Handler name that is used on AWS lambda
lambda_handler = sb.lambda_handler()


######################## Utility functions #######################
NAME_INDEX = 0
PLAYED_INDEX = 1
WINS_INDEX = 2
DRAWS_INDEX = 3
LOSSES_INDEX = 4
GOALS_FOR_INDEX = 5
GOALS_AGAINST_INDEX = 6
GOAL_DIFF_INDEX = 7
POINTS_INDEX = 8
extra_cmd_prompts = {}

def find_team_index(team_id):
    reload_main_table_as_needed()
    index = 0
    for team in table_data:
        if team[0].upper().replace(" ", "") == team_id.upper():
            return index
        index = index + 1
    return -1

    
def random_phrase(low, high, phrases):
    return phrases[randrange(low, high)];


def random_prompt():
    return variedPrompts[randrange(0, 3)] + suggest();
  
    
def pluralize(count, noun, ess):
    if int(count) == 1:
        return count + " " + noun
    else:
        return count + " " + noun + ess

def load_suggestions():
    extra_cmd_prompts["touches"] = ". you can also ask about touches"
    extra_cmd_prompts["fouls"] = ". you can also ask about fouls"
    extra_cmd_prompts["tackles"] = ". you can also ask about tackles"
    extra_cmd_prompts["stadiums"] = ". you can also ask about Premier League stadiums by name"
    extra_cmd_prompts["referees"] = ". you can also ask about referees"
    extra_cmd_prompts["fixtures"] = ". you can also ask about fixtures"
    extra_cmd_prompts["results"] = ". you can also ask about last weeks results"
    extra_cmd_prompts["relegation"] = ". you can also ask about relegation"
    extra_cmd_prompts["redcards"] = ". you can also say red cards"
    extra_cmd_prompts["yellowcards"] = ". you can also say yellow card"
    extra_cmd_prompts["cleansheets"] = ".  you can also ask about clean sheets"
    extra_cmd_prompts["goals"] = ". you can also ask about goals"


def suggest():
    suggestions_left = len(extra_cmd_prompts)
    logger.info("There are {} suggestions remaining".format(suggestions_left))
    sugs = " "
    if suggestions_left > 0:
        key,value = random.choice(list(extra_cmd_prompts.items()))
        del extra_cmd_prompts[key]
        return value
    return ""

    
def build_table_fragment(table_index):
    table_fragment = ""
    for index in range(table_index, table_index+5):
        table_fragment = table_fragment + say_place(index+1) + " " + table_data[index][NAME_INDEX] + " with " + pluralize(table_data[index][POINTS_INDEX], 'point', 's') + ', '
    returned_str = get_excitement_prefix(table_index) + table_fragment + get_excitement_suffix()
    table_index = table_index + 5
    return returned_str

    
def build_relegation_fragment():
    logger.info("at build_relegation_fragment")
    reload_main_table_as_needed()
    logger.info("there are now {} teams in the table_data".format(len(table_data)))
    relegation_fragment = ""
    for index in range(17,20):
        logger.info("index {}".format(index))
        logger.info("name {}".format(table_data[index][NAME_INDEX]))
        logger.info("points {}".format(pluralize(table_data[index][POINTS_INDEX], 'point', 's')))
        
        relegation_fragment = relegation_fragment + say_place(index+1) + " " + table_data[index][NAME_INDEX] + " with " + pluralize(table_data[index][POINTS_INDEX], 'point', 's') + ', '
    return '<amazon:emotion name="disappointed" intensity="high">' + relegation_fragment + '</amazon:emotion>'
    

def get_excitement_prefix(index):
    ''' speak with excitement or disappointment but with some randomness '''
    
    high_or_medium = "high" if randrange(0,2)==0 else "medium"
    medium_or_low = "medium" if randrange(0,2)==0 else "low"
    
    if index < 5:
        return '<amazon:emotion name="excited" intensity="{}">'.format(high_or_medium)
    elif index < 10:
        return '<amazon:emotion name="excited" intensity="{}">'.format(medium_or_low)
    elif index < 10:
        return '<amazon:emotion name="disappointed" intensity="{}">'.format(medium_or_low)
    else:
        return '<amazon:emotion name="disappointed" intensity="high">'.format(high_or_medium)
        
        
def get_excitement_suffix():
    return '</amazon:emotion>'

        
def say_place(table_index):
    if table_index == 1:
        return "first place"
    elif table_index == 2:
        return "second place"
    elif table_index == 3:
        return "third place"
    else:
        return str(table_index) + "th place"

    
def reload_main_table_as_needed():
    if len(table_data) == 0:
        logger.info("needed to reload main table")
        load_main_table()

        
def load_main_table():
    s3 = boto3.client("s3")
    logger.info("about to open main table")
    resp = s3.get_object(Bucket="bpltables", Key="liveMainTable")
    logger.info("back from open main table")
    body_str = string_data = resp['Body'].read().decode("utf-8")
    logger.info("converted streaming_body to string")
    x = body_str.split("\n")
    team_index = 0
    for team in x:
        one_team = team.split(",")
        table_data.append(one_team)
        team_index = team_index + 1
        if team_index > 19:
            break
    table_index = 0
    logger.info("loaded {} teams into table_data".format(len(table_data)))


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

    
def load_stats_ng(number, filename, article1, article2, article3, firstCol, secondCol, thirdCol):
    say = ""
    card_text = ""
    s3 = boto3.client("s3")
    bucket = "bpltables"
    logger.info('try to open file ' + bucket + ":" + filename)
    resp = s3.get_object(Bucket=bucket, Key=filename)
    body_str = string_data = resp['Body'].read().decode("utf-8")
    logger.info("converted streaming_body to string")
    logger.info(body_str)
    n = body_str.split("\n")
    oneCard = n[0].split(',')
    date_lines = 0;
    index = 0
    while index < (number + date_lines):
        oneCard = n[index].split(',')
        if oneCard[0] == 'date':
            say += ' ' + oneCard[1] + ' '
            date_lines += 1;
        else:
            third = oneCard[thirdCol] if thirdCol > -1 else ""
            new_text = get_one_line(oneCard[firstCol], article1, oneCard[secondCol], article2, third, article3)
            say = say + ", " + new_text
            card_text = card_text + new_text + "\n"
        index += 1
    return (say, card_text)            

    
def load_stats(number, filename, article1, article2, article3, firstCol, secondCol, thirdCol):
    say = ""
    card_text = ""
    s3 = boto3.client("s3")
    bucket = "bpltables"
    logger.info('try to open file ' + bucket + ":" + filename)
    resp = s3.get_object(Bucket=bucket, Key=filename)
    body_str = string_data = resp['Body'].read().decode("utf-8")
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
    return (say, card_text)
