scene	cue	follow	name	label	tracks	behavior	timestop	timer	soundintro	soundeval	soundround	soundtrack	soundsynth	rendering	colorset	
preparation	0.10	0.15	register	0.10 register	Reset	default	1							0.00		
preparation	0.15	0.20	walkin	0.15 walkin			1							0.00		
preparation	0.20	0.30	field	0.20 field			1							0.20		
preparation	0.30	0.40	boundaries	0.30 boundaries			1							0.20		
preparation	0.40	0.50	entrance	0.40 entrance			1						1 2000	0.20		
preparation	0.50	1.10	black	0.50 black			1							0.50		
prolog	1.10	1.20	beginning	1.10 beginning			1							0.50		
prolog	1.20	1.30	prolog	1.20 prolog			1		prolog					0.50		
prolog	1.30	1.40	boot	1.30 boot			1		boot					0.50		
prolog	1.40	2.10	platforms	1.40 platforms			1						1 2000	1.40		
polls	2.10	2.20	experimentstart	2.10 experimentstart			1		poll					1.40		
polls	2.20	3.05	poll	2.20 poll			1						1 2000	2.20		
association	3.05	3.10	association_intro	3.05 association intro	Initround	default	1		association					3.05		
association	3.10	3.16	association_ruleset	3.10 association ruleset	Startround		0	Goround				01 1 2000	1 2000	3.10		
association	3.16	3.30	association_countdown	3.16 association countdown			0	Gocd			countdown	01 1 2000	1 2000	3.10		
association	3.30	3.40	association_lab	3.30 association lab	Stopround		1	Reinit		1				3.30		
association	3.40	3.41	association_selection1	3.40 association selection 1			1							3.40		
association	3.41	3.42	association_selection1	3.41 association selection 2			1							3.41		
association	3.42	3.43	association_selection1	3.42 association selection 3			1							3.42		
association	3.43	3.44	association_profile1	3.43 association profile 1			1							3.43		
association	3.44	3.45	association_profile2	3.44 association profile 2			1							3.44		
association	3.45	4.00	association_profile3	3.45 association profile 3			1							3.45		
movement	4.00	4.04	movement_load	4.00 movement load	Initround	default	1	Reinit						4.00		
movement	4.04	4.05	movement_splashscreen	4.04 movement splash	Initround	default	1	Reinit						4.04		
movement	4.05	4.10	movement_intro	4.05 movement intro	Initround	default	1	Reinit	movement					4.05		
movement	4.10	4.12	movement_ruleset	4.10 movement ruleset	Startround		0	Goround				02 1 2000		4.10		
movement	4.12	4.14	movement_plateau1	4.12 movement plateau 1			0					02 2 2000		4.10		
movement	4.14	4.16	movement_plateau2	4.14 movement plateau 2			0					02 3 2000		4.10		
movement	4.16	4.30	movement_countdown	4.16 movement countdown		default	0	Gocd			countdown			4.10		
movement	4.20	4.30	movement_conform	4.20 movement conform	Stopround	conform	1				conformbehavior			4.20		
movement	4.25	4.30	movement_rebel	4.25 movement rebel	Stopround	rebel	1				rebelbehavior			4.25		
movement	4.30	4.40	movement_lab	4.30 movement lab	Stopround		1	Reinit		1				4.30		
movement	4.40	4.43	movement_profilegroup	4.40 movement profile group			1							4.40		
movement	4.43	4.44	movement_profilebest	4.43 movement profile best			1							4.43		
movement	4.44	4.45	movement_profileworst	4.44 movement profile worst			1							4.44		
movement	4.45	5.00	movement_profilemiddle	4.45 movement profile middle			1							4.45		
distance	5.00	5.04	distance_load	5.0 distance load	Initround	default	1	Reinit						5.00		
distance	5.04	5.05	distance_splash	5.04 distance splash	Initround	default	1	Reinit						5.04		
distance	5.05	5.10	distance_intro	5.05 distance intro	Initround	default	1	Reinit	distance					5.05		
distance	5.10	5.12	distance_ruleset	5.10 distance ruleset	Startround		0	Goround				03 1 2000		5.10		
distance	5.12	5.14	distance_plateau1	5.12 distance plateau 1			0					03 2 2000		5.10		
distance	5.14	5.16	distance_plateau2	5.14 distance plateau 2			0					03 3 2000		5.10		
distance	5.16	5.30	distance_countdown	5.16 distance countdown		default	0	Gocd			countdown			5.10		
distance	5.20	5.30	distance_conform	5.20 distance conform	Stopround	conform	1				conformbehavior			5.10		
distance	5.25	5.30	distance_rebel	5.25 distance rebel	Stopround	rebel	1				rebelbehavior			5.10		
distance	5.30	5.40	distance_lab	5.30 distance lab	Stopround		1	Reinit		1				5.30		
distance	5.40	5.43	distance_profilegroup	5.40 distance profile group			1							5.40		
distance	5.43	5.44	distance_profilebest	5.43 distance profile best			1							5.43		
distance	5.44	5.45	distance_profileworst	5.44 distance profile worst			1							5.44		
distance	5.45	6.00	distance_profilemiddle	5.45 distance profile middle			1							5.45		
prediction	6.00	6.04	prediction_load	6.00 prediction load	Initround	default	1	Reinit						6.00		
prediction	6.04	6.05	prediction_splash	6.04 prediction splash	Initround	default	1	Reinit						6.04		
prediction	6.05	6.10	prediction_intro	6.05 prediction intro	Initround	default	1		prediction					6.05		
prediction	6.10	6.16	prediction_ruleset	6.10 prediction ruleset	Startround		0	Goround				04 1		6.10		
prediction	6.16	6.30	prediction_countdown	6.16 prediction countdown		default	0	Gocd			countdown			6.10		
prediction	6.20	6.30	prediction_conform	6.20 prediction_conform	Stopround	conform	0				conformbehavior			6.10		
prediction	6.25	6.30	prediction_rebel	6.25 prediction_rebel	Stopround	rebel	1				rebelbehavior			6.10		
prediction	6.30	6.40	prediction_lab	6.30 prediction_lab	Stopround		1			1				6.30		
prediction	6.40	6.43	prediction_groupprofile	6.40 prediction_groupprofile			1							6.40		
prediction	6.43	7.00	prediction_profilebest	6.43 prediction_profilebest			1							6.43		
custom	7.00	7.04	custom_load	7.00 custom_load			1	Reinit						7.00		
custom	7.04	7.05	custom_splash	7.04 custom_splash			1	Reinit						7.04		
custom	7.05	7.10	custom_intro	7.05 custom_intro			1	Reinit	custom					7.04		
custom	7.10	7.11	custom_question_dist	7.10 custom_question_dist			1							7.04		
custom	7.11	7.20	custom_poll_dist	7.11 custom_poll_dist			1							7.11		
custom	7.20	7.21	custom_question_assoc	7.20 custom_question_assoc			1							7.20		
custom	7.21	7.30	custom_poll_assoc	7.21 custom_poll_assoc			1							7.21		
custom	7.30	7.31	custom_question_mov	7.30 custom_question_mov			1							7.30		
custom	7.31	7.40	custom_poll_mov	7.31 custom_poll_mov			1							7.31		
custom	7.40	7.41	custom_question_pred	7.40 custom_question_pred			1							7.40		
custom	7.41	7.50	custom_poll_pred	7.41 custom_poll_pred			1							7.41		
custom	7.50	8.10	custom_reset	7.50 custom_reset			1				reset			7.50		
epilog	8.10	8.20	epilog_black	8.10 epilog_talk			1							8.10		
epilog	8.20	8.20	epilog_black	8.20 epilog_black			1							8.20		
joker	23	23	joker	joker			1									
reset	123	123	reset	reset			1	Reset			reset			7.10		
