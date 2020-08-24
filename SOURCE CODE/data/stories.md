## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot

## again
* deny
  - utter_greet

## _start_
* intent_start
  - utter_greet

## path 1 corona tracker
* greet
  - utter_greet
* user_entered_corona_tracker
  - utter_corona_tracker
* corona_state
  - action_corona_tracker
  - utter_goodbye

## path 2 bigman salon
* greet
  - utter_greet
* user_entered_services
  - utter_services_partner
* user_choose_bigmansalon
  -utter_big_man_salon_greet
* user_BMS_book_slot
  - utter_bms_chose_gender
* user_bms_choose_gender
  - action_BMS_display_menu
* user_bms_chose_items
  - utter_ask_mail_id
* user_entered_mail_id
  - action_bms_order_recieved
  - utter_big_man_salon_bye

## path 3 netmeds
* user_choose_netmeds
  - utter_netmeds_greet
* user_NM_order
  - utter_nm_chose_category
* user_nm_choose_category
  - action_NM_display_menu
* user_nm_chose_items
  - utter_ask_mail_id
* user_entered_mail_id
  - action_nm_order_recieved
  - utter_nm_bye