
// 1. Text strings =====================================================================================================
//    Modify these strings and messages to change the behavior of your Lambda function

var languageStrings = {
    'en': {
        'translation': {
            'WELCOME' : "Welcome to Premier League, version two",
            'HELP'    : "Say get table or get team. ",
            'ABOUT'   : "Premier League is the best football league in the world.",
            'STOP'    : "Okay, see you next time!"
        }
    }
    // , 'de-DE': { 'translation' : { 'TITLE'   : "Local Helfer etc." } }
};

var https = require('https');
var $ = require('cheerio')
var myRequest = 'tables';

var data = {
    "teams" : [
        { "name":"Manchester United","gamesplayed":"1","wins": "1","losses": "0","draws": "0","goaldifference": "4","points": "3"
        },
        { "name":"Huddersfield Town","gamesplayed":"1","wins": "1","losses": "0","draws": "0","goaldifference": "3","points": "3"
        },
        { "name":"Manchester City","gamesplayed":"1","wins": "1","losses": "0","draws": "0","goaldifference": "2","points": "3"
        },
        { "name":"Tottenham Hotspurs","gamesplayed":"1","wins": "1","losses": "0","draws": "0","goaldifference": "2","points": "3"
        },
        { "name":"Arsenal","gamesplayed":"1","wins": "1","losses": "0","draws": "0","goaldifference": "1","points": "3"
        },
        { "name":"Burnley","gamesplayed":"1","wins": "1","losses": "0","draws": "0","goaldifference": "1","points": "3"
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
        { "name":"Leicester City","gamesplayed":"1","wins": "0","losses": "1","draws": "0","goaldifference": "minus 1","points": "0"
        },
        { "name":"Chelsea","gamesplayed":"1","wins": "0","losses": "1","draws": "0","goaldifference": "minus 1","points": "0"
        },
        { "name":"Bournemoth","gamesplayed":"1","wins": "0","losses": "1","draws": "0","goaldifference": "minus 1","points": "0"
        },
        { "name":"Stoke City","gamesplayed":"1","wins": "0","losses": "1","draws": "0","goaldifference": "minus 1","points": "0"
        },
        { "name":"Brighton","gamesplayed":"0","wins": "0","losses": "0","draws": "0","goaldifference": "minus 2","points": "0"
        },
        { "name":"Newcastle","gamesplayed":"0","wins": "0","losses": "0","draws": "0","goaldifference": "minus 2","points": "0"
        },
        { "name":"Crystal Palace","gamesplayed":"1","wins": "0","losses": "1","draws": "0","goaldifference": "minus 3","points": "0"
        },
        { "name":"West Ham United","gamesplayed":"1","wins": "0","losses": "1","draws": "0","goaldifference": "minus 4","points": "0"
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
    'LaunchRequest2': function () {
        var say = this.t('WELCOME') + ' ' + this.t('HELP');
        console.log('about to scrape the table');
        httpsGet(myRequest,  (myResult) => {
                console.log("sent     : " + myRequest);
                console.log("received : " + myResult);
            }
        );
        console.log('back from scrape the table (too soon?)');
        this.emit(':ask', say, say);
    },

    'LaunchRequest': function () {
        this.emit('MyIntent');
    },

    'MyIntent': function () {
        var say = this.t('WELCOME') + ' ' + this.t('HELP') + ' scrapped web';
        httpsGet(myRequest,  (myResult) => {
                console.log("sent     : " + myRequest);
                // console.log("received : " + myResult);
                this.emit(':ask', say, say );
            }
        );
    },



    'AboutIntent': function () {
        this.emit(':tell', this.t('ABOUT'));
    },

    'ListTeamNamesIntent': function () {
        console.log("at top of ListTeamNamesIntent");
        var say = 'We recognize the following team names';
        say += 'Manchester United, Huddersfield Town, Manchester City, Tottenham Hotspurs, Arsenel, Burnley, Everton, West Bromwich Albion, ';
        say += 'Liverpool, Watford, Southhampton, Swansea City, Leicester City, Chelsea, Bournemouth, Stoke City, Brighton, Newcastle, Crystal Palace and West Ham';
        say += ', , , do you want to list the table, ask about a team or stop?'
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
        console.log('this.event ' + this.event);
        console.log('this.event.request ' + this.event.request);
        console.log('this.event.request.intent ' + this.event.request.intent);
        console.log('this.event.request.intent.slots ' + JSON.stringify(this.event.request.intent.slots));
        console.log('this.event.request.intent.slots ' + JSON.stringify(this.event.request.intent.slots.plteam));
        if(this.event.request.intent.slots.plteam.hasOwnProperty('resolutions')) {
            console.log('we got a resolution');
            console.log('listening for team name ' + JSON.stringify(this.event.request.intent.slots.plteam.resolutions.resolutionsPerAuthority));
            console.log('listening for team name ' + JSON.stringify(this.event.request.intent.slots.plteam.resolutions.resolutionsPerAuthority[0].values));
            console.log('listening for team name ' + JSON.stringify(this.event.request.intent.slots.plteam.resolutions.resolutionsPerAuthority[0].values[0].value));
        } else {
            console.log('we did not get a resolution');
        }
        console.log('confirmationStatus:' + this.event.request.intent.slots.plteam.confirmationStatus);
        var numMatches = this.event.request.intent.slots.plteam.resolutions.resolutionsPerAuthority[0].values.length;
        console.log('there were ' + numMatches + ' matches for name ' + this.event.request.intent.slots.plteam.value)
        console.log('canonical team name ' + this.event.request.intent.slots.plteam.resolutions.resolutionsPerAuthority[0].values[0].value.id);
        team = this.event.request.intent.slots.plteam.value;
        var cannonicalTeam = this.event.request.intent.slots.plteam.resolutions.resolutionsPerAuthority[0].values[0].value.id;
        var say = 'You asked about ' + team ;
        
        teamIndex = findTeamIndex(data, team);
        if(teamIndex == -1) {
            console.log('team not found');
            var say = 'Alexa heard ' + team + ', we did not find them, please say the full team name such as Manchester City.';
            say += ', , , do you want to list the table, ask about a team or stop?';
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

function httpsGet(myData, callback) {

    // GET is a web service request that is fully defined by a URL string
    // Try GET in your browser:
    // https://cp6gckjt97.execute-api.us-east-1.amazonaws.com/prod/stateresource?usstate=New%20Jersey
    console.log('in httpsGet function ' + myData);

    // Update these options with the details of the web service you would like to call
    var options = {
        host: 'www.premierleague.com',
        port: 443,
        path: '/' + encodeURIComponent(myData),
        method: 'GET',

        // if x509 certs are required:
        // key: fs.readFileSync('certs/my-key.pem'),
        // cert: fs.readFileSync('certs/my-cert.pem')
    };

    var req = https.request(options, res => {
        res.setEncoding('utf8');
        var returnData = "";

        res.on('data', chunk => {
            console.log('got some data:' + chunk);
            returnData = returnData + chunk;
        });

        res.on('end', () => {
            console.log('at end of data *************');
            console.log('in res.on end' + JSON.stringify(returnData))
            console.log('at end of logging data *************');
            var parsedHTML = $.load(htmlString)
            console.log('parsed html with cheerio');
            
            //var parsed = JSON.parse(returnData);
            //console.log('parsed json result ' + parsed)
            callback("the return data");  // this will execute whatever function the caller defined, with one argument

        });

    });
    req.end();

}

