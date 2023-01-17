-- Keep a log of any SQL queries you execute as you solve the mystery.
-- Find out more info about the crime:
select description from crime_scene_reports where month=7 and day=28 and street="Humphrey Street";
-- Time was 10:15am at the bakery, three witnesses, their interviews mention bakery
-- Look at interviews:
select name,month,day,transcript from interviews where transcript like "%bakery%" and month=7;
-- Ruth,Eugene,Raymond.Thief left w/ car within 10 minutes.
-- Thief withrew money that morning at ATM at Leggett Street.
-- Thief made call < 60s. Plan: earliest flight out on 29th.
-- Accomplice purchased ticket.
-- Look at security logs:
select activity,license_plate,hour,minute from bakery_security_logs where year=2021 and month=7 and day=28 and hour=10 and minute<25;
-- Look at phone logs:
select caller,receiver,duration from phone_calls where year=2021 and month=7 and day=28 and duration<60;
-- Look at atm_transactions:
select account_number,amount,transaction_type from atm_transactions where year=2021 and month=7 and day=28 and atm_location="Leggett Street";
-- Find out airport id and look at flights:
select * from airports where city="Fiftyville";
select destination_airport_id from flights where day=29 and month=7 and year=2021 and origin_airport_id="8" order by hour,minute;
-- Desination airport_id = 4. Find out where that is:
select * from airports where id=4;
-- Thief probably flew to LaGuardia Airport in New York City on the 29th
-- Narrow down passport:
select id from flights where day=29 and month=7 and year=2021 and origin_airport_id=8 and destination_airport_id=4 order by hour,minute;
-- Flight ID is 36.
select passport_number, seat from passengers where flight_id=36;
-- Now we know that:
-- The thiefs license plate is in this list:
--      5P2BI95     94KL13X     6P58WS2
--      4328GD8     G412CB7     L93JTIZ
--      322W7Je     0NTHK55
-- His phone number is in this list:
--      (130) 555-0289      (499) 555-9472
--      (367) 555-5533      (499) 555-9472
--      (286) 555-6063      (770) 555-1861
--      (031) 555-6622      (826) 555-1652
--      (338) 555-6650
-- His bank account nmbr is one of these:
--      28500762    28296815    76054385
--      49610011    16153065    86363979
--      25506511    81061156    26013199
-- His passport is in this list:
--  7214083635      1695452385
--  5773159633      1540955065
--  8294398571      1988161715
--  9878712108      8496433585

-- Try get thief with this info:
select name from people
    where phone_number in
     (select caller from phone_calls where year=2021 and month=7 and day=28 and duration<60)
     and license_plate in
     (select license_plate from bakery_security_logs where year=2021 and month=7 and day=28 and hour=10 and minute<25)
     and passport_number in
     (select passport_number from passengers where flight_id=36);
-- Possible thieves: Sofia, Kelsey, Bruce
-- Narrow down further using the account number:
    select name from people where (name="Sofia" or name="Kelsey" or name="Bruce") and id in
    (select person_id from bank_accounts
    where account_number in
    (select account_number from atm_transactions where year=2021 and month=7 and day=28 and atm_location="Leggett Street"));
-- Bruce is the thief!
-- Let's find the accomplice:
select * from people where name="Bruce";
-- phone: (367) 555-5533 | pp: 5773159633 | license: 94KL13X
select * from phone_calls where caller="(367) 555-5533" and day=28 and duration<60;
-- accomplice phone number: (375) 555-8161
select * from people where phone_number="(375) 555-8161";
-- accomplice is Robin!