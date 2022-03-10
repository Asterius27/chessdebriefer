# Chess Debriefer

A backend that parses and analyses pgn files

## Endpoints
<details>
  <summary> 
  ## GET /:name/percentages
  
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
			"percentage_won": 58.75,
			"percentage_lost": 41.25,
			"percentage_drawn": 0.0,
			"won_games": 47,
			"lost_games": 33,
			"drawn_games": 0
		},
		"Side percentages": {
			"White": {
				"percentage_won": 63.24,
				"percentage_lost": 36.76,
				"percentage_drawn": 0.0,
				"won_games": 43,
				"lost_games": 25,
				"drawn_games": 0
			},
			"Black": {
				"percentage_won": 33.33,
				"percentage_lost": 66.67,
				"percentage_drawn": 0.0,
				"won_games": 4,
				"lost_games": 8,
				"drawn_games": 0
			}
		},
		"Event percentages": {
			"Rated Bullet game": {
				"percentage_won": 61.04,
				"percentage_lost": 38.96,
				"percentage_drawn": 0.0,
				"won_games": 47,
				"lost_games": 30,
				"drawn_games": 0
			},
			"Rated Blitz game": {
				"percentage_won": 0.0,
				"percentage_lost": 100.0,
				"percentage_drawn": 0.0,
				"won_games": 0,
				"lost_games": 3,
				"drawn_games": 0
			}
		},
		"Opening percentages": {
			"Nimzo-Larsen Attack": {
				"percentage_won": 45.45,
				"percentage_lost": 54.55,
				"percentage_drawn": 0.0,
				"won_games": 5,
				"lost_games": 6,
				"drawn_games": 0,
				"event": {
					"Rated Bullet game": {
						"percentage_won": 45.45,
						"percentage_lost": 54.55,
						"percentage_drawn": 0.0,
						"won_games": 5,
						"lost_games": 6,
						"drawn_games": 0
					}
				}
			},
			"Queen's Pawn Game #2": {
				"percentage_won": 100.0,
				"percentage_lost": 0.0,
				"percentage_drawn": 0.0,
				"won_games": 1,
				"lost_games": 0,
				"drawn_games": 0,
				"event": {
					"Rated Bullet game": {
						"percentage_won": 100.0,
						"percentage_lost": 0.0,
						"percentage_drawn": 0.0,
						"won_games": 1,
						"lost_games": 0,
						"drawn_games": 0
					}
				}
			},
			"Sicilian Defense": {
				"percentage_won": 100.0,
				"percentage_lost": 0.0,
				"percentage_drawn": 0.0,
				"won_games": 1,
				"lost_games": 0,
				"drawn_games": 0,
				"event": {
					"Rated Bullet game": {
						"percentage_won": 100.0,
						"percentage_lost": 0.0,
						"percentage_drawn": 0.0,
						"won_games": 1,
						"lost_games": 0,
						"drawn_games": 0
					}
				}
			},
			"Van't Kruijs Opening": {
				"percentage_won": 33.33,
				"percentage_lost": 66.67,
				"percentage_drawn": 0.0,
				"won_games": 1,
				"lost_games": 2,
				"drawn_games": 0,
				"event": {
					"Rated Bullet game": {
						"percentage_won": 33.33,
						"percentage_lost": 66.67,
						"percentage_drawn": 0.0,
						"won_games": 1,
						"lost_games": 2,
						"drawn_games": 0
					}
				}
			},
			"French Defense: La Bourdonnais Variation": {
				"percentage_won": 0.0,
				"percentage_lost": 100.0,
				"percentage_drawn": 0.0,
				"won_games": 0,
				"lost_games": 1,
				"drawn_games": 0,
				"event": {
					"Rated Bullet game": {
						"percentage_won": 0.0,
						"percentage_lost": 100.0,
						"percentage_drawn": 0.0,
						"won_games": 0,
						"lost_games": 1,
						"drawn_games": 0
					}
				}
			},
			"Scandinavian Defense: Mieses-Kotroc Variation": {
				"percentage_won": 100.0,
				"percentage_lost": 0.0,
				"percentage_drawn": 0.0,
				"won_games": 2,
				"lost_games": 0,
				"drawn_games": 0,
				"event": {
					"Rated Bullet game": {
						"percentage_won": 100.0,
						"percentage_lost": 0.0,
						"percentage_drawn": 0.0,
						"won_games": 2,
						"lost_games": 0,
						"drawn_games": 0
					}
				}
			},
			"Hungarian Opening": {
				"percentage_won": 100.0,
				"percentage_lost": 0.0,
				"percentage_drawn": 0.0,
				"won_games": 6,
				"lost_games": 0,
				"drawn_games": 0,
				"event": {
					"Rated Bullet game": {
						"percentage_won": 100.0,
						"percentage_lost": 0.0,
						"percentage_drawn": 0.0,
						"won_games": 6,
						"lost_games": 0,
						"drawn_games": 0
					}
				}
			},
			"Nimzo-Larsen Attack: Classical Variation": {
				"percentage_won": 100.0,
				"percentage_lost": 0.0,
				"percentage_drawn": 0.0,
				"won_games": 2,
				"lost_games": 0,
				"drawn_games": 0,
				"event": {
					"Rated Bullet game": {
						"percentage_won": 100.0,
						"percentage_lost": 0.0,
						"percentage_drawn": 0.0,
						"won_games": 2,
						"lost_games": 0,
						"drawn_games": 0
					}
				}
			},
			"Old Indian Defense": {
				"percentage_won": 0.0,
				"percentage_lost": 100.0,
				"percentage_drawn": 0.0,
				"won_games": 0,
				"lost_games": 1,
				"drawn_games": 0,
				"event": {
					"Rated Bullet game": {
						"percentage_won": 0.0,
						"percentage_lost": 100.0,
						"percentage_drawn": 0.0,
						"won_games": 0,
						"lost_games": 1,
						"drawn_games": 0
					}
				}
			},
			"King's Pawn Game: Leonardis Variation": {
				"percentage_won": 0.0,
				"percentage_lost": 100.0,
				"percentage_drawn": 0.0,
				"won_games": 0,
				"lost_games": 1,
				"drawn_games": 0,
				"event": {
					"Rated Bullet game": {
						"percentage_won": 0.0,
						"percentage_lost": 100.0,
						"percentage_drawn": 0.0,
						"won_games": 0,
						"lost_games": 1,
						"drawn_games": 0
					}
				}
			},
			"Hungarian Opening: Reversed Modern Defense": {
				"percentage_won": 0.0,
				"percentage_lost": 100.0,
				"percentage_drawn": 0.0,
				"won_games": 0,
				"lost_games": 2,
				"drawn_games": 0,
				"event": {
					"Rated Bullet game": {
						"percentage_won": 0.0,
						"percentage_lost": 100.0,
						"percentage_drawn": 0.0,
						"won_games": 0,
						"lost_games": 2,
						"drawn_games": 0
					}
				}
			},
			"Hungarian Opening: Catalan Formation": {
				"percentage_won": 25.0,
				"percentage_lost": 75.0,
				"percentage_drawn": 0.0,
				"won_games": 1,
				"lost_games": 3,
				"drawn_games": 0,
				"event": {
					"Rated Bullet game": {
						"percentage_won": 25.0,
						"percentage_lost": 75.0,
						"percentage_drawn": 0.0,
						"won_games": 1,
						"lost_games": 3,
						"drawn_games": 0
					}
				}
			},
			"Queen's Gambit Declined: Queen's Knight Variation": {
				"percentage_won": 0.0,
				"percentage_lost": 100.0,
				"percentage_drawn": 0.0,
				"won_games": 0,
				"lost_games": 1,
				"drawn_games": 0,
				"event": {
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
			"French Defense: Knight Variation": {
				"percentage_won": 0.0,
				"percentage_lost": 100.0,
				"percentage_drawn": 0.0,
				"won_games": 0,
				"lost_games": 1,
				"drawn_games": 0,
				"event": {
					"Rated Bullet game": {
						"percentage_won": 0.0,
						"percentage_lost": 100.0,
						"percentage_drawn": 0.0,
						"won_games": 0,
						"lost_games": 1,
						"drawn_games": 0
					}
				}
			},
			"Modern Defense": {
				"percentage_won": 0.0,
				"percentage_lost": 100.0,
				"percentage_drawn": 0.0,
				"won_games": 0,
				"lost_games": 3,
				"drawn_games": 0,
				"event": {
					"Rated Bullet game": {
						"percentage_won": 0.0,
						"percentage_lost": 100.0,
						"percentage_drawn": 0.0,
						"won_games": 0,
						"lost_games": 3,
						"drawn_games": 0
					}
				}
			},
			"Queen's Pawn Game #3": {
				"percentage_won": 0.0,
				"percentage_lost": 100.0,
				"percentage_drawn": 0.0,
				"won_games": 0,
				"lost_games": 1,
				"drawn_games": 0,
				"event": {
					"Rated Bullet game": {
						"percentage_won": 0.0,
						"percentage_lost": 100.0,
						"percentage_drawn": 0.0,
						"won_games": 0,
						"lost_games": 1,
						"drawn_games": 0
					}
				}
			},
			"King's Pawn Game: Macleod Attack": {
				"percentage_won": 0.0,
				"percentage_lost": 100.0,
				"percentage_drawn": 0.0,
				"won_games": 0,
				"lost_games": 1,
				"drawn_games": 0,
				"event": {
					"Rated Bullet game": {
						"percentage_won": 0.0,
						"percentage_lost": 100.0,
						"percentage_drawn": 0.0,
						"won_games": 0,
						"lost_games": 1,
						"drawn_games": 0
					}
				}
			},
			"Alekhine Defense: Maroczy Variation": {
				"percentage_won": 100.0,
				"percentage_lost": 0.0,
				"percentage_drawn": 0.0,
				"won_games": 1,
				"lost_games": 0,
				"drawn_games": 0,
				"event": {
					"Rated Bullet game": {
						"percentage_won": 100.0,
						"percentage_lost": 0.0,
						"percentage_drawn": 0.0,
						"won_games": 1,
						"lost_games": 0,
						"drawn_games": 0
					}
				}
			},
			"Horwitz Defense": {
				"percentage_won": 66.67,
				"percentage_lost": 33.33,
				"percentage_drawn": 0.0,
				"won_games": 2,
				"lost_games": 1,
				"drawn_games": 0,
				"event": {
					"Rated Bullet game": {
						"percentage_won": 100.0,
						"percentage_lost": 0.0,
						"percentage_drawn": 0.0,
						"won_games": 2,
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
			"Queen's Pawn": {
				"percentage_won": 0.0,
				"percentage_lost": 100.0,
				"percentage_drawn": 0.0,
				"won_games": 0,
				"lost_games": 2,
				"drawn_games": 0,
				"event": {
					"Rated Bullet game": {
						"percentage_won": 0.0,
						"percentage_lost": 100.0,
						"percentage_drawn": 0.0,
						"won_games": 0,
						"lost_games": 2,
						"drawn_games": 0
					}
				}
			},
			"French Defense #2": {
				"percentage_won": 100.0,
				"percentage_lost": 0.0,
				"percentage_drawn": 0.0,
				"won_games": 1,
				"lost_games": 0,
				"drawn_games": 0,
				"event": {
					"Rated Bullet game": {
						"percentage_won": 100.0,
						"percentage_lost": 0.0,
						"percentage_drawn": 0.0,
						"won_games": 1,
						"lost_games": 0,
						"drawn_games": 0
					}
				}
			},
			"Indian Game: Pawn Push Variation": {
				"percentage_won": 100.0,
				"percentage_lost": 0.0,
				"percentage_drawn": 0.0,
				"won_games": 1,
				"lost_games": 0,
				"drawn_games": 0,
				"event": {
					"Rated Bullet game": {
						"percentage_won": 100.0,
						"percentage_lost": 0.0,
						"percentage_drawn": 0.0,
						"won_games": 1,
						"lost_games": 0,
						"drawn_games": 0
					}
				}
			},
			"Indian Game: Normal Variation": {
				"percentage_won": 100.0,
				"percentage_lost": 0.0,
				"percentage_drawn": 0.0,
				"won_games": 1,
				"lost_games": 0,
				"drawn_games": 0,
				"event": {
					"Rated Bullet game": {
						"percentage_won": 100.0,
						"percentage_lost": 0.0,
						"percentage_drawn": 0.0,
						"won_games": 1,
						"lost_games": 0,
						"drawn_games": 0
					}
				}
			},
			"Hungarian Opening: Slav Formation": {
				"percentage_won": 0.0,
				"percentage_lost": 100.0,
				"percentage_drawn": 0.0,
				"won_games": 0,
				"lost_games": 1,
				"drawn_games": 0,
				"event": {
					"Rated Bullet game": {
						"percentage_won": 0.0,
						"percentage_lost": 100.0,
						"percentage_drawn": 0.0,
						"won_games": 0,
						"lost_games": 1,
						"drawn_games": 0
					}
				}
			},
			"Saragossa Opening": {
				"percentage_won": 80.0,
				"percentage_lost": 20.0,
				"percentage_drawn": 0.0,
				"won_games": 8,
				"lost_games": 2,
				"drawn_games": 0,
				"event": {
					"Rated Bullet game": {
						"percentage_won": 88.89,
						"percentage_lost": 11.11,
						"percentage_drawn": 0.0,
						"won_games": 8,
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
			"Alekhine Defense #2": {
				"percentage_won": 100.0,
				"percentage_lost": 0.0,
				"percentage_drawn": 0.0,
				"won_games": 1,
				"lost_games": 0,
				"drawn_games": 0,
				"event": {
					"Rated Bullet game": {
						"percentage_won": 100.0,
						"percentage_lost": 0.0,
						"percentage_drawn": 0.0,
						"won_games": 1,
						"lost_games": 0,
						"drawn_games": 0
					}
				}
			},
			"French Defense: Perseus Gambit": {
				"percentage_won": 100.0,
				"percentage_lost": 0.0,
				"percentage_drawn": 0.0,
				"won_games": 1,
				"lost_games": 0,
				"drawn_games": 0,
				"event": {
					"Rated Bullet game": {
						"percentage_won": 100.0,
						"percentage_lost": 0.0,
						"percentage_drawn": 0.0,
						"won_games": 1,
						"lost_games": 0,
						"drawn_games": 0
					}
				}
			},
			"Nimzo-Larsen Attack: Indian Variation": {
				"percentage_won": 100.0,
				"percentage_lost": 0.0,
				"percentage_drawn": 0.0,
				"won_games": 1,
				"lost_games": 0,
				"drawn_games": 0,
				"event": {
					"Rated Bullet game": {
						"percentage_won": 100.0,
						"percentage_lost": 0.0,
						"percentage_drawn": 0.0,
						"won_games": 1,
						"lost_games": 0,
						"drawn_games": 0
					}
				}
			},
			"Grob Opening": {
				"percentage_won": 100.0,
				"percentage_lost": 0.0,
				"percentage_drawn": 0.0,
				"won_games": 1,
				"lost_games": 0,
				"drawn_games": 0,
				"event": {
					"Rated Bullet game": {
						"percentage_won": 100.0,
						"percentage_lost": 0.0,
						"percentage_drawn": 0.0,
						"won_games": 1,
						"lost_games": 0,
						"drawn_games": 0
					}
				}
			},
			"Hungarian Opening: Symmetrical Variation": {
				"percentage_won": 100.0,
				"percentage_lost": 0.0,
				"percentage_drawn": 0.0,
				"won_games": 1,
				"lost_games": 0,
				"drawn_games": 0,
				"event": {
					"Rated Bullet game": {
						"percentage_won": 100.0,
						"percentage_lost": 0.0,
						"percentage_drawn": 0.0,
						"won_games": 1,
						"lost_games": 0,
						"drawn_games": 0
					}
				}
			},
			"Mieses Opening": {
				"percentage_won": 75.0,
				"percentage_lost": 25.0,
				"percentage_drawn": 0.0,
				"won_games": 3,
				"lost_games": 1,
				"drawn_games": 0,
				"event": {
					"Rated Bullet game": {
						"percentage_won": 75.0,
						"percentage_lost": 25.0,
						"percentage_drawn": 0.0,
						"won_games": 3,
						"lost_games": 1,
						"drawn_games": 0
					}
				}
			},
			"Alekhine Defense: Two Pawn Attack, Lasker Variation": {
				"percentage_won": 100.0,
				"percentage_lost": 0.0,
				"percentage_drawn": 0.0,
				"won_games": 2,
				"lost_games": 0,
				"drawn_games": 0,
				"event": {
					"Rated Bullet game": {
						"percentage_won": 100.0,
						"percentage_lost": 0.0,
						"percentage_drawn": 0.0,
						"won_games": 2,
						"lost_games": 0,
						"drawn_games": 0
					}
				}
			},
			"Rat Defense: Small Center Defense": {
				"percentage_won": 100.0,
				"percentage_lost": 0.0,
				"percentage_drawn": 0.0,
				"won_games": 2,
				"lost_games": 0,
				"drawn_games": 0,
				"event": {
					"Rated Bullet game": {
						"percentage_won": 100.0,
						"percentage_lost": 0.0,
						"percentage_drawn": 0.0,
						"won_games": 2,
						"lost_games": 0,
						"drawn_games": 0
					}
				}
			},
			"Modern Defense: Geller's System": {
				"percentage_won": 0.0,
				"percentage_lost": 100.0,
				"percentage_drawn": 0.0,
				"won_games": 0,
				"lost_games": 1,
				"drawn_games": 0,
				"event": {
					"Rated Bullet game": {
						"percentage_won": 0.0,
						"percentage_lost": 100.0,
						"percentage_drawn": 0.0,
						"won_games": 0,
						"lost_games": 1,
						"drawn_games": 0
					}
				}
			},
			"Englund Gambit Complex: Soller Gambit": {
				"percentage_won": 0.0,
				"percentage_lost": 100.0,
				"percentage_drawn": 0.0,
				"won_games": 0,
				"lost_games": 1,
				"drawn_games": 0,
				"event": {
					"Rated Bullet game": {
						"percentage_won": 0.0,
						"percentage_lost": 100.0,
						"percentage_drawn": 0.0,
						"won_games": 0,
						"lost_games": 1,
						"drawn_games": 0
					}
				}
			},
			"Hungarian Opening: Sicilian Invitation": {
				"percentage_won": 100.0,
				"percentage_lost": 0.0,
				"percentage_drawn": 0.0,
				"won_games": 1,
				"lost_games": 0,
				"drawn_games": 0,
				"event": {
					"Rated Bullet game": {
						"percentage_won": 100.0,
						"percentage_lost": 0.0,
						"percentage_drawn": 0.0,
						"won_games": 1,
						"lost_games": 0,
						"drawn_games": 0
					}
				}
			},
			"Nimzo-Larsen Attack: English Variation": {
				"percentage_won": 50.0,
				"percentage_lost": 50.0,
				"percentage_drawn": 0.0,
				"won_games": 1,
				"lost_games": 1,
				"drawn_games": 0,
				"event": {
					"Rated Bullet game": {
						"percentage_won": 50.0,
						"percentage_lost": 50.0,
						"percentage_drawn": 0.0,
						"won_games": 1,
						"lost_games": 1,
						"drawn_games": 0
					}
				}
			}
		},
		"Termination percentages": {
			"Normal": {
				"percentage_won": 60.61,
				"percentage_lost": 39.39,
				"percentage_drawn": 0.0,
				"won_games": 20,
				"lost_games": 13,
				"drawn_games": 0
			},
			"Time forfeit": {
				"percentage_won": 57.45,
				"percentage_lost": 42.55,
				"percentage_drawn": 0.0,
				"won_games": 27,
				"lost_games": 20,
				"drawn_games": 0
			}
		},
		"Throw comeback percentages": {
			"throws": 10,
			"losses": 33,
			"percentage_throws": 30.3,
			"comebacks": 9,
			"wins": 47,
			"percentage_comebacks": 19.15
		}
	  }
  ```
</details>
	
</details>

<details>
  <summary>GET /:name/accuracy</summary>
  
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
		"Accuracy": 0
	}
  ```
</details>

</details>

<details>
  <summary>POST /upload</summary>
  
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