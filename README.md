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
		"General percentages": {
			"percentage_won": 52.76,
			"percentage_lost": 43.22,
			"percentage_drawn": 4.02,
			"won_games": 105,
			"lost_games": 86,
			"drawn_games": 8
		},
		"Side percentages": {
			"White": {
				"percentage_won": 53.57,
				"percentage_lost": 42.86,
				"percentage_drawn": 3.57,
				"won_games": 45,
				"lost_games": 36,
				"drawn_games": 3
			},
			"Black": {
				"percentage_won": 52.17,
				"percentage_lost": 43.48,
				"percentage_drawn": 4.35,
				"won_games": 60,
				"lost_games": 50,
				"drawn_games": 5
			}
		},
		"Throw comeback percentages": {
			"throws": 34,
			"losses": 86,
			"percentage_throws": 39.53,
			"comebacks": 10,
			"wins": 105,
			"percentage_comebacks": 9.52
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
			"other players wins": 35435,
			"your losses": 93,
			"other players losses": 42096,
			"your draws": 9,
			"other players draws": 2448
		},
		"side percentages": {
			"white": {
				"your wins": 20,
				"your losses": 22,
				"your draws": 4,
				"other players wins": 19063,
				"other players losses": 19879,
				"other players draws": 1242
			},
			"black": {
				"your wins": 97,
				"your losses": 71,
				"your draws": 5,
				"other players wins": 16372,
				"other players losses": 22217,
				"other players draws": 1206
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
			"percentage_won": 52.78,
			"percentage_lost": 41.67,
			"percentage_drawn": 5.56,
			"won_games": 19,
			"lost_games": 15,
			"drawn_games": 2
		},
		"Rated Bullet game": {
			"percentage_won": 66.67,
			"percentage_lost": 33.33,
			"percentage_drawn": 0.0,
			"won_games": 2,
			"lost_games": 1,
			"drawn_games": 0
		},
		"Rated Blitz game": {
			"percentage_won": 51.92,
			"percentage_lost": 44.23,
			"percentage_drawn": 3.85,
			"won_games": 81,
			"lost_games": 69,
			"drawn_games": 6
		},
		"Rated Blitz tournament": {
			"percentage_won": 75.0,
			"percentage_lost": 25.0,
			"percentage_drawn": 0.0,
			"won_games": 3,
			"lost_games": 1,
			"drawn_games": 0
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
			"other players wins": 14870,
			"your win percentage": 53.46,
			"other players win percentage": 45.77,
			"your losses": 92,
			"other players losses": 16505,
			"your loss percentage": 42.4,
			"other players loss percentage": 50.81,
			"your draws": 9,
			"other players draws": 1110,
			"your draw percentage": 4.15,
			"other players draw percentage": 3.42
		},
		"Rated Blitz game": {
			"your wins": 1,
			"other players wins": 13940,
			"your win percentage": 50.0,
			"other players win percentage": 44.8,
			"your losses": 1,
			"other players losses": 16231,
			"your loss percentage": 50.0,
			"other players loss percentage": 52.16,
			"your draws": 0,
			"other players draws": 946,
			"your draw percentage": 0.0,
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
  * **eco** : (optional) get only and more specific stats on these ecos, separated by a comma
  
  #### Response
  Headers
  ```
  Content-Type: application/json
  ```
  
<details>
  <summary>Body</summary>
  
  ```json
	{
		"A01": {
			"percentage_won": 0.0,
			"percentage_lost": 100.0,
			"percentage_drawn": 0.0,
			"won_games": 0,
			"lost_games": 1,
			"drawn_games": 0,
			"events": {
				"Rated Blitz game": {
					"percentage_won": 0.0,
					"percentage_lost": 100.0,
					"percentage_drawn": 0.0,
					"won_games": 0,
					"lost_games": 1,
					"drawn_games": 0
				}
			}
		},
		"A00": {
			"percentage_won": 55.56,
			"percentage_lost": 44.44,
			"percentage_drawn": 0.0,
			"won_games": 5,
			"lost_games": 4,
			"drawn_games": 0,
			"events": {
				"Rated Classical game": {
					"percentage_won": 50.0,
					"percentage_lost": 50.0,
					"percentage_drawn": 0.0,
					"won_games": 1,
					"lost_games": 1,
					"drawn_games": 0
				},
				"Rated Blitz game": {
					"percentage_won": 57.14,
					"percentage_lost": 42.86,
					"percentage_drawn": 0.0,
					"won_games": 4,
					"lost_games": 3,
					"drawn_games": 0
				}
			}
		},
		"C00": {
			"percentage_won": 75.0,
			"percentage_lost": 25.0,
			"percentage_drawn": 0.0,
			"won_games": 6,
			"lost_games": 2,
			"drawn_games": 0,
			"events": {
				"Rated Blitz game": {
					"percentage_won": 75.0,
					"percentage_lost": 25.0,
					"percentage_drawn": 0.0,
					"won_games": 6,
					"lost_games": 2,
					"drawn_games": 0
				}
			}
		},
		"B01": {
			"percentage_won": 50.0,
			"percentage_lost": 50.0,
			"percentage_drawn": 0.0,
			"won_games": 3,
			"lost_games": 3,
			"drawn_games": 0,
			"events": {
				"Rated Blitz game": {
					"percentage_won": 50.0,
					"percentage_lost": 50.0,
					"percentage_drawn": 0.0,
					"won_games": 3,
					"lost_games": 3,
					"drawn_games": 0
				}
			}
		},
		"A40": {
			"percentage_won": 21.74,
			"percentage_lost": 73.91,
			"percentage_drawn": 4.35,
			"won_games": 5,
			"lost_games": 17,
			"drawn_games": 1,
			"events": {
				"Rated Classical game": {
					"percentage_won": 0.0,
					"percentage_lost": 50.0,
					"percentage_drawn": 50.0,
					"won_games": 0,
					"lost_games": 1,
					"drawn_games": 1
				},
				"Rated Blitz game": {
					"percentage_won": 23.81,
					"percentage_lost": 76.19,
					"percentage_drawn": 0.0,
					"won_games": 5,
					"lost_games": 16,
					"drawn_games": 0
				}
			}
		},
		"A04": {
			"percentage_won": 25.0,
			"percentage_lost": 75.0,
			"percentage_drawn": 0.0,
			"won_games": 1,
			"lost_games": 3,
			"drawn_games": 0,
			"events": {
				"Rated Classical game": {
					"percentage_won": 0.0,
					"percentage_lost": 100.0,
					"percentage_drawn": 0.0,
					"won_games": 0,
					"lost_games": 1,
					"drawn_games": 0
				},
				"Rated Blitz game": {
					"percentage_won": 33.33,
					"percentage_lost": 66.67,
					"percentage_drawn": 0.0,
					"won_games": 1,
					"lost_games": 2,
					"drawn_games": 0
				}
			}
		},
		"A45": {
			"percentage_won": 100.0,
			"percentage_lost": 0.0,
			"percentage_drawn": 0.0,
			"won_games": 2,
			"lost_games": 0,
			"drawn_games": 0,
			"events": {
				"Rated Classical game": {
					"percentage_won": 100.0,
					"percentage_lost": 0.0,
					"percentage_drawn": 0.0,
					"won_games": 1,
					"lost_games": 0,
					"drawn_games": 0
				},
				"Rated Blitz game": {
					"percentage_won": 100.0,
					"percentage_lost": 0.0,
					"percentage_drawn": 0.0,
					"won_games": 1,
					"lost_games": 0,
					"drawn_games": 0
				}
			}
		},
		"B06": {
			"percentage_won": 70.0,
			"percentage_lost": 22.5,
			"percentage_drawn": 7.5,
			"won_games": 28,
			"lost_games": 9,
			"drawn_games": 3,
			"events": {
				"Rated Bullet game": {
					"percentage_won": 100.0,
					"percentage_lost": 0.0,
					"percentage_drawn": 0.0,
					"won_games": 2,
					"lost_games": 0,
					"drawn_games": 0
				},
				"Rated Blitz game": {
					"percentage_won": 69.44,
					"percentage_lost": 22.22,
					"percentage_drawn": 8.33,
					"won_games": 25,
					"lost_games": 8,
					"drawn_games": 3
				},
				"Rated Blitz tournament": {
					"percentage_won": 50.0,
					"percentage_lost": 50.0,
					"percentage_drawn": 0.0,
					"won_games": 1,
					"lost_games": 1,
					"drawn_games": 0
				}
			}
		},
		"B20": {
			"percentage_won": 100.0,
			"percentage_lost": 0.0,
			"percentage_drawn": 0.0,
			"won_games": 7,
			"lost_games": 0,
			"drawn_games": 0,
			"events": {
				"Rated Classical game": {
					"percentage_won": 100.0,
					"percentage_lost": 0.0,
					"percentage_drawn": 0.0,
					"won_games": 6,
					"lost_games": 0,
					"drawn_games": 0
				},
				"Rated Blitz game": {
					"percentage_won": 100.0,
					"percentage_lost": 0.0,
					"percentage_drawn": 0.0,
					"won_games": 1,
					"lost_games": 0,
					"drawn_games": 0
				}
			}
		},
		"C60": {
			"percentage_won": 57.14,
			"percentage_lost": 28.57,
			"percentage_drawn": 14.29,
			"won_games": 4,
			"lost_games": 2,
			"drawn_games": 1,
			"events": {
				"Rated Classical game": {
					"percentage_won": 66.67,
					"percentage_lost": 33.33,
					"percentage_drawn": 0.0,
					"won_games": 2,
					"lost_games": 1,
					"drawn_games": 0
				},
				"Rated Blitz game": {
					"percentage_won": 50.0,
					"percentage_lost": 25.0,
					"percentage_drawn": 25.0,
					"won_games": 2,
					"lost_games": 1,
					"drawn_games": 1
				}
			}
		},
		"B00": {
			"percentage_won": 27.27,
			"percentage_lost": 54.55,
			"percentage_drawn": 18.18,
			"won_games": 3,
			"lost_games": 6,
			"drawn_games": 2,
			"events": {
				"Rated Blitz game": {
					"percentage_won": 27.27,
					"percentage_lost": 54.55,
					"percentage_drawn": 18.18,
					"won_games": 3,
					"lost_games": 6,
					"drawn_games": 2
				}
			}
		},
		"B21": {
			"percentage_won": 50.0,
			"percentage_lost": 50.0,
			"percentage_drawn": 0.0,
			"won_games": 2,
			"lost_games": 2,
			"drawn_games": 0,
			"events": {
				"Rated Classical game": {
					"percentage_won": 0.0,
					"percentage_lost": 100.0,
					"percentage_drawn": 0.0,
					"won_games": 0,
					"lost_games": 1,
					"drawn_games": 0
				},
				"Rated Blitz game": {
					"percentage_won": 66.67,
					"percentage_lost": 33.33,
					"percentage_drawn": 0.0,
					"won_games": 2,
					"lost_games": 1,
					"drawn_games": 0
				}
			}
		},
		"C41": {
			"percentage_won": 78.57,
			"percentage_lost": 21.43,
			"percentage_drawn": 0.0,
			"won_games": 11,
			"lost_games": 3,
			"drawn_games": 0,
			"events": {
				"Rated Classical game": {
					"percentage_won": 100.0,
					"percentage_lost": 0.0,
					"percentage_drawn": 0.0,
					"won_games": 1,
					"lost_games": 0,
					"drawn_games": 0
				},
				"Rated Blitz game": {
					"percentage_won": 76.92,
					"percentage_lost": 23.08,
					"percentage_drawn": 0.0,
					"won_games": 10,
					"lost_games": 3,
					"drawn_games": 0
				}
			}
		},
		"B23": {
			"percentage_won": 50.0,
			"percentage_lost": 50.0,
			"percentage_drawn": 0.0,
			"won_games": 5,
			"lost_games": 5,
			"drawn_games": 0,
			"events": {
				"Rated Blitz game": {
					"percentage_won": 50.0,
					"percentage_lost": 50.0,
					"percentage_drawn": 0.0,
					"won_games": 5,
					"lost_games": 5,
					"drawn_games": 0
				}
			}
		},
		"C68": {
			"percentage_won": 0.0,
			"percentage_lost": 100.0,
			"percentage_drawn": 0.0,
			"won_games": 0,
			"lost_games": 1,
			"drawn_games": 0,
			"events": {
				"Rated Blitz game": {
					"percentage_won": 0.0,
					"percentage_lost": 100.0,
					"percentage_drawn": 0.0,
					"won_games": 0,
					"lost_games": 1,
					"drawn_games": 0
				}
			}
		},
		"C03": {
			"percentage_won": 50.0,
			"percentage_lost": 50.0,
			"percentage_drawn": 0.0,
			"won_games": 1,
			"lost_games": 1,
			"drawn_games": 0,
			"events": {
				"Rated Classical game": {
					"percentage_won": 0.0,
					"percentage_lost": 100.0,
					"percentage_drawn": 0.0,
					"won_games": 0,
					"lost_games": 1,
					"drawn_games": 0
				},
				"Rated Blitz tournament": {
					"percentage_won": 100.0,
					"percentage_lost": 0.0,
					"percentage_drawn": 0.0,
					"won_games": 1,
					"lost_games": 0,
					"drawn_games": 0
				}
			}
		},
		"C43": {
			"percentage_won": 50.0,
			"percentage_lost": 50.0,
			"percentage_drawn": 0.0,
			"won_games": 1,
			"lost_games": 1,
			"drawn_games": 0,
			"events": {
				"Rated Bullet game": {
					"percentage_won": 0.0,
					"percentage_lost": 100.0,
					"percentage_drawn": 0.0,
					"won_games": 0,
					"lost_games": 1,
					"drawn_games": 0
				},
				"Rated Blitz game": {
					"percentage_won": 100.0,
					"percentage_lost": 0.0,
					"percentage_drawn": 0.0,
					"won_games": 1,
					"lost_games": 0,
					"drawn_games": 0
				}
			}
		},
		"C65": {
			"percentage_won": 100.0,
			"percentage_lost": 0.0,
			"percentage_drawn": 0.0,
			"won_games": 2,
			"lost_games": 0,
			"drawn_games": 0,
			"events": {
				"Rated Blitz game": {
					"percentage_won": 100.0,
					"percentage_lost": 0.0,
					"percentage_drawn": 0.0,
					"won_games": 2,
					"lost_games": 0,
					"drawn_games": 0
				}
			}
		},
		"C61": {
			"percentage_won": 0.0,
			"percentage_lost": 100.0,
			"percentage_drawn": 0.0,
			"won_games": 0,
			"lost_games": 1,
			"drawn_games": 0,
			"events": {
				"Rated Blitz game": {
					"percentage_won": 0.0,
					"percentage_lost": 100.0,
					"percentage_drawn": 0.0,
					"won_games": 0,
					"lost_games": 1,
					"drawn_games": 0
				}
			}
		},
		"A02": {
			"percentage_won": 0.0,
			"percentage_lost": 100.0,
			"percentage_drawn": 0.0,
			"won_games": 0,
			"lost_games": 1,
			"drawn_games": 0,
			"events": {
				"Rated Blitz game": {
					"percentage_won": 0.0,
					"percentage_lost": 100.0,
					"percentage_drawn": 0.0,
					"won_games": 0,
					"lost_games": 1,
					"drawn_games": 0
				}
			}
		},
		"C62": {
			"percentage_won": 42.86,
			"percentage_lost": 57.14,
			"percentage_drawn": 0.0,
			"won_games": 3,
			"lost_games": 4,
			"drawn_games": 0,
			"events": {
				"Rated Classical game": {
					"percentage_won": 50.0,
					"percentage_lost": 50.0,
					"percentage_drawn": 0.0,
					"won_games": 1,
					"lost_games": 1,
					"drawn_games": 0
				},
				"Rated Blitz game": {
					"percentage_won": 25.0,
					"percentage_lost": 75.0,
					"percentage_drawn": 0.0,
					"won_games": 1,
					"lost_games": 3,
					"drawn_games": 0
				},
				"Rated Blitz tournament": {
					"percentage_won": 100.0,
					"percentage_lost": 0.0,
					"percentage_drawn": 0.0,
					"won_games": 1,
					"lost_games": 0,
					"drawn_games": 0
				}
			}
		},
		"B08": {
			"percentage_won": 0.0,
			"percentage_lost": 100.0,
			"percentage_drawn": 0.0,
			"won_games": 0,
			"lost_games": 1,
			"drawn_games": 0,
			"events": {
				"Rated Blitz game": {
					"percentage_won": 0.0,
					"percentage_lost": 100.0,
					"percentage_drawn": 0.0,
					"won_games": 0,
					"lost_games": 1,
					"drawn_games": 0
				}
			}
		},
		"C69": {
			"percentage_won": 0.0,
			"percentage_lost": 100.0,
			"percentage_drawn": 0.0,
			"won_games": 0,
			"lost_games": 1,
			"drawn_games": 0,
			"events": {
				"Rated Blitz game": {
					"percentage_won": 0.0,
					"percentage_lost": 100.0,
					"percentage_drawn": 0.0,
					"won_games": 0,
					"lost_games": 1,
					"drawn_games": 0
				}
			}
		},
		"A10": {
			"percentage_won": 33.33,
			"percentage_lost": 66.67,
			"percentage_drawn": 0.0,
			"won_games": 1,
			"lost_games": 2,
			"drawn_games": 0,
			"events": {
				"Rated Blitz game": {
					"percentage_won": 33.33,
					"percentage_lost": 66.67,
					"percentage_drawn": 0.0,
					"won_games": 1,
					"lost_games": 2,
					"drawn_games": 0
				}
			}
		},
		"E24": {
			"percentage_won": 100.0,
			"percentage_lost": 0.0,
			"percentage_drawn": 0.0,
			"won_games": 1,
			"lost_games": 0,
			"drawn_games": 0,
			"events": {
				"Rated Classical game": {
					"percentage_won": 100.0,
					"percentage_lost": 0.0,
					"percentage_drawn": 0.0,
					"won_games": 1,
					"lost_games": 0,
					"drawn_games": 0
				}
			}
		},
		"B50": {
			"percentage_won": 87.5,
			"percentage_lost": 12.5,
			"percentage_drawn": 0.0,
			"won_games": 7,
			"lost_games": 1,
			"drawn_games": 0,
			"events": {
				"Rated Classical game": {
					"percentage_won": 66.67,
					"percentage_lost": 33.33,
					"percentage_drawn": 0.0,
					"won_games": 2,
					"lost_games": 1,
					"drawn_games": 0
				},
				"Rated Blitz game": {
					"percentage_won": 100.0,
					"percentage_lost": 0.0,
					"percentage_drawn": 0.0,
					"won_games": 5,
					"lost_games": 0,
					"drawn_games": 0
				}
			}
		},
		"B07": {
			"percentage_won": 33.33,
			"percentage_lost": 66.67,
			"percentage_drawn": 0.0,
			"won_games": 1,
			"lost_games": 2,
			"drawn_games": 0,
			"events": {
				"Rated Blitz game": {
					"percentage_won": 33.33,
					"percentage_lost": 66.67,
					"percentage_drawn": 0.0,
					"won_games": 1,
					"lost_games": 2,
					"drawn_games": 0
				}
			}
		},
		"A46": {
			"percentage_won": 0.0,
			"percentage_lost": 100.0,
			"percentage_drawn": 0.0,
			"won_games": 0,
			"lost_games": 2,
			"drawn_games": 0,
			"events": {
				"Rated Blitz game": {
					"percentage_won": 0.0,
					"percentage_lost": 100.0,
					"percentage_drawn": 0.0,
					"won_games": 0,
					"lost_games": 2,
					"drawn_games": 0
				}
			}
		},
		"B32": {
			"percentage_won": 0.0,
			"percentage_lost": 100.0,
			"percentage_drawn": 0.0,
			"won_games": 0,
			"lost_games": 2,
			"drawn_games": 0,
			"events": {
				"Rated Classical game": {
					"percentage_won": 0.0,
					"percentage_lost": 100.0,
					"percentage_drawn": 0.0,
					"won_games": 0,
					"lost_games": 1,
					"drawn_games": 0
				},
				"Rated Blitz game": {
					"percentage_won": 0.0,
					"percentage_lost": 100.0,
					"percentage_drawn": 0.0,
					"won_games": 0,
					"lost_games": 1,
					"drawn_games": 0
				}
			}
		},
		"A05": {
			"percentage_won": 0.0,
			"percentage_lost": 100.0,
			"percentage_drawn": 0.0,
			"won_games": 0,
			"lost_games": 1,
			"drawn_games": 0,
			"events": {
				"Rated Classical game": {
					"percentage_won": 0.0,
					"percentage_lost": 100.0,
					"percentage_drawn": 0.0,
					"won_games": 0,
					"lost_games": 1,
					"drawn_games": 0
				}
			}
		},
		"A03": {
			"percentage_won": 100.0,
			"percentage_lost": 0.0,
			"percentage_drawn": 0.0,
			"won_games": 1,
			"lost_games": 0,
			"drawn_games": 0,
			"events": {
				"Rated Classical game": {
					"percentage_won": 100.0,
					"percentage_lost": 0.0,
					"percentage_drawn": 0.0,
					"won_games": 1,
					"lost_games": 0,
					"drawn_games": 0
				}
			}
		},
		"B54": {
			"percentage_won": 50.0,
			"percentage_lost": 50.0,
			"percentage_drawn": 0.0,
			"won_games": 1,
			"lost_games": 1,
			"drawn_games": 0,
			"events": {
				"Rated Classical game": {
					"percentage_won": 100.0,
					"percentage_lost": 0.0,
					"percentage_drawn": 0.0,
					"won_games": 1,
					"lost_games": 0,
					"drawn_games": 0
				},
				"Rated Blitz game": {
					"percentage_won": 0.0,
					"percentage_lost": 100.0,
					"percentage_drawn": 0.0,
					"won_games": 0,
					"lost_games": 1,
					"drawn_games": 0
				}
			}
		},
		"B13": {
			"percentage_won": 0.0,
			"percentage_lost": 100.0,
			"percentage_drawn": 0.0,
			"won_games": 0,
			"lost_games": 1,
			"drawn_games": 0,
			"events": {
				"Rated Classical game": {
					"percentage_won": 0.0,
					"percentage_lost": 100.0,
					"percentage_drawn": 0.0,
					"won_games": 0,
					"lost_games": 1,
					"drawn_games": 0
				}
			}
		},
		"B52": {
			"percentage_won": 50.0,
			"percentage_lost": 50.0,
			"percentage_drawn": 0.0,
			"won_games": 2,
			"lost_games": 2,
			"drawn_games": 0,
			"events": {
				"Rated Classical game": {
					"percentage_won": 0.0,
					"percentage_lost": 100.0,
					"percentage_drawn": 0.0,
					"won_games": 0,
					"lost_games": 1,
					"drawn_games": 0
				},
				"Rated Blitz game": {
					"percentage_won": 66.67,
					"percentage_lost": 33.33,
					"percentage_drawn": 0.0,
					"won_games": 2,
					"lost_games": 1,
					"drawn_games": 0
				}
			}
		},
		"A48": {
			"percentage_won": 0.0,
			"percentage_lost": 100.0,
			"percentage_drawn": 0.0,
			"won_games": 0,
			"lost_games": 1,
			"drawn_games": 0,
			"events": {
				"Rated Classical game": {
					"percentage_won": 0.0,
					"percentage_lost": 100.0,
					"percentage_drawn": 0.0,
					"won_games": 0,
					"lost_games": 1,
					"drawn_games": 0
				}
			}
		},
		"B92": {
			"percentage_won": 100.0,
			"percentage_lost": 0.0,
			"percentage_drawn": 0.0,
			"won_games": 1,
			"lost_games": 0,
			"drawn_games": 0,
			"events": {
				"Rated Classical game": {
					"percentage_won": 100.0,
					"percentage_lost": 0.0,
					"percentage_drawn": 0.0,
					"won_games": 1,
					"lost_games": 0,
					"drawn_games": 0
				}
			}
		},
		"E21": {
			"percentage_won": 0.0,
			"percentage_lost": 0.0,
			"percentage_drawn": 100.0,
			"won_games": 0,
			"lost_games": 0,
			"drawn_games": 1,
			"events": {
				"Rated Classical game": {
					"percentage_won": 0.0,
					"percentage_lost": 0.0,
					"percentage_drawn": 100.0,
					"won_games": 0,
					"lost_games": 0,
					"drawn_games": 1
				}
			}
		},
		"E00": {
			"percentage_won": 0.0,
			"percentage_lost": 100.0,
			"percentage_drawn": 0.0,
			"won_games": 0,
			"lost_games": 1,
			"drawn_games": 0,
			"events": {
				"Rated Classical game": {
					"percentage_won": 0.0,
					"percentage_lost": 100.0,
					"percentage_drawn": 0.0,
					"won_games": 0,
					"lost_games": 1,
					"drawn_games": 0
				}
			}
		},
		"B90": {
			"percentage_won": 100.0,
			"percentage_lost": 0.0,
			"percentage_drawn": 0.0,
			"won_games": 1,
			"lost_games": 0,
			"drawn_games": 0,
			"events": {
				"Rated Classical game": {
					"percentage_won": 100.0,
					"percentage_lost": 0.0,
					"percentage_drawn": 0.0,
					"won_games": 1,
					"lost_games": 0,
					"drawn_games": 0
				}
			}
		},
		"B22": {
			"percentage_won": 0.0,
			"percentage_lost": 100.0,
			"percentage_drawn": 0.0,
			"won_games": 0,
			"lost_games": 1,
			"drawn_games": 0,
			"events": {
				"Rated Classical game": {
					"percentage_won": 0.0,
					"percentage_lost": 100.0,
					"percentage_drawn": 0.0,
					"won_games": 0,
					"lost_games": 1,
					"drawn_games": 0
				}
			}
		},
		"B33": {
			"percentage_won": 0.0,
			"percentage_lost": 100.0,
			"percentage_drawn": 0.0,
			"won_games": 0,
			"lost_games": 1,
			"drawn_games": 0,
			"events": {
				"Rated Blitz game": {
					"percentage_won": 0.0,
					"percentage_lost": 100.0,
					"percentage_drawn": 0.0,
					"won_games": 0,
					"lost_games": 1,
					"drawn_games": 0
				}
			}
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
  * **eco** : (optional) which ecos to find stats on, otherwise all of your ecos are used
  
  #### Response
  Headers
  ```
  Content-Type: application/json
  ```
  
<details>
  <summary>Body</summary>
  
  ```json
	{
		"A01": {
			"your wins": 18,
			"other players wins": 118,
			"your losses": 12,
			"other players losses": 127,
			"your draws": 0,
			"other players draws": 14,
			"your win percentages": 60.0,
			"other players win percentages": 45.56,
			"your loss percentages": 40.0,
			"other players loss percentages": 49.03,
			"your draw percentages": 0.0,
			"other players draw percentages": 5.41
		},
		"A00": {
			"your wins": 50,
			"other players wins": 849,
			"your losses": 42,
			"other players losses": 1033,
			"your draws": 1,
			"other players draws": 43,
			"your win percentages": 53.76,
			"other players win percentages": 44.1,
			"your loss percentages": 45.16,
			"other players loss percentages": 53.66,
			"your draw percentages": 1.08,
			"other players draw percentages": 2.23
		},
		"C00": {
			"your wins": 10,
			"other players wins": 553,
			"your losses": 11,
			"other players losses": 750,
			"your draws": 0,
			"other players draws": 32,
			"your win percentages": 47.62,
			"other players win percentages": 41.42,
			"your loss percentages": 52.38,
			"other players loss percentages": 56.18,
			"your draw percentages": 0.0,
			"other players draw percentages": 2.4
		},
		"B01": {
			"your wins": 4,
			"other players wins": 546,
			"your losses": 2,
			"other players losses": 571,
			"your draws": 0,
			"other players draws": 38,
			"your win percentages": 66.67,
			"other players win percentages": 47.27,
			"your loss percentages": 33.33,
			"other players loss percentages": 49.44,
			"your draw percentages": 0.0,
			"other players draw percentages": 3.29
		},
		"A40": {
			"your wins": 8,
			"other players wins": 663,
			"your losses": 14,
			"other players losses": 921,
			"your draws": 0,
			"other players draws": 39,
			"your win percentages": 36.36,
			"other players win percentages": 40.85,
			"your loss percentages": 63.64,
			"other players loss percentages": 56.75,
			"your draw percentages": 0.0,
			"other players draw percentages": 2.4
		},
		"C20": {
			"your wins": 1,
			"other players wins": 718,
			"your losses": 2,
			"other players losses": 924,
			"your draws": 1,
			"other players draws": 56,
			"your win percentages": 25.0,
			"other players win percentages": 42.29,
			"your loss percentages": 50.0,
			"other players loss percentages": 54.42,
			"your draw percentages": 25.0,
			"other players draw percentages": 3.3
		},
		"D00": {
			"your wins": 1,
			"other players wins": 717,
			"your losses": 6,
			"other players losses": 968,
			"your draws": 0,
			"other players draws": 51,
			"your win percentages": 14.29,
			"other players win percentages": 41.3,
			"your loss percentages": 85.71,
			"other players loss percentages": 55.76,
			"your draw percentages": 0.0,
			"other players draw percentages": 2.94
		},
		"A04": {
			"your wins": 4,
			"other players wins": 210,
			"your losses": 0,
			"other players losses": 224,
			"your draws": 0,
			"other players draws": 7,
			"your win percentages": 100.0,
			"other players win percentages": 47.62,
			"your loss percentages": 0.0,
			"other players loss percentages": 50.79,
			"your draw percentages": 0.0,
			"other players draw percentages": 1.59
		},
		"A45": {
			"your wins": 1,
			"other players wins": 150,
			"your losses": 0,
			"other players losses": 178,
			"your draws": 0,
			"other players draws": 6,
			"your win percentages": 100.0,
			"other players win percentages": 44.91,
			"your loss percentages": 0.0,
			"other players loss percentages": 53.29,
			"your draw percentages": 0.0,
			"other players draw percentages": 1.8
		},
		"B02": {
			"your wins": 3,
			"other players wins": 89,
			"your losses": 0,
			"other players losses": 122,
			"your draws": 0,
			"other players draws": 4,
			"your win percentages": 100.0,
			"other players win percentages": 41.4,
			"your loss percentages": 0.0,
			"other players loss percentages": 56.74,
			"your draw percentages": 0.0,
			"other players draw percentages": 1.86
		},
		"B03": {
			"your wins": 1,
			"other players wins": 11,
			"your losses": 0,
			"other players losses": 3,
			"your draws": 0,
			"other players draws": 1,
			"your win percentages": 100.0,
			"other players win percentages": 73.33,
			"your loss percentages": 0.0,
			"other players loss percentages": 20.0,
			"your draw percentages": 0.0,
			"other players draw percentages": 6.67
		},
		"A15": {
			"your wins": 1,
			"other players wins": 8,
			"your losses": 0,
			"other players losses": 16,
			"your draws": 0,
			"other players draws": 0,
			"your win percentages": 100.0,
			"other players win percentages": 33.33,
			"your loss percentages": 0.0,
			"other players loss percentages": 66.67,
			"your draw percentages": 0.0,
			"other players draw percentages": 0.0
		},
		"A41": {
			"your wins": 1,
			"other players wins": 75,
			"your losses": 2,
			"other players losses": 112,
			"your draws": 0,
			"other players draws": 4,
			"your win percentages": 33.33,
			"other players win percentages": 39.27,
			"your loss percentages": 66.67,
			"other players loss percentages": 58.64,
			"your draw percentages": 0.0,
			"other players draw percentages": 2.09
		},
		"B06": {
			"your wins": 0,
			"other players wins": 262,
			"your losses": 1,
			"other players losses": 282,
			"your draws": 0,
			"other players draws": 19,
			"your win percentages": 0.0,
			"other players win percentages": 46.54,
			"your loss percentages": 100.0,
			"other players loss percentages": 50.09,
			"your draw percentages": 0.0,
			"other players draw percentages": 3.37
		},
		"B20": {
			"your wins": 2,
			"other players wins": 422,
			"your losses": 1,
			"other players losses": 422,
			"your draws": 0,
			"other players draws": 28,
			"your win percentages": 66.67,
			"other players win percentages": 48.39,
			"your loss percentages": 33.33,
			"other players loss percentages": 48.39,
			"your draw percentages": 0.0,
			"other players draw percentages": 3.21
		},
		"A80": {
			"your wins": 0,
			"other players wins": 12,
			"your losses": 1,
			"other players losses": 26,
			"your draws": 0,
			"other players draws": 1,
			"your win percentages": 0.0,
			"other players win percentages": 30.77,
			"your loss percentages": 100.0,
			"other players loss percentages": 66.67,
			"your draw percentages": 0.0,
			"other players draw percentages": 2.56
		},
		"A02": {
			"your wins": 2,
			"other players wins": 58,
			"your losses": 4,
			"other players losses": 56,
			"your draws": 0,
			"other players draws": 4,
			"your win percentages": 33.33,
			"other players win percentages": 49.15,
			"your loss percentages": 66.67,
			"other players loss percentages": 47.46,
			"your draw percentages": 0.0,
			"other players draw percentages": 3.39
		},
		"A43": {
			"your wins": 4,
			"other players wins": 125,
			"your losses": 1,
			"other players losses": 121,
			"your draws": 1,
			"other players draws": 9,
			"your win percentages": 66.67,
			"other players win percentages": 49.02,
			"your loss percentages": 16.67,
			"other players loss percentages": 47.45,
			"your draw percentages": 16.67,
			"other players draw percentages": 3.53
		},
		"B12": {
			"your wins": 0,
			"other players wins": 53,
			"your losses": 1,
			"other players losses": 62,
			"your draws": 0,
			"other players draws": 3,
			"your win percentages": 0.0,
			"other players win percentages": 44.92,
			"your loss percentages": 100.0,
			"other players loss percentages": 52.54,
			"your draw percentages": 0.0,
			"other players draw percentages": 2.54
		},
		"B00": {
			"your wins": 4,
			"other players wins": 537,
			"your losses": 3,
			"other players losses": 699,
			"your draws": 0,
			"other players draws": 41,
			"your win percentages": 57.14,
			"other players win percentages": 42.05,
			"your loss percentages": 42.86,
			"other players loss percentages": 54.74,
			"your draw percentages": 0.0,
			"other players draw percentages": 3.21
		},
		"C40": {
			"your wins": 1,
			"other players wins": 247,
			"your losses": 1,
			"other players losses": 362,
			"your draws": 0,
			"other players draws": 19,
			"your win percentages": 50.0,
			"other players win percentages": 39.33,
			"your loss percentages": 50.0,
			"other players loss percentages": 57.64,
			"your draw percentages": 0.0,
			"other players draw percentages": 3.03
		},
		"C02": {
			"your wins": 0,
			"other players wins": 71,
			"your losses": 1,
			"other players losses": 85,
			"your draws": 0,
			"other players draws": 5,
			"your win percentages": 0.0,
			"other players win percentages": 44.1,
			"your loss percentages": 100.0,
			"other players loss percentages": 52.8,
			"your draw percentages": 0.0,
			"other players draw percentages": 3.11
		},
		"B10": {
			"your wins": 0,
			"other players wins": 118,
			"your losses": 2,
			"other players losses": 198,
			"your draws": 0,
			"other players draws": 5,
			"your win percentages": 0.0,
			"other players win percentages": 36.76,
			"your loss percentages": 100.0,
			"other players loss percentages": 61.68,
			"your draw percentages": 0.0,
			"other players draw percentages": 1.56
		},
		"A10": {
			"your wins": 1,
			"other players wins": 59,
			"your losses": 0,
			"other players losses": 77,
			"your draws": 0,
			"other players draws": 4,
			"your win percentages": 100.0,
			"other players win percentages": 42.14,
			"your loss percentages": 0.0,
			"other players loss percentages": 55.0,
			"your draw percentages": 0.0,
			"other players draw percentages": 2.86
		},
		"B21": {
			"your wins": 0,
			"other players wins": 133,
			"your losses": 1,
			"other players losses": 166,
			"your draws": 0,
			"other players draws": 4,
			"your win percentages": 0.0,
			"other players win percentages": 43.89,
			"your loss percentages": 100.0,
			"other players loss percentages": 54.79,
			"your draw percentages": 0.0,
			"other players draw percentages": 1.32
		},
		"A03": {
			"your wins": 0,
			"other players wins": 20,
			"your losses": 1,
			"other players losses": 25,
			"your draws": 0,
			"other players draws": 1,
			"your win percentages": 0.0,
			"other players win percentages": 43.48,
			"your loss percentages": 100.0,
			"other players loss percentages": 54.35,
			"your draw percentages": 0.0,
			"other players draw percentages": 2.17
		},
		"C30": {
			"your wins": 0,
			"other players wins": 147,
			"your losses": 1,
			"other players losses": 122,
			"your draws": 0,
			"other players draws": 6,
			"your win percentages": 0.0,
			"other players win percentages": 53.45,
			"your loss percentages": 100.0,
			"other players loss percentages": 44.36,
			"your draw percentages": 0.0,
			"other players draw percentages": 2.18
		}
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
			"percentage_won": 47.54,
			"percentage_lost": 45.9,
			"percentage_drawn": 6.56,
			"won_games": 58,
			"lost_games": 56,
			"drawn_games": 8
		},
		"Time forfeit": {
			"percentage_won": 61.04,
			"percentage_lost": 38.96,
			"percentage_drawn": 0.0,
			"won_games": 47,
			"lost_games": 30,
			"drawn_games": 0
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
		"Time forfeit": {
			"your wins": 18,
			"other players wins": 14084,
			"your win percentage": 75.0,
			"other players win percentage": 49.38,
			"your losses": 6,
			"other players losses": 14116,
			"your loss percentage": 25.0,
			"other players loss percentage": 49.5,
			"your draws": 0,
			"other players draws": 319,
			"your draw percentage": 0.0,
			"other players draw percentage": 1.12
		},
		"Normal": {
			"your wins": 84,
			"other players wins": 30879,
			"your win percentage": 52.17,
			"other players win percentage": 49.27,
			"your losses": 68,
			"other players losses": 29081,
			"your loss percentage": 42.24,
			"other players loss percentage": 46.4,
			"your draws": 9,
			"other players draws": 2710,
			"your draw percentage": 5.59,
			"other players draw percentage": 4.32
		}
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
			"white_wins": 5414,
			"black_wins": 4767,
			"draws": 323,
			"percentage_white_wins": 51.54,
			"percentage_black_wins": 45.38,
			"percentage_draws_wins": 3.08
		},
		"variations": {
			"Reti Opening": {
				"white_wins": 4733,
				"black_wins": 4112,
				"draws": 284,
				"percentage_white_wins": 51.85,
				"percentage_black_wins": 45.04,
				"percentage_draws_wins": 3.11,
				"engine_evaluation": 0.49
			},
			"Reti v Dutch": {
				"white_wins": 114,
				"black_wins": 121,
				"draws": 4,
				"percentage_white_wins": 47.7,
				"percentage_black_wins": 50.63,
				"percentage_draws_wins": 1.67,
				"engine_evaluation": 0.75
			},
			"Reti Pirc-Lisitsin gambit": {
				"white_wins": 11,
				"black_wins": 4,
				"draws": 1,
				"percentage_white_wins": 68.75,
				"percentage_black_wins": 25.0,
				"percentage_draws_wins": 6.25,
				"engine_evaluation": -0.1
			},
			"Reti Lisitsin gambit deferred": {
				"white_wins": 5,
				"black_wins": 2,
				"draws": 0,
				"percentage_white_wins": 71.43,
				"percentage_black_wins": 28.57,
				"percentage_draws_wins": 0.0,
				"engine_evaluation": 0.62
			},
			"Reti Opening 0": {
				"white_wins": 545,
				"black_wins": 521,
				"draws": 33,
				"percentage_white_wins": 49.59,
				"percentage_black_wins": 47.41,
				"percentage_draws_wins": 3.0,
				"engine_evaluation": 0.94
			},
			"Reti Wade defense": {
				"white_wins": 1,
				"black_wins": 5,
				"draws": 1,
				"percentage_white_wins": 14.29,
				"percentage_black_wins": 71.43,
				"percentage_draws_wins": 14.29,
				"engine_evaluation": 1.02
			},
			"Reti Herrstroem gambit": {
				"white_wins": 5,
				"black_wins": 2,
				"draws": 0,
				"percentage_white_wins": 71.43,
				"percentage_black_wins": 28.57,
				"percentage_draws_wins": 0.0,
				"engine_evaluation": 1.98
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
