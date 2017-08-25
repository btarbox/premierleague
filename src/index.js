
// 1. Text strings =====================================================================================================
//    Modify these strings and messages to change the behavior of your Lambda function

var languageStrings = {
    'en': {
        'translation': {
            'WELCOME' : "Welcome to Premier League V two, ",
            'HELP'    : "Say get table, a team name or nickname, red cards, yellow cards, clean sheets or golden boot ",
            'ABOUT'   : "Premier League is the best football league in the world.",
            'STOP'    : "Okay, see you next time!"
        }
    }
    // , 'de-DE': { 'translation' : { 'TITLE'   : "Local Helfer etc." } }
};

var variedPrompts = {
    "help": [
        "Say get table, a team name, red cards, yellow cards, clean sheets or golden boot ",
        "Ask about the table, a team, cards, goals or clean sheets ",
        "Do you want to hear about a team, cards, goals, clean sheets, or the table ",
        "We can tell you about the table, red or yellow cards, goals, clean sheets or a team "
        ]
};

var data = {
    "teams" : [
        { "name":"Manchester United","gamesplayed":"2","wins": "2","losses": "0","draws": "0","goaldifference": "8","points": "6"
        },
        { "name":"Huddersfield Town","gamesplayed":"2","wins": "2","losses": "0","draws": "0","goaldifference": "4","points": "3"
        },
        { "name":"West Bromwich Albion","gamesplayed":"2","wins": "2","losses": "0","draws": "0","goaldifference": "2","points": "6"
        },
        { "name":"Watford","gamesplayed":"2","wins": "1","losses": "0","draws": "1","goaldifference": "2","points": "4"
        },
        { "name":"Liverpool","gamesplayed":"2","wins": "1","losses": "0","draws": "1","goaldifference": "1","points": "4"
        },
        { "name":"Southhampton","gamesplayed":"1","wins": "1","losses": "0","draws": "1","goaldifference": "1","points": "4"
        },
        { "name":"Manchester City","gamesplayed":"1","wins": "1","losses": "0","draws": "0","goaldifference": "2","points": "3"
        },
        { "name":"Leicester City","gamesplayed":"2","wins": "1","losses": "1","draws": "0","goaldifference": "1","points": "3"
        },
        { "name":"Tottenham Hotspurs","gamesplayed":"2","wins": "1","losses": "1","draws": "0","goaldifference": "1","points": "3"
        },
        { "name":"Everton","gamesplayed":"1","wins": "1","losses": "0","draws": "0","goaldifference": "1","points": "3"
        },
        { "name":"Arsenal","gamesplayed":"2","wins": "1","losses": "1","draws": "0","goaldifference": "0","points": "3"
        },
        { "name":"Chelsea","gamesplayed":"2","wins": "1","losses": "1","draws": "0","goaldifference": "0","points": "3"
        },
        { "name":"Burnley","gamesplayed":"2","wins": "1","losses": "1","draws": "0","goaldifference": "0","points": "3"
        },
        { "name":"Stoke City","gamesplayed":"2","wins": "1","losses": "1","draws": "0","goaldifference": "0","points": "3"
        },
        { "name":"Swansea City","gamesplayed":"2","wins": "0","losses": "1","draws": "1","goaldifference": "minus 4","points": "1"
        },
        { "name":"Bournemoth","gamesplayed":"2","wins": "0","losses": "2","draws": "0","goaldifference": "minus 3","points": "0"
        },
        { "name":"Newcastle","gamesplayed":"2","wins": "0","losses": "2","draws": "0","goaldifference": "minus 3","points": "0"
        },
        { "name":"Brighton","gamesplayed":"2","wins": "0","losses": "2","draws": "0","goaldifference": "minus 4","points": "0"
        },
        { "name":"Crystal Palace","gamesplayed":"2","wins": "0","losses": "2","draws": "0","goaldifference": "minus 4","points": "0"
        },
        { "name":"West Ham United","gamesplayed":"2","wins": "0","losses": "2","draws": "0","goaldifference": "minus 5","points": "0"
        },


        { "name":"past the end team",
            "gamesplayed":"0",
            "wins": "0",
            "losses": "0",
            "draws": "0",
            "goaldifference": "0",
            "points": "0"
        }

    ]
}


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
        var say = this.t('WELCOME') + ' ' + this.t('HELP');
        //console.log('about to call loadFileText');
        //say += ", the keepers with the most clean sheets are, "
        //loadStats(this, say, "cleansheets");
        this.emit(':ask', say, say);
    },

    'AboutIntent': function () {
        this.emit(':tell', this.t('ABOUT'));
    },

    'CleanSheetsIntent': function() {
        var say = "the defenders with the most clean sheets are, ";
        loadStats(this, say, "cleansheets", this.t('HELP'));
    },
    
    'GoldenBootIntent': function() {
        var say = "the players with the most goals are, ";
        loadStats(this, say, "goldenboot", this.t('HELP'));
    },
    
    'RedCardIntent': function() {
        var say = "the players with the most red cards are, ";
        loadStats(this, say, "redcards", this.t('HELP'));
    },
    
    'YellowCardIntent': function() {
        var say = "the players with the most yellow cards are, ";
        loadStats(this, say, "yellowcards", this.t('HELP'));
    },

    'ListTeamNamesIntent': function () {
        console.log("at top of ListTeamNamesIntent");
        var say = 'We recognize the following team names';
        say += 'Manchester United, Huddersfield Town, Manchester City, Tottenham Hotspurs, Arsenel, Burnley, Everton, West Bromwich Albion, ';
        say += 'Liverpool, Watford, Southhampton, Swansea City, Leicester City, Chelsea, Bournemouth, Stoke City, Brighton, Newcastle, Crystal Palace and West Ham';
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
        console.log('table index is ' + this.attributes['tableIndex'])
        this.emit(':ask', say);
    },

    'TeamIntent': function () {
        try {
        console.log('at TeamIntent');
        //console.log('this.event ' + this.event);
        //console.log('this.event.request ' + this.event.request);
        //console.log('this.event.request.intent ' + this.event.request.intent);
        //console.log('this.event.request.intent.slots ' + JSON.stringify(this.event.request.intent.slots));
        //console.log('this.event.request.intent.slots ' + JSON.stringify(this.event.request.intent.slots.plteam));
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
        console.log('there were ' + numMatches + ' matches for name ' + this.event.request.intent.slots.plteam.value)
        var cannonicalTeam = this.event.request.intent.slots.plteam.resolutions.resolutionsPerAuthority[0].values[0].value.id;
        console.log('canonical team name ' + cannonicalTeam);
        team = this.event.request.intent.slots.plteam.value;
        var say = 'You asked about ' + cannonicalTeam ;
        
        teamIndex = findTeamIndex(data, cannonicalTeam)
        if(teamIndex == -1) {
            console.log('team not found');
            var say = 'Alexa heard ' + team + ', we did not find them, please say the full team name such as Manchester City.';
            say += ', , , do you want to list the table, ask about a team or stop?'
            this.emit(':ask', say);
        } else {
        // say += ' their index is ' + teamIndex + ' '
        say += ', their form is ' 
           + pluralize(data.teams[teamIndex].wins,  'win', 's')    + ', '
           + pluralize(data.teams[teamIndex].draws, 'draw', 's')   + ', '
           + pluralize(data.teams[teamIndex].losses, 'loss', 'es') + ', '
           + ' and a goal differential of '
           + data.teams[teamIndex].goaldifference
           + 'and ' + pluralize(data.teams[teamIndex].points, 'point', 's')  // ' + data.teams[teamIndex].points + ' points'
           
        say += ',' + randomPrompt();
        this.emit(':ask', say);
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
          var say2 = 'The last five teams in the table are ' + buildTableFragment(tableIndex) + '. do you want to list the table, ask about a team or stop?';
          this.emit(':ask', say2);
        }

    },

    'AMAZON.NoIntent': function () {
        // this.emit('AMAZON.StopIntent');
        this.emit(':ask', 'do you want to list the table, ask about a team or stop?')
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

function loadStats(emmiter, say, filename, reprompt) {
    const bucket = "bpltables";
    const fileParams = {
        Bucket: bucket,
        Key: filename
    };
    console.log('try to open file ' + bucket + ":" + filename);
    s3.getObject(fileParams, function(err, data) {
        if (err) {
            console.log("did not find file " + filename + " because:" + err);
            say += " unable to open file " + filename
            emmiter.emit(':ask', say, say);
        } else {
            console.log("found file " + filename);
            var body = data.Body.toString('ascii');
            //console.log("body is " + body);
            var n = body.split("\n");

            oneCard = n[0].split(',')
            ///console.log( oneCard[1] + " with " + oneCard[2] +  " has " + oneCard[4] + " cards")
            
            for(var index = 0; index < 5; index++) {
                /// console.log("process line " + index + " which is " + n[index])
                oneCard = n[index].split(',')
                // console.log( oneCard[1] + " with " + oneCard[2] +  " has " + oneCard[4] + " cards")
                say += ", " + oneCard[1] + " with " + oneCard[2] +  " has " + oneCard[4];
            }
            
            say += ". ," + randomPrompt(); //reprompt;
            emmiter.emit(':ask', say, say);
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
    return variedPrompts.help[Math.floor(Math.random() * (high - low + 1) + low)]
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

