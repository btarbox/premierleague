# -*- coding: utf-8 -*-


import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name, get_supported_interfaces
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import get_supported_interfaces
from ask_sdk_model.ui import SimpleCard,StandardCard, Image
from ask_sdk_model import Response
from ask_sdk_model.interfaces.alexa.presentation.apl import RenderDocumentDirective as APLRenderDocumentDirective
from ask_sdk_model.interfaces.alexa.presentation.apla import RenderDocumentDirective as APLARenderDocumentDirective
import json
from random import randrange
from shared import datasources2, test_speach_data, noise_data, teamsdatasource

sb = SkillBuilder()
radioButtonText = "default"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def say_stats(handler_input, text_to_speak): 
        noise_index = randrange(0, 3)
        return (
            handler_input.response_builder
                .ask("this is the reprompt")
                .set_should_end_session(False)          
                .add_directive( 
                  APLARenderDocumentDirective(
                    token= "developer-provided-string",
                    document = {
                        "type" : "Link",
                        "src"  : "doc://alexa/apla/documents/template_with_data_sources"
                    },
                    datasources = {
                        "text": {
                          "speak": text_to_speak
                        },
                        "crowd": {
                            "noise": noise_data[noise_index][0],
                            "start": str(randrange(0, noise_data[noise_index][1]))
                        }
                        
                    }              
                  )
                ).response)


def go_home(handler_input):
    return (
        handler_input.response_builder
            .speak("Welcome to Premier League")
            .set_should_end_session(False)          
            .add_directive( 
              APLRenderDocumentDirective(
                token= "developer-provided-string",
                document = {
                    "type" : "Link",
                    "token" : "my token",
                    "src"  : "doc://alexa/apl/documents/GridList"
                },
                datasources = datasources2 
              )
            ).response
        )
    

def load_apl_document(file_path):
    with open(file_path) as f:
        logger.info("opened template file")
        return json.load(f)
        
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("*****  at handle launch request   *******")
        speech_text = "Welcome to the Alexa APLA demo"

        logger.info("about to return response")
        image_url = "https://duy7y3nglgmh.cloudfront.net/Depositphotos_referee.jpg"
        card = StandardCard(title="Premier League", text="bla", image=Image(small_image_url=image_url, large_image_url=image_url))

        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["radioButtonText"] = "Form"
        handler_input.attributes_manager.session_attributes = session_attr
        
        return(
        handler_input.response_builder
          #.speak("this is the speak")
          .ask("this is the ask").set_card(card).response)






class SimpleTextIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("SimpleTextIntent")(handler_input)

    def handle(self, handler_input):
        speech_text = "This is a simple spoken response"

        return (
            handler_input.response_builder
                .ask("this is the reprompt")
                .speak(speech_text).response
        )






class TextWithEmotionIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("TextWithEmotionIntent")(handler_input)

    def handle(self, handler_input):
        speech_text = "This is a simple spoken response \
                        <amazon:emotion name=\"excited\" intensity=\"high\"> \
                         with emotion indicators, Liverpool wins the league and so on and so \
                         on emotions take time \
                        </amazon:emotion>"
        return (
            handler_input.response_builder
                .ask("this is the reprompt")
                .speak(speech_text)
                .set_should_end_session(False).response
        )





class SimpleCardIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("SimpleCardIntent")(handler_input)

    def handle(self, handler_input):
        speech_text = "This is a simple spoken response with a simple card"

        return (
            handler_input.response_builder
                .ask("this is the reprompt")
                .speak(speech_text)
                .set_card(SimpleCard("Hello World", speech_text))
                .set_should_end_session(False).response
        )




class StandardCardIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("StandardCardIntent")(handler_input)

    def handle(self, handler_input):
        speech_text = "This is a simple spoken response with a standard card"
        image_url = "https://duy7y3nglgmh.cloudfront.net/tackles.png"
        card = StandardCard(title="Premier League", text=speech_text, image=Image(small_image_url=image_url, large_image_url=image_url))

        return (
            handler_input.response_builder
                .ask("this is the reprompt")
                .speak(speech_text)
                .set_card(card)
                .set_should_end_session(False).response
        )




class AudioMixIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AudioMixIntent")(handler_input)

    def handle(self, handler_input):
        card_text = "This is a AudioMixed response with a standard card"
        image_url = "https://duy7y3nglgmh.cloudfront.net/tackles.png"
        card = StandardCard(title="Premier League", text=card_text, image=Image(small_image_url=image_url, large_image_url=image_url))

        return (
            handler_input.response_builder
                .ask("this is the reprompt")
                .set_card(card)
                .set_should_end_session(False)          
                .add_directive( 
                  RenderDocumentDirective(
                    token= "developer-provided-string",
                    document = {
                        "type" : "Link",
                        "src"  : "doc://alexa/apla/documents/template_without_data_sources"
                    },
                    datasources = {}              
                  )
                ).response
        )




class AudioMixWithDataSourceIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AudioMixWithDataSourceIntent")(handler_input)

    def handle(self, handler_input):
        card_text = "This is a AudioMixed response with data and a standard card"
        image_url = "https://duy7y3nglgmh.cloudfront.net/tackles.png"
        card = StandardCard(title="Premier League", text=card_text, image=Image(small_image_url=image_url, large_image_url=image_url))

        return (
            handler_input.response_builder
                .ask("this is the reprompt")
                .set_card(card)
                .set_should_end_session(False)          
                .add_directive( 
                  RenderDocumentDirective(
                    token= "developer-provided-string",
                    document = {
                        "type" : "Link",
                        "src"  : "doc://alexa/apla/documents/template_with_data_sources"
                    },
                    datasources = {
                        "text": {
                          "speak": "This is the text that will be spoken at the same time the audio \
                          clip plays, it is dynamic and set by the lambda"
                        },
                        "crowd": {
                            "noise": "https://btbscratch.s3.amazonaws.com/FootballCrowdSound.mp3",
                            "start": str(randrange(0, 50*60))
                        }
                    }              
                  )
                ).response
        )



class GridMixIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("GridMixIntent")(handler_input)

    def handle(self, handler_input):
        card_text = "This is a GridMixed response with a standard card"
        image_url = "https://duy7y3nglgmh.cloudfront.net/tackles.png"
        card = StandardCard(title="Premier League", text=card_text, image=Image(small_image_url=image_url, large_image_url=image_url))
        if get_supported_interfaces(handler_input).alexa_presentation_apl is not None:
            return (
                handler_input.response_builder
                    .speak("Welcome to Premier League")
                    .set_should_end_session(False)          
                    .add_directive( 
                      APLRenderDocumentDirective(
                        token= "developer-provided-string",
                        document = {
                            "type" : "Link",
                            "token" : "my token",
                            "src"  : "doc://alexa/apl/documents/GridList"
                        },
                        datasources = datasources2 
                      )
                    ).response
                )
        else:
            return (handler_input.response_builder.speak("no screen for you").set_should_end_session(False).response)      


class ButtonEventHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # The user_event.source is a dict object. We can retrieve the id
        # using the get method on the dictionary.
        logger.info("at ButtonEventHandler")
        if is_request_type("Alexa.Presentation.APL.UserEvent")(handler_input):
            user_event = handler_input.request_envelope.request  # type: UserEvent
            return True
        else:
            return False
 
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("at ButtonEventHandler.handle " + str(handler_input.request_envelope.request))
        logger.info("at ButtonEventHandler.handle " + str(handler_input.request_envelope.request.source))
        logger.info("at ButtonEventHandler.handle " + str(handler_input.request_envelope.request.arguments))
        first_arg = handler_input.request_envelope.request.arguments[0]
        if first_arg == 'radio button':
            #radioButtonText = handler_input.request_envelope.request.arguments[1]
            logger.info(f"set radioButtonText to {radioButtonText}")
            session_attr = handler_input.attributes_manager.session_attributes
            session_attr["radioButtonText"] = handler_input.request_envelope.request.arguments[1]
            handler_input.attributes_manager.session_attributes = session_attr
            return
            
            
        if first_arg == "goBack":
            return(go_home(handler_input))
            
        if first_arg == "teams":
            return (
                handler_input.response_builder
                    .speak("Here is the page of just teams")
                    .set_should_end_session(False)          
                    .add_directive( 
                      APLRenderDocumentDirective(
                        token= "radio button page",
                        document = {
                            "type" : "Link",
                            "token" : "my token",
                            "src"  : "doc://alexa/apl/documents/RadioButtons"
                        },
                        datasources = teamsdatasource 
                      )
                    ).response
                )
            
        session_attr = handler_input.attributes_manager.session_attributes

        return say_stats(handler_input,test_speach_data.get(first_arg, first_arg + ", " + session_attr["radioButtonText"]))


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "You can say hello to me!"

        handler_input.response_builder.speak(speech_text).ask(
            speech_text).set_card(SimpleCard(
                "Hello World", speech_text))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Goodbye!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text))
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """
    This handler will not be triggered except in supported locales,
    so it is safe to deploy on any locale.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        logger.info("can_handle fallback")
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("handle fallback")
        # type: (HandlerInput) -> Response
        speech_text = (
            "The Hello World skill can't help you with that.  "
            "You can say hello!!")
        reprompt = "You can say hello!!"
        handler_input.response_builder.speak(speech_text).ask(reprompt)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speech = "Sorry, there was some problem. Please try again!!"
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response

class RequestLogger(AbstractRequestInterceptor):
    """Log the alexa requests."""
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.info("Alexa Request was: {}".format(
            handler_input.request_envelope.request))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the alexa responses."""
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.info("Alexa Response: {}".format(response))

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(SimpleTextIntentHandler())
sb.add_request_handler(TextWithEmotionIntentHandler())
sb.add_request_handler(SimpleCardIntentHandler())
sb.add_request_handler(StandardCardIntentHandler())
sb.add_request_handler(AudioMixIntentHandler())
sb.add_request_handler(GridMixIntentHandler())
sb.add_request_handler(ButtonEventHandler())
sb.add_request_handler(AudioMixWithDataSourceIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

sb.add_exception_handler(CatchAllExceptionHandler())

handler = sb.lambda_handler()
