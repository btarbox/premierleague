
// 1. Text strings =====================================================================================================
//    Modify these strings and messages to change the behavior of your Lambda function

var languageStrings = {
    'en': {
        'translation': {
            'WELCOME' : "Welcome to Premier League 2.3, ",
            'HELP'    : "Say get table, a team name or nickname, red cards, yellow cards, clean sheets or golden boot ",
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

var variedPrompts = {
    "help": [
        "Say get table, or say a team name ",
        "Ask about the table, or a team ",
        "Say a command ",
        "We can tell you about teams or the table "
        ]
};

var data = {
    "teams" : Array(20)
};


// 2. Skill Code =======================================================================================================

var Alexa = require('alexa-sdk');
const aws = require('aws-sdk');

var s3 = new aws.S3({ apiVersion: '2006-03-01' });

exports.handler = function(event, context, callback) {
    var alexa = Alexa.handler(event, context);

    // alexa.appId = 'amzn1.echo-sdk-ams.app.1234';
    ///alexa.dynamoDBTableName = 'YourTableName'; // creates new table for session.attributes
    alexa.resources = languageStrings;
    alexa.registerHandlers(handlers);
    alexa.execute();
};

var handlers = {
    'LaunchRequest': function () {
        var say = this.t('WELCOME') + ' Say get table, or say a team name ';

        loadMainTable(this, say, "liveMainTable", this.t('HELP'));
    },

    'AboutIntent': function () {
        this.emit(':tell', this.t('ABOUT'));
    },

    'CleanSheetsIntent': function() {
        extraCmdPrompts.delete('cleansheets')
        var say = "the defenders with the most clean sheets are, ";
        loadStats(this, say, 5, "cleansheets", ", with ", " has ", 1, 2, 4, this.t('HELP'));
    },
    
    'GoldenBootIntent': function() {
        extraCmdPrompts.delete('goals')
        var say = "the players with the most goals are, ";
        loadStats(this, say, 5, "goldenboot", ", with ", " has ", 1, 2, 4, this.t('HELP'));
    },
    
    'RedCardIntent': function() {
        extraCmdPrompts.delete('redcards')
        var say = "the players with the most red cards are, ";
        loadStats(this, say, 5, "redcards", ", with ", " has ", 1, 2, 4, this.t('HELP'));
    },
    
    'YellowCardIntent': function() {
        extraCmdPrompts.delete('yellowcards')
        var say = "the players with the most yellow cards are, ";
        loadStats(this, say, 5, "yellowcards", ", with ", " has ", 1, 2, 4, this.t('HELP'));
    },

    'RelegationIntent': function() {
        extraCmdPrompts.delete('relegation')
        var say = "the teams currently in the relegation zone are, ";
        loadStats(this, say, 3, "relegation", "", " has ", 1, 2, 4, this.t('HELP'));
    },

    'FixturesIntent': function() {
        extraCmdPrompts.delete('fixtures')
        var say = "the fixtures for the next match week are, ";
        loadStats(this, say, 10, "fixtures", " versus ", " at ", 0, 2, 3, this.t('HELP'));
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
            //console.log('listening for team name ' + JSON.stringify(this.event.request.intent.slots.plteam.resolutions.resolutionsPerAuthority));
            //console.log('listening for team name ' + JSON.stringify(this.event.request.intent.slots.plteam.resolutions.resolutionsPerAuthority[0].values));
            //console.log('listening for team name ' + JSON.stringify(this.event.request.intent.slots.plteam.resolutions.resolutionsPerAuthority[0].values[0].value));
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
        // this.emit('AMAZON.StopIntent');
        this.emit(':ask', randomPrompt())
    },
    
    'AMAZON.HelpIntent': function () {
        this.emit(':ask', this.t('HELP'));
    },
    'AMAZON.CancelIntent': function () {
        this.emit(':tell', this.t('STOP'));
    },
    'AMAZON.StopIntent': function () {
        this.emit(':tell', this.t('STOP'));
    }

};

//    END of Intent Handlers {} ========================================================================================

// 3. Helper Function  =================================================================================================

function loadStats(emmiter, say, number, filename, article1, article2, firstCol, secondCol, thirdCol, reprompt) {
    const bucket = "bpltables";
    const fileParams = {
        Bucket: bucket,
        Key: filename
    };
    //var cardTitle = say;
    var cardText = "";
    
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
                var newText = oneCard[firstCol] + article1 + oneCard[secondCol] +  article2 + oneCard[thirdCol];
                say += ", " + newText;
                cardText += newText + '\n';
            }
            
            say += "<break time='1s'/>" + randomPrompt(); //reprompt;
            console.log("about to say " + say);
            console.log("card would be " + filename + ";" + cardText)
            //emmiter.emit(':ask', say, say);
            emmiter.emit(':askWithCard', say, randomPrompt(), filename, cardText)
        }
    });
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

