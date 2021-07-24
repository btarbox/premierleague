datasources2 = {

    "gridListData": {
        "type": "object",
        "objectId": "gridListSample",
        "backgroundImage": {
            "contentDescription": "this is the content",
            "smallSourceUrl": "https://duy7y3nglgmh.cloudfront.net/football_pitch.png",
            "largeSourceUrl": "https://duy7y3nglgmh.cloudfront.net/football_pitch.png",
            "sources": [
                {
                    "url": "https://duy7y3nglgmh.cloudfront.net/football_pitch.png",
                    "size": "small",
                    "widthPixels": 0,
                    "heightPixels": 0
                },
                {
                    "url": "https://duy7y3nglgmh.cloudfront.net/football_pitch.png",
                    "size": "large",
                    "widthPixels": 0,
                    "heightPixels": 0
                }
            ]
        },
        "title": "You can ask about ....",
        "listItems": [
            {
                "primaryText": "The Table",
                "imageSource": "https://duy7y3nglgmh.cloudfront.net/table.png",
                "primaryAction": [{"type": "SendEvent","arguments": ["table"]}]
            },
            {
                "primaryText": "Fixtures",
                "imageSource": "https://duy7y3nglgmh.cloudfront.net/fixtures.png",
                "primaryAction": [{"type": "SendEvent","arguments": ["fixtures"]}]
            },
            {
                "primaryText": "Results",
                "imageSource": "https://duy7y3nglgmh.cloudfront.net/results.png",
                "primaryAction": [{"type": "SendEvent","arguments": ["results"]}]
            },
            {
                "primaryText": "Relegation",
                "imageSource": "https://duy7y3nglgmh.cloudfront.net/relegation.png",
                "primaryAction": [{"type": "SendEvent","arguments": ["relegation"]}]
            },
            {
                "primaryText": "Tackles",
                "imageSource": "https://duy7y3nglgmh.cloudfront.net/tackles.png",
                "primaryAction": [{"type": "SendEvent","arguments": ["tackles"]}]
            },
            {
                "primaryText": "Touches",
                "imageSource": "https://duy7y3nglgmh.cloudfront.net/Depositphotos_touches.jpg",
                "primaryAction": [{"type": "SendEvent","arguments": ["touches"]}]
            },
            {
                "primaryText": "Fouls",
                "imageSource": "https://duy7y3nglgmh.cloudfront.net/fouls.png",
                "primaryAction": [{"type": "SendEvent","arguments": ["fouls"]}]
            },
            {
                "primaryText": "Goals",
                "imageSource": "https://duy7y3nglgmh.cloudfront.net/Depositphotos_goal.jpg",
                "primaryAction": [{"type": "SendEvent","arguments": ["goals"]}]
            },
            {
                "primaryText": "Clean Sheets",
                "imageSource": "https://duy7y3nglgmh.cloudfront.net/Depositphotos_keeper.jpg",
                "primaryAction": [{"type": "SendEvent","arguments": ["cleansheet"]}]
            },
            {
                "primaryText": "Yellow Card",
                "imageSource": "https://duy7y3nglgmh.cloudfront.net/yellowcard.png",
                "primaryAction": [{"type": "SendEvent","arguments": ["yellowcard"]}]
            },
            {
                "primaryText": "Red Card",
                "imageSource": "https://duy7y3nglgmh.cloudfront.net/redcard.png",
                "primaryAction": [{"type": "SendEvent","arguments": ["redcard"]}]
            },
            {
                "primaryText": "Referees",
                "imageSource": "https://duy7y3nglgmh.cloudfront.net/Depositphotos_referee.jpg",
                "primaryAction": [{"type": "SendEvent","arguments": ["referee"]}]
            },
        ],
        "logoUrl": "https://duy7y3nglgmh.cloudfront.net/redcard.png"
    }                        
} 

test_speach_data =  {
    "referee" : "The most used referees are Martin Atkinson with 22 yellow cards and 4 red cards, \
                              Anthony Taylor with 3 yellow cards and 17 red cards",
    "touches" : "The players with the most touches were Kane with all of them, Son with some of them, and Vardy with the rest of them "
    
}

noise_data = [
    ("https://duy7y3nglgmh.cloudfront.net/FootballCrowdSound.mp3", 4 * 60 * 1000),
    ("https://duy7y3nglgmh.cloudfront.net/SoccerStadiumSoundEffect.mp3", 40 * 1000),
    ("https://duy7y3nglgmh.cloudfront.net/SportsStadiumCrowdCheering", 40 * 1000)
]
