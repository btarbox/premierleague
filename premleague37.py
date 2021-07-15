# -*- coding: utf-8 -*-
"""
Python 3.7 version of PremierLeague.
TODO: 
full regression test
split source code into multiple files
add team sounds
copy india voice model to other models
"""
#from utility import foo, GoalsHandler
import shared
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

from ask_sdk_model.ui import SimpleCard, StandardCard, Image
from ask_sdk_model import Response
from ask_sdk_model.interfaces.alexa.presentation.apla import RenderDocumentDirective

from statshandlers import bla
from shared import extra_cmd_prompts, variedPrompts, doc, noise, noise2, noise3, noise_max_millis, noise2_max_millis, noise3_max_millis
from statshandlers import load_suggestions, suggest, strip_emotions, get_excitement_prefix, get_excitement_suffix,normalize_score, get_one_line, GoalsHandler, random_phrase, random_prompt, pluralize, load_stats, ListTeamNamesHandler, CleanSheetsHandler,FoulsHandler, RedCardHandler, YellowCardHandler, TouchesHandler, TacklesHandler, RefereesHandler

SKILL_NAME = "PremierLeague"
HELP_MESSAGE = "Say get table, a team name or nickname, red cards, yellow cards, clean sheets, golden boot, fixtures, results, relegation, referees, stadiums by name, touches, fouls and tackles"
HELP_REPROMPT = "What can we help you with?"
STOP_MESSAGE = "Okay, hope to see you next time!"
FALLBACK_MESSAGE = "Sorry, I did not understand, you can ask for help to get a list of things to ask me"
FALLBACK_REPROMPT = 'What can I help you with?'
EXCEPTION_MESSAGE = "Sorry,  I did not understand, you can ask for help to get a list of things to ask me"


sb = SkillBuilder()
sns_client = boto3.client('sns')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
WELCOME_MESSAGE = "Welcome to PremierLeague"
table_data = []
table_index = 0
#variedPrompts = ["Say get table, or say a team name ", "Ask about the table or a team", "What can we tell you about Premier League  ", "We can tell you about teams or the table"]

class WelcomeHandler(AbstractRequestHandler):
    """Handler for StartIntent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        logger.info("in can_handle StartHandler")
        return (is_request_type("LaunchRequest")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In WelcomeHandler")
        logger.info("test: " + shared.this_is_shared)
        #bla()
        load_suggestions()
        #suggest()
        #del extra_cmd_prompts["referees"]
        #load_main_table()
        reload_main_table_as_needed()
        logger.info("first place is {} and last place is {}".format(table_data[0][0], table_data[19][0]))
        
        speech = WELCOME_MESSAGE + ' Say get table, or say a team name '
        handler_input.response_builder.speak(speech).ask(speech).set_card(SimpleCard("Hello PremierLeague", speech))
        return handler_input.response_builder.response


class TeamHandler(AbstractRequestHandler):
    """Handler for TeamIntent."""

    def can_handle(self, handler_input):
        logger.info("in can_handle TeamHandler")
        logger.info("intent_name is " + get_intent_name(handler_input))
        return (is_intent_name("TeamIntent")(handler_input))

    def handle(self, handler_input):
        logger.info("In TeamHandler")
        card_text = ""
        reload_main_table_as_needed()
        slot = get_slot(handler_input, "plteam")
        dict = slot.resolutions.to_dict()
        success = dict['resolutions_per_authority'][0]["status"]["code"]
        if success == 'ER_SUCCESS_MATCH':
            team_id = dict['resolutions_per_authority'][0]["values"][0]["value"]["id"]
            team_name = dict['resolutions_per_authority'][0]["values"][0]["value"]["name"]
            logger.info("found team {} {}".format(team_id, team_name))
            if team_id == 'Southhampton':
                team_id = 'Southampton'
            this_team_index = find_team_index(team_id)
            if this_team_index == -1:
                logger.info("could not find team")
                speech = "count not find team"
                card_text = speech
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
                card_text = strip_emotions(speech + form)
                new_intent = f", you can also ask for fixtures or results for {team_name}"
                speech = speech + form + new_intent
        else:
            err_msg = "could not find team with that name, please try again or ask us for a list of team names"
            team_id = None
            logger.info(err_msg)
            speech = err_msg
        team_logos = ["Arsenal","AstonVilla","Brentford","BrightonAndHoveAlbion","Burnley", "Chelsea","CrystalPalace","Everton","LeedsUnited","LeicesterCity","Liverpool","ManchesterUnited","ManchesterCity","NewcastleUnited","NorwichCity","Southhampton","TottenhamHotspur","Watford","WestHamUnited","WolverhamptonWanderers" ]
        #if team_id in team_logos:
        if team_id is not None:
            #image_url = "https://bplskillimages.s3.amazonaws.com/" + team_id + ".png"
            image_url = "https://duy7y3nglgmh.cloudfront.net/" + team_id + ".png"
            card = StandardCard(title="Premier League", text=card_text, image=Image(small_image_url=image_url, large_image_url=image_url))
            logger.info("built standard card")
            handler_input.response_builder.ask(speech).set_card(card).add_directive(
              RenderDocumentDirective(
                token= "tok",
                document = {"type" : "Link", "src"  : doc},
                datasources = {"user": {"name": speech},"crowd": {"noise": noise,"start": str(randrange(0, noise_max_millis))}
                }
                )
            )
        else:    
            logger.info("built simple card")
            handler_input.response_builder.speak(speech).ask(speech).set_card(SimpleCard("Premier League", card_text))
        return handler_input.response_builder.response


class StadiumHandler(AbstractRequestHandler):
    """Handler for StadiumIntent."""

    def can_handle(self, handler_input):
        logger.info("in can_handle StadiumHandler")
        return (is_intent_name("StadiumIntent")(handler_input))

    def handle(self, handler_input):
        logger.info("In StadiumHandler")
        if "stadiums" in extra_cmd_prompts:
            del extra_cmd_prompts["stadiums"]
        slot = get_slot(handler_input, "stadiumType")
        dict = slot.resolutions.to_dict()
        success = dict['resolutions_per_authority'][0]["status"]["code"]
        if success == 'ER_SUCCESS_MATCH':
            stadium_id = dict['resolutions_per_authority'][0]["values"][0]["value"]["id"]
            stadium_name = dict['resolutions_per_authority'][0]["values"][0]["value"]["name"]
            logger.info("found stadium {} {}".format(stadium_id, stadium_name))

            s3 = boto3.client("s3")
            bucket = "bpltables"
            key = "stadiums/" + stadium_name
            logger.info('try to open file ' + bucket + ":" + key)
            resp = s3.get_object(Bucket=bucket, Key=key)
            body_str = resp['Body'].read().decode("utf-8")
            logger.info("converted streaming_body to string")
            
            speech = body_str
        else:
            logger.info("could not find stadium")
            speech = "Sorry, we could not find that stadium"
        #speech = "in development"
        card_text = "in development"
        
        handler_input.response_builder.speak(speech).ask(speech).set_card(SimpleCard("Stadium", card_text))
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
        
        handler_input.response_builderask(speech).set_card(SimpleCard("Hello PremierLeague", speech)).add_directive(
              RenderDocumentDirective(
                token= "tok",
                document = {"type" : "Link", "src"  : doc},
                datasources = {"user": {"name": speech},"crowd": {"noise2": noise,"start": str(randrange(0, noise2_max_millis))}
                }
                )
            )
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
        session_attr["which_list"] = "table"
        handler_input.attributes_manager.session_attributes = session_attr
        
        table_index = 0
        speech = 'The first five teams in the table are ' + build_table_fragment(table_index)
        card_text = strip_emotions(speech)
        speech = speech + ' Would you like to hear more?'
        
        handler_input.response_builder.ask(speech).set_card(SimpleCard("Premier League", card_text)).add_directive(
              RenderDocumentDirective(
                token= "tok",
                document = {"type" : "Link", "src"  : doc},
                datasources = {"user": {"name": speech},"crowd": {"noise": noise,"start": str(randrange(0, noise_max_millis))}
                }
                )
            )
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

        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["which_list"] = "fixtures"
        session_attr["fixture_index"] = 5
        handler_input.attributes_manager.session_attributes = session_attr
        
        speech, card_text = load_stats_ng(5, "fixtures2", " versus ", " ", "  ", 0, 2, -1, "")
        speech = intro + speech + ' Would you like to hear more?'
        
        handler_input.response_builder.ask(speech).set_card(SimpleCard("Fixtures", card_text)).add_directive(
              RenderDocumentDirective(
                token= "tok",
                document = {"type" : "Link", "src"  : doc},
                datasources = {"user": {"name": speech},"crowd": {"noise": noise,"start": str(randrange(0, noise_max_millis))}
                }
                )
            )
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
        result_phrases = ["the results for the recent match week were, ","last weeks results were ","last week saw  "]
        intro = random_phrase(0,2, result_phrases)
        
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["which_list"] = "results"
        session_attr["results_index"] = 5
        handler_input.attributes_manager.session_attributes = session_attr
        
        speech, card_text = load_stats_ng(5, "prevWeekFixtures", "  ", "  ", "  ", 0, 2, 1, "")
        speech = intro + speech + ',' + ' Would you like to hear more?'
        
        handler_input.response_builder.ask(speech).set_card(SimpleCard("Results", card_text)).add_directive(
              RenderDocumentDirective(
                token= "tok",
                document = {"type" : "Link", "src"  : doc},
                datasources = {"user": {"name": speech},"crowd": {"noise": noise,"start": str(randrange(0, noise_max_millis))}
                }
                )
            )
        return handler_input.response_builder.response


class TeamResultsHandler(AbstractRequestHandler):
    """Handler for TeamResultsIntent."""

    def can_handle(self, handler_input):
        logger.info("in can_handle TeamResultsHandler")
        return (is_intent_name("TeamResultsIntent")(handler_input))

    def handle(self, handler_input):
        logger.info("In TeamResultsHandler")
        if "teamresults" in extra_cmd_prompts:
            del extra_cmd_prompts["teamresults"]
            
        slot = get_slot(handler_input, "plteam")
        dict = slot.resolutions.to_dict()
        success = dict['resolutions_per_authority'][0]["status"]["code"]
        if success == 'ER_SUCCESS_MATCH':
            team_id = dict['resolutions_per_authority'][0]["values"][0]["value"]["id"]
            team_name = dict['resolutions_per_authority'][0]["values"][0]["value"]["name"]
    
        logger.info(f"asked about {team_name}")
        intro = f"recent results for {team_name} were"
        session_attr = handler_input.attributes_manager.session_attributes
        handler_input.attributes_manager.session_attributes = session_attr
        
        speech, card_text = load_stats_ng(5, "prevWeekFixtures", "  ", "  ", "  ", 0, 2, 1, team_name)
        speech = intro + speech + ',' + random_prompt()
        
        handler_input.response_builder.ask(speech).set_card(SimpleCard("Results", card_text)).add_directive(
              RenderDocumentDirective(
                token= "tok",
                document = {"type" : "Link", "src"  : doc},
                datasources = {"user": {"name": speech},"crowd": {"noise": noise3,"start": str(randrange(0, noise3_max_millis))}
                }
                )
            )
        return handler_input.response_builder.response


class TeamFixturesHandler(AbstractRequestHandler):
    """Handler for TeamFixturesIntent."""

    def can_handle(self, handler_input):
        logger.info("in can_handle TeamFixturesHandler")
        return (is_intent_name("TeamFixturesIntent")(handler_input))

    def handle(self, handler_input):
        logger.info("In TeamFixturesHandler")
        if "teamfixtures" in extra_cmd_prompts:
            del extra_cmd_prompts["teamfixtures"]
            
        slot = get_slot(handler_input, "plteam")
        dict = slot.resolutions.to_dict()
        success = dict['resolutions_per_authority'][0]["status"]["code"]
        if success == 'ER_SUCCESS_MATCH':
            team_id = dict['resolutions_per_authority'][0]["values"][0]["value"]["id"]
            team_name = dict['resolutions_per_authority'][0]["values"][0]["value"]["name"]
    
        logger.info(f"asked about {team_name}")
        intro = f"upcoming fixtures for {team_name} are"
        session_attr = handler_input.attributes_manager.session_attributes
        handler_input.attributes_manager.session_attributes = session_attr
        
        #speech, card_text = load_stats_ng(5, "fixtures2", "  ", "  ", "  ", 0, 2, 1, team_name)
        speech, card_text = load_stats_ng(5, "fixtures2", " versus ", " ", "  ", 0, 2, -1, team_name)
        speech = intro + speech + ',' + random_prompt()
        
        handler_input.response_builder.ask(speech).set_card(SimpleCard("Fixtures", card_text)).add_directive(
              RenderDocumentDirective(
                token= "tok",
                document = {"type" : "Link", "src"  : doc},
                datasources = {"user": {"name": speech},"crowd": {"noise": noise,"start": str(randrange(0, noise_max_millis))}
                }
                )
            )
        return handler_input.response_builder.response


class YesHandler(AbstractRequestHandler):
    """Handler for YesIntent."""

    def can_handle(self, handler_input):
        logger.info("in can_handle YesHandler")
        return (is_intent_name("AMAZON.YesIntent")(handler_input))

    def handle(self, handler_input):
        logger.info("In YesHandler")
        session_attr = handler_input.attributes_manager.session_attributes
        which_list = session_attr.get("which_list", "")
        if which_list == "table":
            current_table_index = session_attr.get('table_index', "")
            logger.info("current_table_index is {}".format(current_table_index))
            card_text = ""
            if current_table_index < 15:
                speech = 'The next five teams in the table are ' + build_table_fragment(current_table_index) 
                card_text = strip_emotions(speech)
                speech = speech + ' Would you like to hear more?'
                session_attr["table_index"] = current_table_index + 5
            else:
                speech = 'The last five teams in the table are ' + build_table_fragment(current_table_index) 
                card_text = strip_emotions(speech)
                speech = speech + random_prompt()
                session_attr["table_index"] = 0
            handler_input.attributes_manager.session_attributes = session_attr
    
            handler_input.response_builder.ask(speech).set_card(SimpleCard("Premier League", card_text)).add_directive(
              RenderDocumentDirective(
                token= "tok",
                document = {"type" : "Link", "src"  : doc},
                datasources = {"user": {"name": speech},"crowd": {"noise": noise,"start": str(randrange(0, noise_max_millis))}
                }
                )
            )
            return handler_input.response_builder.response
        elif which_list == "fixtures":
            intro = 'The next five fixtures are'
            fixture_index = session_attr.get("fixture_index", 0)
            session_attr["fixture_index"] = fixture_index + 5
            handler_input.attributes_manager.session_attributes = session_attr
            speech, card_text = load_stats_ng(5, "fixtures2", " versus ", " ", "  ", 0, 2, -1, "", fixture_index)
            speech = intro + speech + ' Would you like to hear more?'
            handler_input.response_builder.ask(speech).set_card(SimpleCard("Premier League", card_text)).add_directive(
              RenderDocumentDirective(
                token= "tok",
                document = {"type" : "Link", "src"  : doc},
                datasources = {"user": {"name": speech},"crowd": {"noise": noise,"start": str(randrange(0, noise_max_millis))}
                }
                )
            )
            return handler_input.response_builder.response
        else:
            intro = 'The next five results were'
            results_index = session_attr.get("results_index", 0)
            session_attr["results_index"] = results_index + 5
            handler_input.attributes_manager.session_attributes = session_attr
            speech, card_text = load_stats_ng(5, "prevWeekFixtures", "  ", "  ", "  ", 0, 2, 1, "", results_index)
            speech = intro + speech + ' Would you like to hear more?'
            handler_input.response_builder.ask(speech).set_card(SimpleCard("Premier League", card_text)).add_directive(
              RenderDocumentDirective(
                token= "tok",
                document = {"type" : "Link", "src"  : doc},
                datasources = {"user": {"name": speech},"crowd": {"noise": noise,"start": str(randrange(0, noise_max_millis))}
                }
                )
            )
            return handler_input.response_builder.response


class NoHandler(AbstractRequestHandler):
    """Handler for NoIntent."""

    def can_handle(self, handler_input):
        logger.info("in can_handle NoHandler")
        return (is_intent_name("AMAZON.NoIntent")(handler_input))

    def handle(self, handler_input):
        logger.info("In NoHandler")
        speech = random_prompt();
        handler_input.response_builder.speak(speech).ask(speech).set_card(SimpleCard("Premier League", speech))
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
        message = {"CatchAllExceptionHandler": "was called"}
        sns_client.publish(
            TargetArn="arn:aws:sns:us-east-1:747458360727:lambdatop",
            Message=json.dumps({'default': json.dumps(message)}),
            MessageStructure='json')
        handler_input.response_builder.speak(EXCEPTION_MESSAGE).ask(HELP_REPROMPT)

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
sb.add_request_handler(StadiumHandler())
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
sb.add_request_handler(TeamResultsHandler())
sb.add_request_handler(TeamFixturesHandler())

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
#extra_cmd_prompts = {}


def find_team_index(team_id):
    reload_main_table_as_needed()
    for index, team in enumerate(table_data):
        if team[NAME_INDEX].upper().replace(" ", "") == team_id.upper():
            return index
    return -1

    
def build_table_fragment(table_index):
    table_fragment = ""
    reload_main_table_as_needed()
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
    else:
        logger.info("did not need to load main table")

        
def load_main_table():
    s3 = boto3.client("s3")
    logger.info("about to open main table")
    resp = s3.get_object(Bucket="bpltables", Key="liveMainTable")
    logger.info("back from open main table")
    body_str = resp['Body'].read().decode("utf-8")
    logger.info("converted streaming_body to string")
    x = body_str.split("\n")
    team_index = 0
    #table_data.clear()
    #table_data = []

    for team in x:
        one_team = team.split(",")
        table_data.append(one_team)
        team_index = team_index + 1
        if team_index > 19:
            break
    table_index = 0
    logger.info("loaded {} teams into table_data".format(len(table_data)))


def load_stats_ng(number, filename, article1, article2, article3, firstCol, secondCol, thirdCol, team_to_match, lines_to_skip=0):
    say = ""
    card_text = ""
    s3 = boto3.client("s3")
    bucket = "bpltables"
    logger.info('try to open file ' + bucket + ":" + filename)
    resp = s3.get_object(Bucket=bucket, Key=filename)
    body_str = string_data = resp['Body'].read().decode("utf-8")
    logger.info("converted streaming_body to string")
    logger.info("load_stats_ng, lines_to_skip:" + str(lines_to_skip))
    #logger.info(body_str)
    n = body_str.split("\n")
    lines_in_file = len(n)
    logger.info(f"there are {len(n)} items in the list")
    oneCard = n[0].split(',')
    date_lines = 0;
    index = 0
    skip_index = 0
    while skip_index < (lines_to_skip):
        oneCard = n[index].split(',')
        if oneCard[0] == 'date':
            index += 1
            date_lines += 1;
            logger.info("increment index but don't increment lines to skip")
        else:
            index += 1
            skip_index += 1
            logger.info("we have seen one of the lines to skip")

    logger.info(f"index: {index} number:{number} date_lines: {date_lines} lines_to_skip: {lines_to_skip}")
    last_line_was_a_date = False
    
    while (index < (number + date_lines + lines_to_skip)) and (index < lines_in_file):
        oneCard = n[index].split(',')
        if oneCard[0] == 'date':
            if last_line_was_a_date == False:
                say += ' ' + oneCard[1] + ' '
                last_line_was_a_date = True
            date_lines += 1;
        else:
            third = oneCard[thirdCol] if thirdCol > -1 else ""
            new_text = get_one_line(oneCard[firstCol], article1, oneCard[secondCol], article2, third, article3)
            if team_matches(team_to_match, new_text):
                say = say + ", " + new_text
                card_text = card_text + new_text + "\n"
                last_line_was_a_date = False
            else:
                date_lines += 1
        index += 1
    return (say, strip_emotions(card_text))            


''' Accept a cannonical name from Speech Model such as "tottenhamhotspurs" , convert to name as in text files and look for a match'''
def team_matches(team_name, text_to_search):
    logger.info(f"team_matches {team_name} {text_to_search}")
    if team_name == "":
        return True
    cannonical_names = {
        #"as appears in table" : "as appears in results"
        "Arsenal"           : "Arsenal",
        "Aston Villa"       : "Aston Villa",
        "Burnley"           : "Burnley",
        "Brentford"         : "Brentford",
        "Brighton and Hove Albion" : "Brighton",
        "Chelsea"           : "Chelsea",
        "Everton"           : "Everton",
        "Leeds United"      : "Leeds",
        "Leicester City"    : "Leicester",
        "Liverpool"         : "Liverpool",
        "Manchester United" : "Man United",
        "Manchester City"   : "Man City",
        "Newcastle United"  : "Newcastle",
        "Norwich City"      : "Norwich",
        "Southampton"       : "Southampton",
        "Tottenham Hotspur" : "Spurs", 
        "Watford"           : "Watford",
        "West Ham United"   : "West Ham"
    }
    name_to_look_for = cannonical_names.get(team_name, "not found")
    match_index = text_to_search.find(name_to_look_for)
    if match_index == -1:
        logger.info(f"{name_to_look_for} not found in {text_to_search}")
    else:
        logger.info(f"{name_to_look_for} FOUND in {text_to_search}")
    return match_index != -1

