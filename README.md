# Chess Debriefer

A backend that parses and analyses pgn files

## Endpoints
<details>
  <summary> 
  <h3> GET /:name/percentages </h3>
  
  </summary>
  
  #### URI parameters
  * **opponent** : (optional) find only the matches played against this opponent
  * **from** : (optional) find only the matches played after this date
  * **to** : (optional) find only the matches played before this date
  * **minelo** : (optional) find only the matches played where your elo was greater than this
  * **maxelo** : (optional) find only the matches played where your elo was lower than this
  
  #### Response
  Headers
  ```
  Content-Type: application/json
  ```
  
<details>
  <summary>Body</summary>
  
  ```json
	{
		"general percentages": {
			"your wins": 117,
			"your losses": 93,
			"your draws": 9,
			"your win percentage": 53.42,
			"your loss percentage": 42.47,
			"your draw percentage": 4.11
		},
		"side percentages": {
			"white": {
				"your wins": 20,
				"your losses": 22,
				"your draws": 4,
				"your win percentage": 43.48,
				"your loss percentage": 47.83,
				"your draw percentage": 8.7
			},
			"black": {
				"your wins": 97,
				"your losses": 71,
				"your draws": 5,
				"your win percentage": 56.07,
				"your loss percentage": 41.04,
				"your draw percentage": 2.89
			}
		}
	}
  ```
</details>
	
</details>

<details>
  <summary> 
  <h3> GET /:name/percentages/compare </h3>
  
  </summary>
  
  #### URI parameters
  * **elo** : (optional) elo used to find other players' stats, otherwise your elo is used
  * **range** : (optional) players used to generate the stats are within this range (elo - range ~ elo + range)
  
  #### Response
  Headers
  ```
  Content-Type: application/json
  ```
  
<details>
  <summary>Body</summary>
  
  ```json
	{
		"general percentages": {
			"your wins": 117,
			"your losses": 93,
			"your draws": 9,
			"your win percentage": 53.42,
			"your loss percentage": 42.47,
			"your draw percentage": 4.11,
			"other players wins": 35435,
			"other players losses": 42096,
			"other players draws": 2448,
			"other players win percentage": 44.31,
			"other players loss percentage": 52.63,
			"other players draw percentage": 3.06
		},
		"side percentages": {
			"white": {
				"your wins": 20,
				"your losses": 22,
				"your draws": 4,
				"your win percentage": 43.48,
				"your loss percentage": 47.83,
				"your draw percentage": 8.7,
				"other players wins": 19063,
				"other players losses": 19879,
				"other players draws": 1242,
				"other players win percentage": 47.44,
				"other players loss percentage": 49.47,
				"other players draw percentage": 3.09
			},
			"black": {
				"your wins": 97,
				"your losses": 71,
				"your draws": 5,
				"your win percentage": 56.07,
				"your loss percentage": 41.04,
				"your draw percentage": 2.89,
				"other players wins": 16372,
				"other players losses": 22217,
				"other players draws": 1206,
				"other players win percentage": 41.14,
				"other players loss percentage": 55.83,
				"other players draw percentage": 3.03
			}
		}
	}
  ```
</details>
	
</details>

<details>
  <summary> 
  <h3> GET /:name/percentages/events </h3>
  
  </summary>
  
  #### URI parameters
  * **opponent** : (optional) find only the matches played against this opponent
  * **from** : (optional) find only the matches played after this date
  * **to** : (optional) find only the matches played before this date
  * **minelo** : (optional) find only the matches played where your elo was greater than this
  * **maxelo** : (optional) find only the matches played where your elo was lower than this
  
  #### Response
  Headers
  ```
  Content-Type: application/json
  ```
  
<details>
  <summary>Body</summary>
  
  ```json
	{
		"Rated Classical game": {
			"your wins": 116,
			"your losses": 92,
			"your draws": 9,
			"your win percentage": 53.46,
			"your loss percentage": 42.4,
			"your draw percentage": 4.15
		},
		"Rated Blitz game": {
			"your wins": 1,
			"your losses": 1,
			"your draws": 0,
			"your win percentage": 50.0,
			"your loss percentage": 50.0,
			"your draw percentage": 0.0
		}
	}
  ```
</details>
	
</details>

<details>
  <summary> 
  <h3> GET /:name/percentages/events/compare </h3>
  
  </summary>
  
  #### URI parameters
  * **elo** : (optional) elo used to find other players' stats, otherwise your elo is used
  * **range** : (optional) players used to generate the stats are within this range (elo - range ~ elo + range)
  * **event** : (optional) which events to find stats on, otherwise all of your events are used
  
  #### Response
  Headers
  ```
  Content-Type: application/json
  ```
  
<details>
  <summary>Body</summary>
  
  ```json
	{
		"Rated Classical game": {
			"your wins": 116,
			"your losses": 92,
			"your draws": 9,
			"your win percentage": 53.46,
			"your loss percentage": 42.4,
			"your draw percentage": 4.15,
			"other players wins": 14870,
			"other players losses": 16505,
			"other players draws": 1110,
			"other players win percentage": 45.77,
			"other players loss percentage": 50.81,
			"other players draw percentage": 3.42
		},
		"Rated Blitz game": {
			"your wins": 1,
			"your losses": 1,
			"your draws": 0,
			"your win percentage": 50.0,
			"your loss percentage": 50.0,
			"your draw percentage": 0.0,
			"other players wins": 13940,
			"other players losses": 16231,
			"other players draws": 946,
			"other players win percentage": 44.8,
			"other players loss percentage": 52.16,
			"other players draw percentage": 3.04
		}
	}
  ```
</details>
	
</details>

<details>
  <summary> 
  <h3> GET /:name/percentages/openings </h3>
  
  </summary>
  
  #### URI parameters
  * **opponent** : (optional) find only the matches played against this opponent
  * **from** : (optional) find only the matches played after this date
  * **to** : (optional) find only the matches played before this date
  * **minelo** : (optional) find only the matches played where your elo was greater than this
  * **maxelo** : (optional) find only the matches played where your elo was lower than this
  * **eco** : (optional) get only and more specific stats on these ecos, separated by a comma or specify a range (from-to)
  
  #### Response
  Headers
  ```
  Content-Type: application/json
  ```
  
<details>
  <summary>Body</summary>
  
  ```json
	{
		"A04": {
			"your wins": 3,
			"your losses": 4,
			"your draws": 0,
			"your win percentage": 42.86,
			"your loss percentage": 57.14,
			"your draw percentage": 0.0
		},
		"A00": {
			"your wins": 31,
			"your losses": 26,
			"your draws": 4,
			"your win percentage": 50.82,
			"your loss percentage": 42.62,
			"your draw percentage": 6.56
		},
		"A13": {
			"your wins": 1,
			"your losses": 2,
			"your draws": 0,
			"your win percentage": 33.33,
			"your loss percentage": 66.67,
			"your draw percentage": 0.0
		},
		"C20": {
			"your wins": 1,
			"your losses": 0,
			"your draws": 0,
			"your win percentage": 100.0,
			"your loss percentage": 0.0,
			"your draw percentage": 0.0
		},
		"C00": {
			"your wins": 48,
			"your losses": 46,
			"your draws": 3,
			"your win percentage": 49.48,
			"your loss percentage": 47.42,
			"your draw percentage": 3.09
		},
		"A40": {
			"your wins": 33,
			"your losses": 14,
			"your draws": 2,
			"your win percentage": 67.35,
			"your loss percentage": 28.57,
			"your draw percentage": 4.08
		},
		"B00": {
			"your wins": 0,
			"your losses": 1,
			"your draws": 0,
			"your win percentage": 0.0,
			"your loss percentage": 100.0,
			"your draw percentage": 0.0
		}
	}
  ```
</details>
	
</details>

<details>
  <summary> 
  <h3> GET /:name/percentages/openings/compare </h3>
  
  </summary>
  
  #### URI parameters
  * **elo** : (optional) elo used to find other players' stats, otherwise your elo is used
  * **range** : (optional) players used to generate the stats are within this range (elo - range ~ elo + range)
  * **eco** : (optional) which ecos to find stats on, otherwise all of your ecos are used (list separated by a comma)
  
  #### Response
  Headers
  ```
  Content-Type: application/json
  ```
  
<details>
  <summary>Body</summary>
  
  ```json
	{
		"A00": {
			"your wins": 31,
			"your losses": 26,
			"your draws": 4,
			"your win percentage": 50.82,
			"your loss percentage": 42.62,
			"your draw percentage": 6.56,
			"other players wins": 3017,
			"other players losses": 3426,
			"other players draws": 200,
			"other players win percentage": 45.42,
			"other players loss percentage": 51.57,
			"other players draw percentage": 3.01
		},
		"A13": {
			"your wins": 1,
			"your losses": 2,
			"your draws": 0,
			"your win percentage": 33.33,
			"your loss percentage": 66.67,
			"your draw percentage": 0.0,
			"other players wins": 105,
			"other players losses": 143,
			"other players draws": 12,
			"other players win percentage": 40.38,
			"other players loss percentage": 55.0,
			"other players draw percentage": 4.62
		},
		"A04": {
			"your wins": 3,
			"your losses": 4,
			"your draws": 0,
			"your win percentage": 42.86,
			"your loss percentage": 57.14,
			"your draw percentage": 0.0,
			"other players wins": 392,
			"other players losses": 548,
			"other players draws": 25,
			"other players win percentage": 40.62,
			"other players loss percentage": 56.79,
			"other players draw percentage": 2.59
		},
		"C20": {
			"your wins": 1,
			"your losses": 0,
			"your draws": 0,
			"your win percentage": 100.0,
			"your loss percentage": 0.0,
			"your draw percentage": 0.0,
			"other players wins": 2015,
			"other players losses": 2067,
			"other players draws": 116,
			"other players win percentage": 48.0,
			"other players loss percentage": 49.24,
			"other players draw percentage": 2.76
		},
		"B00": {
			"your wins": 0,
			"your losses": 1,
			"your draws": 0,
			"your win percentage": 0.0,
			"your loss percentage": 100.0,
			"your draw percentage": 0.0,
			"other players wins": 2563,
			"other players losses": 3059,
			"other players draws": 171,
			"other players win percentage": 44.24,
			"other players loss percentage": 52.81,
			"other players draw percentage": 2.95
		},
		"C00": {
			"your wins": 48,
			"your losses": 46,
			"your draws": 3,
			"your win percentage": 49.48,
			"your loss percentage": 47.42,
			"your draw percentage": 3.09,
			"other players wins": 1876,
			"other players losses": 2083,
			"other players draws": 113,
			"other players win percentage": 46.07,
			"other players loss percentage": 51.15,
			"other players draw percentage": 2.78
		},
		"A40": {
			"your wins": 33,
			"your losses": 14,
			"your draws": 2,
			"your win percentage": 67.35,
			"your loss percentage": 28.57,
			"your draw percentage": 4.08,
			"other players wins": 2415,
			"other players losses": 2870,
			"other players draws": 153,
			"other players win percentage": 44.41,
			"other players loss percentage": 52.78,
			"other players draw percentage": 2.81
		}
	}
  ```
</details>
	
</details>

<details>
  <summary> 
  <h3> GET /:name/percentages/openings/best-worst </h3>
  
  </summary>
  
  #### URI parameters
  * **opponent** : (optional) find only the matches played against this opponent (only filters your best worst openings)
  * **from** : (optional) find only the matches played after this date (only filters your best worst openings)
  * **to** : (optional) find only the matches played before this date (only filters your best worst openings)
  * **minelo** : (optional) find only the matches played where your elo was greater than this (only filters your best worst openings)
  * **maxelo** : (optional) find only the matches played where your elo was lower than this (only filters your best worst openings)
  * **elo** : (optional) elo used to find other players' stats, otherwise your elo is used
  * **range** : (optional) players used to generate the stats are within this range (elo - range ~ elo + range)
  * **limit** : (optional) openings list limit (default is 3)
  * **min_played** : (optional) only considers openings that have at least this many matches played
  
  #### Response
  Headers
  ```
  Content-Type: application/json
  ```
  
<details>
  <summary>Body</summary>
  
  ```json
	{
		"your best": [
			"B01",
			"C02",
			"C23"
		],
		"your worst": [
			"C24",
			"C00",
			"B20"
		],
		"other players best": [
			"C28",
			"C48",
			"D01"
		],
		"other players worst": [
			"C80",
			"B31",
			"C11"
		]
	}
  ```
</details>
	
</details>

<details>
  <summary> 
  <h3> GET /:name/percentages/terminations </h3>
  
  </summary>
  
  #### URI parameters
  * **opponent** : (optional) find only the matches played against this opponent
  * **from** : (optional) find only the matches played after this date
  * **to** : (optional) find only the matches played before this date
  * **minelo** : (optional) find only the matches played where your elo was greater than this
  * **maxelo** : (optional) find only the matches played where your elo was lower than this
  
  #### Response
  Headers
  ```
  Content-Type: application/json
  ```
  
<details>
  <summary>Body</summary>
  
  ```json
	{
		"Normal": {
			"your wins": 101,
			"your losses": 87,
			"your draws": 9,
			"your win percentage": 51.27,
			"your loss percentage": 44.16,
			"your draw percentage": 4.57
		},
		"Time forfeit": {
			"your wins": 16,
			"your losses": 6,
			"your draws": 0,
			"your win percentage": 72.73,
			"your loss percentage": 27.27,
			"your draw percentage": 0.0
		}
	}
  ```
</details>
	
</details>

<details>
  <summary> 
  <h3> GET /:name/percentages/terminations/compare </h3>
  
  </summary>
  
  #### URI parameters
  * **elo** : (optional) elo used to find other players' stats, otherwise your elo is used
  * **range** : (optional) players used to generate the stats are within this range (elo - range ~ elo + range)
  * **termination** : (optional) which terminations to find stats on, otherwise all of your terminations are used
  
  #### Response
  Headers
  ```
  Content-Type: application/json
  ```
  
<details>
  <summary>Body</summary>
  
  ```json
	{
		"Normal": {
			"your wins": 101,
			"your losses": 87,
			"your draws": 9,
			"your win percentage": 51.27,
			"your loss percentage": 44.16,
			"your draw percentage": 4.57,
			"other players wins": 24634,
			"other players losses": 29923,
			"other players draws": 2187,
			"other players win percentage": 43.41,
			"other players loss percentage": 52.73,
			"other players draw percentage": 3.85
		},
		"Time forfeit": {
			"your wins": 16,
			"your losses": 6,
			"your draws": 0,
			"your win percentage": 72.73,
			"your loss percentage": 27.27,
			"your draw percentage": 0.0,
			"other players wins": 10801,
			"other players losses": 12173,
			"other players draws": 261,
			"other players win percentage": 46.49,
			"other players loss percentage": 52.39,
			"other players draw percentage": 1.12
		}
	}
  ```
</details>
	
</details>

<details>
  <summary> 
  <h3> GET /:name/percentages/throws-comebacks </h3>
  
  </summary>
  
  #### URI parameters
  * **opponent** : (optional) find only the matches played against this opponent
  * **from** : (optional) find only the matches played after this date
  * **to** : (optional) find only the matches played before this date
  * **minelo** : (optional) find only the matches played where your elo was greater than this
  * **maxelo** : (optional) find only the matches played where your elo was lower than this
  
  #### Response
  Headers
  ```
  Content-Type: application/json
  ```
  
<details>
  <summary>Body</summary>
  
  ```json
	{
		"throws": 34,
		"losses": 86,
		"percentage_throws": 39.53,
		"comebacks": 10,
		"wins": 105,
		"percentage_comebacks": 9.52
	}
  ```
</details>
	
</details>

<details>
  <summary> 
  <h3> GET /:name/percentages/endgames </h3>
  
  </summary>
  
  #### URI parameters
  * **pieces** : (optional) how many pieces must be left on the board (at least) to be considered an endgame
  * **opponent** : (optional) find only the matches played against this opponent
  * **from** : (optional) find only the matches played after this date
  * **to** : (optional) find only the matches played before this date
  * **minelo** : (optional) find only the matches played where your elo was greater than this
  * **maxelo** : (optional) find only the matches played where your elo was lower than this
  
  #### Response
  Headers
  ```
  Content-Type: application/json
  ```
  
<details>
  <summary>Body</summary>
  
  ```json
	{
		"general percentages": {
			"games": 219,
			"endgames": 54,
			"percentage of games that finish in the endgame": 24.66,
			"wins": 23,
			"losses": 25,
			"draws": 6,
			"win percentage": 42.59,
			"loss percentage": 46.3,
			"draw percentage": 11.11
		},
		"side percentages": {
			"white": {
				"wins": 3,
				"losses": 5,
				"draws": 2,
				"win percentage": 30.0,
				"loss percentage": 50.0,
				"draw percentage": 20.0
			},
			"black": {
				"wins": 20,
				"losses": 20,
				"draws": 4,
				"win percentage": 45.45,
				"loss percentage": 45.45,
				"draw percentage": 9.09
			}
		}
	}
  ```
</details>
	
</details>

<details>
  <summary> 
  <h3> GET /:name/percentages/endgames/compare </h3>
  
  </summary>
  
  #### URI parameters
  * **elo** : (optional) elo used to find other players' stats, otherwise your elo is used
  * **range** : (optional) players used to generate the stats are within this range (elo - range ~ elo + range)
  
  #### Response
  Headers
  ```
  Content-Type: application/json
  ```
  
<details>
  <summary>Body</summary>
  
  ```json
	{
		"general percentages": {
			"games": 184,
			"endgames": 17,
			"percentage of games that finish in the endgame": 9.24,
			"wins": 4,
			"losses": 8,
			"draws": 5,
			"win percentage": 23.53,
			"loss percentage": 47.06,
			"draw percentage": 29.41,
			"other players games": 4077,
			"other players wins": 3083,
			"other players losses": 3082,
			"other players draws": 1978,
			"other players win percentage": 37.86,
			"other players loss percentage": 37.85,
			"other players draw percentage": 24.29
		},
		"side percentages": {
			"white": {
				"wins": 1,
				"losses": 1,
				"draws": 2,
				"win percentage": 25.0,
				"loss percentage": 25.0,
				"draw percentage": 50.0,
				"other players wins": 1532,
				"other players losses": 1554,
				"other players draws": 990,
				"other players win percentage": 37.59,
				"other players loss percentage": 38.13,
				"other players draw percentage": 24.29
			},
			"black": {
				"wins": 3,
				"losses": 7,
				"draws": 3,
				"win percentage": 23.08,
				"loss percentage": 53.85,
				"draw percentage": 23.08,
				"other players wins": 1551,
				"other players losses": 1528,
				"other players draws": 988,
				"other players win percentage": 38.14,
				"other players loss percentage": 37.57,
				"other players draw percentage": 24.29
			}
		}
	}
  ```
</details>
	
</details>

<details>
  <summary> 
  <h3> GET /:name/percentages/endgames/material </h3>
  
  </summary>
  
  #### URI parameters
  * **pieces** : (optional) how many pieces must be left on the board (at least) to be considered an endgame
  * **opponent** : (optional) find only the matches played against this opponent
  * **from** : (optional) find only the matches played after this date
  * **to** : (optional) find only the matches played before this date
  * **minelo** : (optional) find only the matches played where your elo was greater than this
  * **maxelo** : (optional) find only the matches played where your elo was lower than this
  
  #### Response
  Headers
  ```
  Content-Type: application/json
  ```
  
<details>
  <summary>Body</summary>
  
  ```json
	{
		"wins": 23,
		"matches you should have won (material advantage)": 16,
		"losses": 25,
		"matches you should have lost (material disadvantage)": 24,
		"draws": 6,
		"draws with material advantage": 2,
		"draws with material disadvantage": 4
	}
  ```
</details>
	
</details>

<details>
  <summary> 
  <h3> GET /:name/percentages/endgames/material/compare </h3>
  
  </summary>
  
  #### URI parameters
  * **elo** : (optional) elo used to find other players' stats, otherwise your elo is used
  * **range** : (optional) players used to generate the stats are within this range (elo - range ~ elo + range)
  
  #### Response
  Headers
  ```
  Content-Type: application/json
  ```
  
<details>
  <summary>Body</summary>
  
  ```json
	{
		"wins": 4,
		"matches you should have won (material advantage)": 4,
		"losses": 8,
		"matches you should have lost (material disadvantage)": 7,
		"draws": 5,
		"draws with material advantage": 3,
		"draws with material disadvantage": 2,
		"other players wins": 3083,
		"matches other players should have won (material advantage)": 2717,
		"other players losses": 3082,
		"matches other players should have lost (material disadvantage)": 2717,
		"other players draws": 1978,
		"other players draws with material advantage": 989,
		"other players draws with material disadvantage": 989
	}
  ```
</details>
	
</details>

<details>
  <summary> 
  <h3> GET /:name/percentages/endgames/tablebase </h3>
  
  </summary>
  
  #### URI parameters
  * **pieces** : (optional) how many pieces must be left on the board (at least) to be considered an endgame (maximum is 5 for tablebase)
  * **opponent** : (optional) find only the matches played against this opponent
  * **from** : (optional) find only the matches played after this date
  * **to** : (optional) find only the matches played before this date
  * **minelo** : (optional) find only the matches played where your elo was greater than this
  * **maxelo** : (optional) find only the matches played where your elo was lower than this
  
  #### Response
  Headers
  ```
  Content-Type: application/json
  ```
  
<details>
  <summary>Body</summary>
  
  ```json
	{
		"wins": 4,
		"matches you should have won": 4,
		"losses": 10,
		"matches you should have lost": 9,
		"draws": 5,
		"matches you should have drawn": 4
	}
  ```
</details>
	
</details>

<details>
  <summary> 
  <h3> GET /:name/percentages/endgames/tablebase/compare </h3>
  
  </summary>
  
  #### URI parameters
  * **elo** : (optional) elo used to find other players' stats, otherwise your elo is used
  * **range** : (optional) players used to generate the stats are within this range (elo - range ~ elo + range)
  
  #### Response
  Headers
  ```
  Content-Type: application/json
  ```
  
<details>
  <summary>Body</summary>
  
  ```json
	{
		"wins": 4,
		"matches you should have won": 4,
		"losses": 8,
		"matches you should have lost": 7,
		"draws": 5,
		"matches you should have drawn": 4,
		"other players wins": 3083,
		"matches other players should have won": 2740,
		"other players losses": 3082,
		"matches other players should have lost": 2740,
		"other players draws": 1978,
		"matches other players should have drawn": 1125
	}
  ```
</details>
	
</details>

<details>
  <summary>
  <h3> GET /:name/accuracy </h3>
  </summary>
  
  #### URI parameters
  * None
  
  #### Response
  Headers
  ```
  Content-Type: application/json
  ```
  
<details>
  <summary>Body</summary>
  
  ```json
	{
		"general accuracy": 28.98,
		"accuracy after opening": 30.21
	}
  ```
</details>

</details>

<details>
  <summary>
  <h3> GET /:eco/stats </h3>
  </summary>
  
  #### URI parameters
  * **tournament** : (optional) get opening statistics only based on tournament games
  * **min_elo** : (optional) get opening statistics only based on games that have at least this elo
  * **elo** : (optional) elo used to find the matches, can be used only if min_elo isn't specified
  * **range** : (optional) matches used to generate the stats when using elo param are within this range (elo - range ~ elo + range)
  
  #### Response
  Headers
  ```
  Content-Type: application/json
  ```
  
<details>
  <summary>Body</summary>
  
  ```json
	{
		"E30": {
			"white_wins": 3,
			"black_wins": 24,
			"draws": 1,
			"percentage_white_wins": 10.71,
			"percentage_black_wins": 85.71,
			"percentage_draws_wins": 3.57
		},
		"variations": {
			"Nimzo-Indian Leningrad Variation ": {
				"white_wins": 3,
				"black_wins": 24,
				"draws": 1,
				"white_win_percentage": 10.71,
				"black_win_percentage": 85.71,
				"draw_percentage": 3.57,
				"engine_evaluation": -0.15
			},
			"Nimzo-Indian Leningrad, ...b5 gambit": {
				"white_wins": 0,
				"black_wins": 0,
				"draws": 0,
				"white_win_percentage": 0.0,
				"black_win_percentage": 0.0,
				"draw_percentage": 0.0,
				"engine_evaluation": 0.14
			}
		}
	}
  ```
</details>

</details>

<details>
  <summary>
  <h3> POST /upload </h3>
  </summary>
  
  #### URI parameters
  * None
  
  #### Request
  Headers
  ```
  Content-Type: multipart/form-data
  ```
  
<details>
  <summary>Body</summary>
  
  KEY: file
  VALUE: the pgn file
</details>
  
  #### Response
  Headers
  ```
  Content-Type: text/html
  ```
  
<details>
  <summary>Body</summary>
  
  None
</details>

</details>

<details>
  <summary>
  <h3> POST /upload/openings </h3>
  </summary>
  
  #### URI parameters
  * None
  
  #### Request
  Headers
  ```
  Content-Type: multipart/form-data
  ```
  
<details>
  <summary>Body</summary>
  
  KEY: file
  VALUE: the pgn file
</details>
  
  #### Response
  Headers
  ```
  Content-Type: text/html
  ```
  
<details>
  <summary>Body</summary>
  
  None
</details>

</details>
