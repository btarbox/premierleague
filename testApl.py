# -*- coding: utf-8 -*-

# This is a simple Hello World Alexa Skill, built using
# the implementation of handler classes approach in skill builder.
import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name, get_supported_interfaces
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import get_supported_interfaces
from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response
#from ask_sdk_model.interfaces.alexa.presentation.apl import (RenderDocumentDirective)
from ask_sdk_model.interfaces.alexa.presentation.apla import RenderDocumentDirective
import json


sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

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
        speech_text = "Welcome to the Alexa Skills Kit, you can say hello!"

        # directive =  [
        #       {
        #         "type": "Alexa.Presentation.APL.RenderDocument",
        #         "token": {
        #           "document": {
        #             "type": "Link",
        #             "src": "doc://alexa/apla/documents/test_crowd_noise"
        #           }
        #         }
        #       }
        #     ]
        
        # return(
        #     handler_input.response_builder.add_directive({
        #             "object_type": 'Alexa.Presentation.APLA.RenderDocument',
        #             "version": '0.91',
        #             "document": load_apl_document("hello.json"),
        #     }))
        
        # return(
        #     handler_input.response_builder
        #     .add_directive({
        #         "type": "Alexa.Presentation.APLA.RenderDocument",
        #         "token": "mytoken",
        #         "document": {
        #             "type":"Link",
        #             "src":  "doc://alexa/apla/documents/test_crowd_noise"
        #         }, }               
        #     )
        # )
        #if get_supported_interfaces(handler_input).alexa_presentation_apl is not None:
        logger.info("about to return response")
        return(
        handler_input.response_builder
          #.speak("this is the speak")
          .ask("this is the ask")
          .add_directive( 
              RenderDocumentDirective(
                token= "developer-provided-string",
                document = {
                "type" : "Link",
                "src"  : "doc://alexa/apla/documents/unchanged_template_from_tools"
                },
                datasources = {
                    "user": {
                      "name": "Brian Guthrie Tarbox"
                      }
                }              
            )
            ).response
        )
        # else:
        #     return(handler_input.response_builder.speak("complex voice not supported").ask("try again").response)

        #logger.info("build response")
        #return handler_input.response_builder.response
                # "document": {
                #  "type": "Link",
                #  "src":  "doc://alexa/apla/documents/test_crowd_noise",


class HelloWorldIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Hello Python World from Classes!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
            True)
        return handler_input.response_builder.response


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
        logger.info("Alexa Request: {}".format(
            handler_input.request_envelope.request))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the alexa responses."""
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.info("Alexa Response: {}".format(response))

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

sb.add_exception_handler(CatchAllExceptionHandler())

handler = sb.lambda_handler()

