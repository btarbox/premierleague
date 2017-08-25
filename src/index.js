
var languageStrings = {
    'en': {
        'translation': {
            'WELCOME' : "Welcome to Premier League",
            'HELP'    : "Say get table or get team. ",
            'ABOUT'   : "Premier League is the best football league in the world.",
            'STOP'    : "Okay, see you next time!"
        }
    }
    // , 'de-DE': { 'translation' : { 'TITLE'   : "Local Helfer etc." } }
};
var data = {
    "teams" : [
        { "name":"Huddersfield Town","gamesplayed":"1","wins": "1","losses": "0","draws": "0","goaldifference": "3","points": "3"
        },
        { "name":"Arsenal","gamesplayed":"1","wins": "1","losses": "0","draws": "0","goaldifference": "1","points": "3"
        },
        { "name":"Burnley FC","gamesplayed":"1","wins": "1","losses": "0","draws": "0","goaldifference": "1","points": "3"
        },
        { "name":"Everton","gamesplayed":"1","wins": "1","losses": "0","draws": "0","goaldifference": "1","points": "3"
        },
        { "name":"West Bromwich Albion","gamesplayed":"1","wins": "1","losses": "0","draws": "0","goaldifference": "1","points": "3"
        },
        { "name":"Liverpool","gamesplayed":"1","wins": "0","losses": "0","draws": "1","goaldifference": "0","points": "1"
        },
        { "name":"Watford","gamesplayed":"1","wins": "0","losses": "0","draws": "1","goaldifference": "0","points": "1"
        },
        { "name":"Southhampton","gamesplayed":"1","wins": "0","losses": "0","draws": "1","goaldifference": "0","points": "1"
        },
        { "name":"Swansea City","gamesplayed":"1","wins": "0","losses": "0","draws": "0","goaldifference": "0","points": "1"
        },
        { "name":"Brighton","gamesplayed":"0","wins": "0","losses": "0","draws": "0","goaldifference": "0","points": "0"
        },
        { "name":"Manchester City","gamesplayed":"0","wins": "0","losses": "0","draws": "0","goaldifference": "0","points": "0"
        },
        { "name":"Manchester United","gamesplayed":"0","wins": "0","losses": "0","draws": "0","goaldifference": "0","points": "0"
        },
        { "name":"Newcastle","gamesplayed":"0","wins": "0","losses": "0","draws": "0","goaldifference": "0","points": "0"
        },
        { "name":"Tottenham Hotspurs","gamesplayed":"0","wins": "0","losses": "0","draws": "0","goaldifference": "0","points": "0"
        },
        { "name":"West Ham United","gamesplayed":"0","wins": "0","losses": "0","draws": "0","goaldifference": "0","points": "0"
        },
        { "name":"Leicester City","gamesplayed":"1","wins": "0","losses": "1","draws": "0","goaldifference": "-1","points": "0"
        },
        { "name":"Chelsea","gamesplayed":"1","wins": "0","losses": "1","draws": "0","goaldifference": "-1","points": "0"
        },
        { "name":"Bournemouth","gamesplayed":"1","wins": "0","losses": "1","draws": "0","goaldifference": "-1","points": "0"
        },
        { "name":"Stoke City","gamesplayed":"1","wins": "0","losses": "1","draws": "0","goaldifference": "-1","points": "0"
        },
        { "name":"Crystal Palace","gamesplayed":"1","wins": "0","losses": "1","draws": "0","goaldifference": "3","points": "0"
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
        this.emit(':ask', say, say);
    },

    'AboutIntent': function () {
        this.emit(':tell', this.t('ABOUT'));
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
        console.log('at TeamIntent');
        console.log('this.event ' + this.event);
        console.log('this.event.request ' + this.event.request);
        console.log('this.event.request.intent ' + this.event.request.intent);
        console.log('this.event.request.intent.slots ' + this.event.request.intent.slots);
        console.log('this.event.request.intent.slots ' + JSON.stringify(this.event.request.intent.slots));
        console.log('listening for team name ' + JSON.stringify(this.event.request.intent.slots.plteam.resolutions.resolutionsPerAuthority));
        console.log('listening for team name ' + JSON.stringify(this.event.request.intent.slots.plteam.resolutions.resolutionsPerAuthority[0].values));
        console.log('listening for team name ' + JSON.stringify(this.event.request.intent.slots.plteam.resolutions.resolutionsPerAuthority[0].values[0].value));
        console.log('canonical team name ' + this.event.request.intent.slots.plteam.resolutions.resolutionsPerAuthority[0].values[0].value.id);
        team = this.event.request.intent.slots.plteam.value;
        var say = 'You asked about ' + team + ' which has slotIndex ' + this.event.request.intent.slots.plteam.resolutions.resolutionsPerAuthority;
        
        teamIndex = findTeamIndex(data, team)
        if(teamIndex == -1) {
            console.log('team not found');
            var say = 'We did not find your team, please say the full team name such as Manchester City.  We will add alternate names in the upcoming release.';
            say += ', , , do you want to list the table, ask about a team or stop?'
            this.emit(':ask', say);
        } else {
        // say += ' their index is ' + teamIndex + ' '
        say += ', their form is ' 
           + data.teams[teamIndex].wins + ' wins, ' 
           + data.teams[teamIndex].losses + ' losses and,' 
           + data.teams[teamIndex].draws + ' draws,'
           + ' a goal differential of '
           + data.teams[teamIndex].goaldifference
           + 'and ' + data.teams[teamIndex].points + ' points'
           
        say += ', , , do you want to list the table, ask about a team or stop?'
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

function findTeamIndex(data, teamName) {
  console.log('trying to find team ' + teamName)
  for (var i = 0; i < 20; i++) {
      console.log('compare ' + data.teams[i].name.toUpperCase() + ' with ' + teamName.toUpperCase() + '.')
      if(data.teams[i].name.toUpperCase() == teamName.toUpperCase()) {
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
        tableFragment = tableFragment + sayPlace(i+1) + data.teams[i].name + ' with ' + data.teams[i].points +' points, ';
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

