
var languageStrings = {
    'en': {
        'translation': {
            'WELCOME' : "Welcome to Champions League, say get Group and a group letter ",
            'HELP'    : "Say get group and a group letter, such as get group b or get group c, you can also ask who are the leaders ",
            'ABOUT'   : "Champions League is the best football league in the world.",
            'STOP'    : "Okay, see you next time!"
        }
    }
    // , 'de-DE': { 'translation' : { 'TITLE'   : "Local Helfer etc." } }
};

/*var extraCmdPrompts = new Map();
// extraCmdPrompts.set("injuries", ". you can also ask about injuries");
extraCmdPrompts.set("touches", ". you can also ask about touches");
extraCmdPrompts.set("fouls", ". you can also ask about fouls");
extraCmdPrompts.set("tackles", ". you can also ask about tackles");
extraCmdPrompts.set("stadiums", ". you can also ask about Premier League stadiums by name");
extraCmdPrompts.set("referees", ". you can also ask about referees");
extraCmdPrompts.set("fixtures", ". you can also ask about fixtures");
extraCmdPrompts.set("results", ". you can also ask about last weeks results");
extraCmdPrompts.set("relegation", ". you can also ask about relegation");
extraCmdPrompts.set("redcards", ". you can also say red cards");
extraCmdPrompts.set("yellowcards", ". you can also say yellow card");
extraCmdPrompts.set("cleansheets", ".  you can also ask about clean sheets");
extraCmdPrompts.set("goals", ". you can also ask about goals");
*/

var variedPrompts = {
    "help": [
        "Say get group and a group letter or say get leaders ",
        "Ask about the table for a group or say get leaders",
        "Ask who are the leaders or ask about a group ",
        "We can tell you about the table for a group or say get leaders"
        ]
};
var invocation_count = 0;
var question_count = 0;

var data = {
    "teams" : Array(20)
};

var interruptable = false;

var Alexa = require('alexa-sdk');
const aws = require('aws-sdk');

var s3 = new aws.S3({ apiVersion: '2006-03-01' });

exports.handler = function(event, context, callback) {
    var alexa = Alexa.handler(event, context);

    // alexa.appId = 'amzn1.echo-sdk-ams.app.1234';
    alexa.dynamoDBTableName = 'PremierLeagueSkill'; // creates new table for session.attributes
    alexa.resources = languageStrings;
    console.log("got here");
    alexa.registerHandlers(handlers);
    console.log("and got here");
    alexa.execute();
};

var handlers = {
    'LaunchRequest': function () {
        console.log('at top of LaunchRequest');
        var say = this.t('WELCOME');
       // invocation_count = this.attributes['invocation_count'];
    /*    if (typeof invocation_count == "undefined") {
            console.log('invocation_count was not found in dynamo, initializing it to 1');
            this.attributes['invocation_count'] = 1;
            invocation_count = 1;
            this.attributes['question_count'] = 1;
            question_count = 1;
        } else {
            invocation_count += 1;
            this.attributes['invocation_count'] = invocation_count;
            
            question_count = this.attributes['question_count']
            if (typeof question_count == "undefined") {
                question_count = 1;
            } else {
                question_count += 1;
            }
            this.attributes['question_count'] = question_count;
            console.log("invocation_count incremented to " + invocation_count + ", question_count " + question_count);
        }*/

        // loadMainTable(this, say, "liveMainTable", this.t('HELP'));
        console.log("at end of launch request")
        this.emit(':ask', say, say);

    },

    'LeadersIntent': function() {
        var say = "the champions league leaders are:, ";
        loadStats(this, say, 8, "groupLeaders", " leads ", " ", " ", 0, 1, -1, this.t('HELP'));
    },

    'GroupIntent': function() {
        try {
        console.log('at TeamIntent');
        if(this.event.request.intent.slots.groupslot.hasOwnProperty('resolutions')) {
            console.log('we got a resolution');
        } else {
            console.log('we did not get a resolution');
        }
        console.log('bla:' + this.event.request.intent.slots.groupslot);
        
        console.log('confirmationStatus:' + this.event.request.intent.slots.groupslot.confirmationStatus);
        var numMatches = this.event.request.intent.slots.groupslot.resolutions.resolutionsPerAuthority[0].values.length;
        console.log('there were ' + numMatches + ' matches for name ' + this.event.request.intent.slots.groupslot.value);
        console.log("cannonical group name is " + this.event.request.intent.slots.groupslot.resolutions.resolutionsPerAuthority[0].values[0].value.id);
        
        } catch(err) {
            console.log('sorry, we had a problem recognizing your group ' + err);
            say = 'sorry, we had a problem recognizing your group, say something like group a or group b '
            this.emit(':ask', say);
        }


        // extraCmdPrompts.delete('fixtures');
        var say = "the table for this group is:, ";
        loadStats(this, say, 4, this.event.request.intent.slots.groupslot.resolutions.resolutionsPerAuthority[0].values[0].value.id.toLowerCase(), " has a goal difference of ", " and ", " points ", 0, 4, 5, this.t('HELP'));
    },

    'AboutIntent': function () {
        this.emit(':tell', this.t('ABOUT'));
    },

    
    'AMAZON.NoIntent': function () {
        this.emit(':ask', randomPrompt())
    },
    
    'AMAZON.HelpIntent': function () {
        this.emit(':ask', this.t('HELP'));
    },
    
    'AMAZON.CancelIntent': function () {
        this.emit(':tell', this.t('STOP'));
    },
    
    'AMAZON.ExitIntent': function () {
        this.emit(':tell', this.t('STOP'));
    },
    'Unhandled': function () {
        console.log("at the unhandled intent")
        this.emit(':tell', this.t('STOP'));
    },
    'SessionEndedRequest': function () {
        this.emit(':tell', this.t('STOP'));
    },    
    
    'AMAZON.StopIntent': function () {
        if(interruptable) {
            interruptable = false;
            this.emit(':ask', "say stop to exit Champions League or say another command");
        } else {
            this.emit(':tell', this.t('STOP') + maybeAskForReview(this));
        }
    }
};

//    END of Intent Handlers {} ========================================================================================

function maybeAskForReview(main) {
    var askForReview = "";
    var low = 1;
    var high = 9;
    var thisRandInt = Math.floor(Math.random() * (high - low + 1) + low)
    console.log('thisRandInt is ' + thisRandInt);
    if(thisRandInt == 3) {
       // var haveAskedForReview = main.attributes['haveAskedForReview'];
       //if (typeof haveAskedForReview == "undefined") {
       //     main.attributes['haveAskedForReview'] = true;
       askForReview = ', and if you would like to write us a review, <prosody pitch="x-high"> that would be great</prosody>'
       //  }
    }
    if(thisRandInt == 4) {
       askForReview = ', and you might want to try our other skill called Premier League' 
    }
    return askForReview;
}

function updateStats(main, extraPrompt) {
    if(extraPrompt.length > 0) {
        extraCmdPrompts.delete(extraPrompt);
    }    
    question_count += 1;
    main.attributes['question_count'] = question_count;
}

// read the entire contents of a file
function readFile(emmiter, say, filename) {
    const bucket = "bpltables";
    const fileParams = {
        Bucket: bucket,
        Key: filename
    };
    var cardText = "";
    interruptable = true;
    
    console.log('try to open file ' + bucket + ":" + filename);
    s3.getObject(fileParams, function(err, data) {
        if (err) {
            console.log("did not find file " + filename + " because:" + err);
            say += " unable to open file " + filename
            emmiter.emit(':ask', say, say);
        } else {
            console.log("found file " + filename);
            var body = data.Body.toString('ascii');
            say += body;
            
            say += "<break time='1s'/>" + randomPrompt(); //reprompt;
            console.log("about to say " + say);
            console.log("card would be " + filename + ";" + cardText)
            //emmiter.emit(':ask', say, say);
            emmiter.emit(':askWithCard', say, randomPrompt(), filename, cardText)
            interruptable = false;
        }
    });
}

function loadStats(emmiter, say, number, filename, article1, article2, article3, firstCol, secondCol, thirdCol, reprompt) {
    const bucket = "bpltables";
    const fileParams = {
        Bucket: bucket,
        Key: filename
    };
    //var cardTitle = say;
    var cardText = "";
    interruptable = true;
    
    console.log('try to open file ' + bucket + ":" + filename);
    s3.getObject(fileParams, function(err, data) {
        if (err) {
            console.log("did not find file " + filename + " because:" + err);
            say += " unable to open file " + filename
            emmiter.emit(':ask', say, say);
        } else {
            console.log("found file " + filename);
            var body = data.Body.toString('ascii');
            var n = body.split("\n");

            oneCard = n[0].split(',')
            
            for(var index = 0; index < number; index++) {
                oneCard = n[index].split(',')
                var third = thirdCol > -1 ? oneCard[thirdCol] : "";
                var newText = getOneLine(oneCard[firstCol], article1, oneCard[secondCol], article2, third, article3);
                say += ", " + newText;
                cardText += newText + '\n';
            }
            
            say += "<break time='1s'/>" + randomPrompt(); //reprompt;
            console.log("about to say " + say);
            console.log("card would be " + filename + ";" + cardText)
            //emmiter.emit(':ask', say, say);
            emmiter.emit(':askWithCard', say, randomPrompt(), filename, cardText)
            interruptable = false;
        }
    });
}

function getOneLine(noun1, article1, noun2, article2, noun3, article3) {
    console.log("at getOneFixture:" + noun1 + article1 + noun2 + article2 + noun3 + article3);
    var foundNumber = noun1.search('[0-9]');
    var foundNil = noun1.search('nil');
    // console.log(noun1 + " has a score " + foundNumber);
    if(foundNumber != -1 || foundNil != -1) {
        return noun1 + "<break time='350ms'/>" + noun2;
    } else {
        return noun1 + article1 + noun2 + article2 + noun3 + article3 + ",";
    }
}

function pluralize(count, noun, ess) {
    if(parseInt(count) == 1) {
        return count + " " + noun;
    } else {
        return count + " " + noun + ess;
    }
}

function randomPrompt() {
    var low = 0;
    var high = 3;
    return variedPrompts.help[Math.floor(Math.random() * (high - low + 1) + low)] //+ suggest()
}

// This command lets us suggest commands to the user that they have not yet used
function suggest() {
    var suggestionsLeft = extraCmdPrompts.size;
    console.log("num suggestions left:" + suggestionsLeft)
    if(parseInt(suggestionsLeft) > 0) {
        var firstKey = Array.from(extraCmdPrompts.keys())[0];
        var firstValue = extraCmdPrompts.get(firstKey);
        extraCmdPrompts.delete(firstKey);
        return firstValue;
    }
    return ''
}


function sayPlace(tableIndex) {
    if(tableIndex == 1)
       return "first place "
       else if (tableIndex == 2)
       return "second place "
       else if(tableIndex == 3)
       return "third place"
       else 
       return tableIndex + "th place"
}
