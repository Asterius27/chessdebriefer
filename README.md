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
  <h3> GET /:name/percentages/openings </h3>
  
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
		"accuracy_percentage": 31.28
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
  
  The pgn file
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
  
  The pgn file
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
