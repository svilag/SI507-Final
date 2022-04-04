# Final Project Proposal

## Data Sources

Winter Guard International website: [https://wgi.org/#](https://wgi.org/#)

The plan is to use BeautifulSoup to parse the scores on the WGI website. There are three types of scores: `percission`, `color guard`, and `winds`. Scores are broken down by participating group, and are divided into different subcategories depending on the type of competition, with an overall score. Each year of competition also has scores for multiple classes based on skill level.

Percussion scores are divided into: `effect - music`, `effect - visual`, `music`, and `visual`.

Color Guard scores are divided into: `equipment analysis`, `movement analysis`, `design analysis`, and `general effect`

Winds scores are divided into: `overall effect`, `music analysis`, and `visual analysis`

[https://www.crummy.com/software/BeautifulSoup/bs4/doc/](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

## Data Access and Storage

The HTML pages the scores are on will be cached and then parsed to JSON records.

ex link with scores: [https://recaps.competitionsuite.com/d46f147c-0bad-4f12-86b3-4a9077686a07.htm](https://recaps.competitionsuite.com/d46f147c-0bad-4f12-86b3-4a9077686a07.htm)

ex JSON records:

```json
{"2018":{
    "Winds Scholastic A":{
        "group_name":{
            "overall effect": {
                "score": 10,
                "adjudicators": ["name","name"]
            },
            "music analysis": {
                "score": 10,
                "adjudicators": ["name","name"]
            },
            "visual analysis": {
                "score": 10,
                "adjudicators": ["name","name"]
            },
            "total score": 10
        },
        "group_name":{
            "overall effect": {
                "score": 10,
                "adjudicators": ["name","name"]
            },
            "music analysis": {
                "score": 10,
                "adjudicators": ["name","name"]
            },
            "visual analysis": {
                "score": 10,
                "adjudicators": ["name","name"]
            },
            "total score": 10
        },
        "group_name":{
            "overall effect": {
                "score": 10,
                "adjudicators": ["name","name"]
            },
            "music analysis": {
                "score": 10,
                "adjudicators": ["name","name"]
            },
            "visual analysis": {
                "score": 10,
                "adjudicators": ["name","name"]
            },
            "total score": 10
        },
    }
}}
```

## Data Presentation

The plan for data presentation is to create a Flask application with a form for the user to input options to search for specific data.
