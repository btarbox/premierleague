
var languageStrings = {
    'en': {
        'translation': {
            'WELCOME' : "Welcome to Premier League 2.4, ",
            'HELP'    : "Say get table, a team name or nickname, red cards, yellow cards, clean sheets, golden boot, fixtures, results or relegation ",
            'ABOUT'   : "Premier League is the best football league in the world.",
            'STOP'    : "Okay, see you next time!"
        }
    }
    // , 'de-DE': { 'translation' : { 'TITLE'   : "Local Helfer etc." } }
};

var extraCmdPrompts = new Map();
extraCmdPrompts.set("redcards", ". you can also say red cards");
extraCmdPrompts.set("yellowcards", ". you can also say yellow card");
extraCmdPrompts.set("cleansheets", ".  you can also ask about clean sheets");
extraCmdPrompts.set("goals", ". you can also ask about goals");
extraCmdPrompts.set("relegation", ". you can also ask about relegation");
extraCmdPrompts.set("fixtures", ". you can also ask about fixtures");
extraCmdPrompts.set("results", ". you can also ask about last weeks results");
extraCmdPrompts.set("referees", ". you can also ask about referees");

var variedPrompts = {
    "help": [
        "Say get table, or say a team name ",
        "Ask about the table, or a team ",
        "Say a command ",
        "We can tell you about teams or the table "
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
        var say = this.t('WELCOME') + ' Say get table, or say a team name ';
        invocation_count = this.attributes['invocation_count'];
        if (typeof invocation_count == "undefined") {
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
        }

        loadMainTable(this, say, "liveMainTable", this.t('HELP'));
    },

    'AboutIntent': function () {
        this.emit(':tell', this.t('ABOUT'));
    },

    'CleanSheetsIntent': function() {
        updateStats(this, 'cleansheets');//extraCmdPrompts.delete('cleansheets')
        var say = "the defenders with the most clean sheets are, ";
        loadStats(this, say, 5, "cleansheets", ", with ", " has ", "  ", 1, 2, 4, this.t('HELP'));
    },
    
    'GoldenBootIntent': function() {
        updateStats(this, 'goals');//extraCmdPrompts.delete('goals')
        var say = "the players with the most goals are, ";
        loadStats(this, say, 5, "goldenboot", ", with ", " has ", "  ", 1, 2, 4, this.t('HELP'));
    },
    
    'RedCardIntent': function() {
        updateStats(this, 'redcards');//extraCmdPrompts.delete('redcards');
        var say = "the players with the most red cards are, ";
        loadStats(this, say, 5, "redcards", ", with ", " has ", "  ", 1, 2, 4, this.t('HELP'));
    }, 
    
    'YellowCardIntent': function() {
        updateStats(this, 'yellowcards');//extraCmdPrompts.delete('yellowcards');
        var say = "the players with the most yellow cards are, ";
        loadStats(this, say, 5, "yellowcards", ", with ", " has ", "  ", 1, 2, 4, this.t('HELP'));
    },

    'RelegationIntent': function() {
        updateStats(this, 'relegation');//extraCmdPrompts.delete('relegation');
        var say = "the teams currently in the relegation zone are, ";
        loadStats(this, say, 3, "relegation", "", " has ", "  ", 1, 2, 4, this.t('HELP'));
    },

    'FixturesIntent': function() {
        extraCmdPrompts.delete('fixtures');
        var say = "the fixtures for the current / upcoming match week are, ";
        loadStats(this, say, 10, "fixtures2", " versus ", " at ", "  ", 0, 2, 3, this.t('HELP'));
    },

    'ResultsIntent': function() {
        extraCmdPrompts.delete('results');
        var say = "the results for the last match week were, ";
        loadStats(this, say, 10, "prevWeekFixtures", "  ", "  ", "  ", 0, 1, 2, this.t('HELP'));
    },

    'RefereesIntent': function() {
        extraCmdPrompts.delete('referees');
        var say = "the most used referees were, ";
        loadStats(this, say, 5, "referees", " ", " yellow cards and ", " red cards", 0, 3, 2, this.t('HELP'));
    },
    
    'StadiumIntent': function() {
        extraCmdPrompts.delete('stadium');
        var say = "You asked about a stadium, ";
        //readFile(this, say, "stadiums/Etihad");
        try {
            if(this.event.request.intent.slots.stadiumType.hasOwnProperty('resolutions')) {
                console.log('we got a resolution');
            } else {
                console.log('we did not get a resolution');
            }
            var cannonicalStadium = this.event.request.intent.slots.stadiumType.resolutions.resolutionsPerAuthority[0].values[0].value.id;
            console.log("heard stadium " + cannonicalStadium);
            readFile(this, say, ("stadiums/" + cannonicalStadium));
        }catch(err){
            console.log('sorry, we had a problem recognizing your stadium ' + err);
            say = 'sorry, we had a problem recognizing your stadium, do you want to list the table, ask about a team or stop? ';
            this.emit(':ask', say);
        }
    },


    'ListTeamNamesIntent': function () {
        console.log("at top of ListTeamNamesIntent");
        var say = 'We recognize the following team names';
        say += 'Manchester United, Huddersfield Town, Manchester City, Tottenham Hotspurs, Arsenel, Burnley, Everton, West Bromwich Albion, ';
        say += 'Liverpool, Watford, Southhampton, Swansea City, Leicester City, Chelsea, Bournemouth, Stoke City, Brighton, Newcastle, Crystal Palace and West Ham.';
        say += 'You can also say gunners, potters, cherries, the blues, foxes, hammers, magpies, swans, saints, hornets, the reds, toffees, clarets, terries, citizens';
        say += ',' + randomPrompt()
        this.emit(':ask', say);
    },

    'TableIntent': function () {
        console.log("at top of TableIntent")
        this.attributes['activity'] = 'list table';
        this.attributes['tableIndex'] = 0;
        tableIndex = 0

        var say = 'The next five teams in the table are ' + buildTableFragment(tableIndex) + '. Would you like to hear more?';
        this.attributes['tableIndex'] = tableIndex + 5;
        console.log('table index is ' + this.attributes['tableIndex']);
        this.emit(':ask', say);
    },

    'TeamIntent': function () {
        try {
        console.log('at TeamIntent');
        if(this.event.request.intent.slots.plteam.hasOwnProperty('resolutions')) {
            console.log('we got a resolution');
        } else {
            console.log('we did not get a resolution');
        }
        console.log('confirmationStatus:' + this.event.request.intent.slots.plteam.confirmationStatus);
        var numMatches = this.event.request.intent.slots.plteam.resolutions.resolutionsPerAuthority[0].values.length;
        console.log('there were ' + numMatches + ' matches for name ' + this.event.request.intent.slots.plteam.value);
        var cannonicalTeam = this.event.request.intent.slots.plteam.resolutions.resolutionsPerAuthority[0].values[0].value.id;
        console.log('canonical team name ' + cannonicalTeam);
        team = this.event.request.intent.slots.plteam.value;
        var say = 'You asked about ' + cannonicalTeam ;
        
        teamIndex = findTeamIndex(data, cannonicalTeam);
        if(teamIndex == -1) {
            console.log('team not found');
            var say = 'Alexa heard ' + team + ', we did not find them, please say the full team name such as Manchester City.';
            say += ', , , do you want to list the table, ask about a team or stop?';
            this.emit(':ask', say);
        } else {
        // say += ' their index is ' + teamIndex + ' '
        var form = pluralize(data.teams[teamIndex].wins,  'win', 's')    + ', '
           + pluralize(data.teams[teamIndex].draws, 'draw', 's')   + ', '
           + pluralize(data.teams[teamIndex].losses, 'loss', 'es') + ', '
           + pluralize(data.teams[teamIndex].goalsfor, 'goal', 's') + ' scored, '
           + pluralize(data.teams[teamIndex].goalsagainst, 'goal', 's') + ' allowed, '
           + ' for a goal differential of '
           + data.teams[teamIndex].goaldifference
           + ', and ' + pluralize(data.teams[teamIndex].points, 'point', 's')
        say += ', their form is ' + form

        say += "<break time='1s'/>" + "say a team name or other command";
        var card = cannonicalTeam + "'s form is:" + form;
        this.emit(':askWithCard', say, "say a team name or other command", cannonicalTeam, card);
        }
        }
        catch(err) {
            console.log('sorry, we had a problem recognizing your team ' + err);
            say = 'sorry, we had a problem recognizing your team, try saying their full name, ' + 'do you want to list the table, ask about a team or stop?  You can also say list team names'
            this.emit(':ask', say);
        }
    },

    'AMAZON.YesIntent': function () {
        tableIndex =  this.attributes['tableIndex'];
        console.log('at the yes intent, tableIndex is ' + tableIndex);
        this.attributes['tableIndex'] += 5;
        if(tableIndex < 15) {
          var say = 'The next five teams in the table are ' + buildTableFragment(tableIndex) + '. Would you like to hear more?';
          this.emit(':ask', say);
        } else {
          var say2 = 'The last five teams in the table are ' + buildTableFragment(tableIndex) + '.' + randomPrompt();
          this.emit(':ask', say2);
        }

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
        this.emit(':tell', this.t('STOP'));
    },
    'SessionEndedRequest': function () {
        this.emit(':tell', this.t('STOP'));
    },    
    
    'AMAZON.StopIntent': function () {
        if(interruptable) {
            interruptable = false;
            this.emit(':ask', "say stop to exit Premier League or say another command");
        } else {
            this.emit(':tell', this.t('STOP') + maybeAskForReview(this));
        }
    }
};

//    END of Intent Handlers {} ========================================================================================

function maybeAskForReview(main) {
    var askForReview = "";
    if(question_count > 10) {
        var haveAskedForReview = main.attributes['haveAskedForReview'];
        if (typeof haveAskedForReview == "undefined") {
            main.attributes['haveAskedForReview'] = true;
            askForReview = ', and if you would like to write us a review, <prosody pitch="x-high"> that would be great</prosody>'
        }
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
                //var newText = oneCard[firstCol] + article1 + oneCard[secondCol] +  article2 + oneCard[thirdCol];
                var newText = getOneLine(oneCard[firstCol], article1, oneCard[secondCol], article2, oneCard[thirdCol], article3);
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
    return variedPrompts.help[Math.floor(Math.random() * (high - low + 1) + low)] + suggest()
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

function findTeamIndex(data, teamName) {
  console.log('trying to find team ' + teamName)
  for (var i = 0; i < 20; i++) {
      console.log('compare ' + data.teams[i].name.toUpperCase().replace(/ /g,'') + ' with ' + teamName.toUpperCase() + '.')
      if(data.teams[i].name.toUpperCase().replace(/ /g,'') == teamName.toUpperCase()) {
          console.log('found team at index ' + i);
          return i;
      }
  }    
  console.log('did not find team');
  return -1;
}

function buildTableFragment(tableIndex) {
    console.log('build next 5 teams starting from ' + tableIndex)

    tableFragment = '';
    for (var i = tableIndex; i < (tableIndex + 5); i++) {
        tableFragment = tableFragment + sayPlace(i+1) + data.teams[i].name + ' with ' + pluralize(data.teams[i].points, 'point', 's') + ', ';
        console.log('index is now ' + i + 'fragment is ' + tableFragment);
    }
    tableIndex += 5
    return tableFragment
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

function loadMainTable(emmiter, say, filename, reprompt) {
    const bucket = "bpltables";
    const fileParams = {
        Bucket: bucket,
        Key: filename
    };
    console.log('try to open file ' + bucket + ":" + filename);
    s3.getObject(fileParams, function(err, filedata) {
        if (err) {
            console.log("did not find file " + filename + " because:" + err);
            say += " unable to open file " + filename
            emmiter.emit(':ask', say, say);
        } else {
            console.log("found file " + filename);
            var body = filedata.Body.toString('ascii');
            var n = body.split("\n");

            for(var teamIndex = 0; teamIndex < 20; teamIndex++) {
                oneTeam = n[teamIndex].split(',')
    
                datastring = '{ "name":"'    + oneTeam[0] + 
                     '", "games played":"'   + oneTeam[1] + 
                     '", "wins":"'           + oneTeam[2] + 
                     '", "draws":"'          + oneTeam[3] + 
                     '", "losses":"'         + oneTeam[4] + 
                     '", "goalsfor":"'       + oneTeam[5] + 
                     '", "goalsagainst":"'   + oneTeam[6] + 
                     '", "goaldifference":"' + oneTeam[7] + 
                     '", "points":"'         + oneTeam[8] + 
                     '"}';
                
                data.teams[teamIndex] = JSON.parse(datastring);
            }
            
        emmiter.emit(':ask', say, say);
        }
    });
}

