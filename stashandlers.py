import shared
from shared import extra_cmd_prompts
import logging
import random
from random import randrange

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

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
    extra_cmd_prompts["teamresults"]  = ". you can also say, how has my team done recently"

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


