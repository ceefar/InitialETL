# InitialETL   
Initial work with sample data on etl pipelines   
  
Documenting very first work with ETL pipeline task, mostly to showcase that I managed to do quite a large amount (and upload to a new repo)   
on the very first day of working on the project/task (Thursday 02 June 2022, the first bank holiday day we have off for the jubilee)   
particularly in terms of insights   
  
Here is a very brief overview off the top of my head of what I have done so far   
Note i have removed some extra fields from the sample data set to test my code for better cleaning,   
I've also altered some dates so calculating things like averages made a lot more sense   
  
  
## EXTRACT
Extracts data and dummifies any missing entries, then fills in any missing entries it can if valid
- e.g. if have a product_id but no product_amount for a user ive created a new ProductPricing db table that
- it checks again and then fills in the price data, this means that before where user 1054 would have been 
- completely ommited from the insights dataset, but now their data is entirely included
  
  
## TRANSFORM
lots of value based insights from the given dataset, mostly (since im just adding lots still)
is outputted to the terminal, with some data saved to individual txt files for each user
these txt files will have different file names depending on if data is parsed from the entire datasets timeline
or from a specific date range. Some data is included in a new CustomerSpendingInsights table, which i will expand on shortly
  
  
## LOAD
initially data is sent to CustomerSalesData_Staging table, and cleaned here before being set to the the final CustomerSalesData table
obviously wasnt entirely necessary but seemed like was the expected thing to do, 
and i guess if there were multiple data sources this would be a necessity
after data is loaded from the staging table to the final table the staging table is wiped
  
  
## PLANS
many plans for expanding the insights in product specific insights, obviously moving my terminal data to txt files and relevant db tables
would like to start work on a super simple dashboard app with this data by the end of the bank holiday weekend using streamlit
would also like to expand and improve the db generally
considering a super simple ml algorithm for predicting revenues but might leave this for now
  
  
## DB TABLES
- CustomerSalesData_Staging
- CustomerSalesData
- CustomerSpendingInsights
- ProductPricing
- **[NEW]** CustomerInsights
- **[NEW]** CustomerInsightsHistorical (for dashboard app)
   
  
## NEW  
**updates for saturday 4th June**  
So some quite major updates already in just a few days, but firstly the technical issues  
i've had a big time issue with windows 11, basically nothing inherent to the os worked (e.g. photos, snipping tool, entire office suite) and i had no startbar   
  
there were workarounds (i.e. using run or navigating to exes in root folders for startbar workaround)  
then decided friday would be a good day to fix things, got up early contacted microsoft support, and THEY BROKE MY LAPTOP WORSE XD  
you honestly cannot make this stuff up, now no taskbar at all, and nothing at all microsoft related works (no settings, no recycle bin, not even files or folders)  
  
the only work around is to do **everything** through the run menu, very sadge, much annoy, but we move on.
i've got them to give me the dl for windows 10, would have reverted already but yet to be given a time to showcase my first project  
which i missed due to surgery and since i'm not confident in spinning the sql server back up i figured ill wait til that's done  
  
ok so with that out of the way, a large refactor and formatting to the original app on friday after raging with microsoft for 2 hours and starting  
file backups (windows 10 install will require wiping my entire system fml), but refactor was very much worth it, then expanded the extract data drastically though i've not included the specifics of the update here, thinking i'll possibly do that on sunday with a new readme.md   
  
today tho has been my favourite day, spent entirely working with streamlit and trying to get a super basic dashboard app up and running,  
was a real pain at the start but after a while got to grips with it and man am i proud of it so far,  
pretty much a basic etl pipeline and basic dashboard app already in 3 days after the first etl tasksheet :D
still an awful lot to do on it tho, but the data included is brought in from either csv files that are saved from the db data,
or are directly accessed from the db itself, so real cool stuff there like inclusion of historical data to show the difference between  
the avg spend kpi for the current set of data, and the previous time the etl pipeline was run, this shows as a difference indicator in
the metric widget which is also coloured (green for growth, red for loss), and also tables showing highlighted missing data fields,  
vs the ones that were cleaned and ones that were improved (function for figuring out what data is missing based on what is available),   
which i think looks super cool too you can see the screenshots of that below and like i said i'll update this readme 
hopefully sunday to show how the transformation data has evolved ive also started doing some minor additions to the data set  
as working with more data really brings this whole thing to life, slowly but steadily mind you.  
  
also to end, an unnecessarily long amount of time figuring out how to format in markdown, totally work it tho as not only does streamlit use markdown  
(which is the python library im using for my current dashboard app) but in all seriousness I'm probably going to need to know how to do this  
eventually so mights as well get it out of the way now lol  
  
actually also have had some issues with pushing to github, but i'll figure that one out eventually, might just be the os issues idk  
  
   
## PERSONAL 
old personal notes on the project and my progress overall have been moved to the end of the document
  
  
## EXAMPLES  
See 5 examples below, **[NEW] Dashboard App**, Terminal, Txt Files, DB peek, SQLcommands  
All from first days work  
(got the task on Weds, today is thurs, only had 3 hours to work during class 10am to 1pm, though i worked throughout my lunch too so 4)  
   
   
## DASHBOARD APP  
*click to enlarge images*  
yes this is supppper basic, but first day working with it, and it is live data from the database or database csvs,  
most of the learning today was just figuring out how to use streamlit and it's widgets  
note files upload via discord but i literally cannot do it another way due to broken af os (ggwp microsoft)  
    
**Dashboard Home**    
<img src="https://cdn.discordapp.com/attachments/981171204008345613/982656327010648094/dashboard_app_home.png" alt="dashboard home - 1" width="500"/>
<img src="https://cdn.discordapp.com/attachments/981171204008345613/982656327862087801/dashboard_app2_home.png" alt="dashboard home - 2" width="500"/>  
   
**Dashboard Insights**    
<img src="https://cdn.discordapp.com/attachments/981171204008345613/982656327245496370/dashboard_app_insights.png" alt="dashboard insights - 1" width="500"/>  
   
**Dashboard Data**    
<img src="https://cdn.discordapp.com/attachments/981171204008345613/982656326775750686/dashboard_app_data1.png" alt="dashboard data - 1" width="500"/>  
  
   
### EXAMPLE 2 [TERMINAL]  
- - + - -  
**EXAMPLE OF TERMINAL PRINT OUT SO FAR**  
*(below output has been trimmed to show only 2 users)*     
  
Local Data Successfully Moved To Staging Table  
Some Items From Local Data Were Dummified Due To Incomplete Data  
Lines -> [3, 6, 25, 27]  
DATE RANGE : ALL  
Unique Customers (by ID) Used In This Data Set  
996  
1054  
2194  
3451  
5632  
7365  
- - + - -  
**CUSTOMER 5632**  
Total Spend : $62.26  
Total Items Purchased : 10  
Average Spend Per Item : $6.23  
Highest Value Item : 853HGZ at $7.75  
Unique Items (list with counts)  
113BCA [x4]  
853HGZ [x3]  
439FS [x3]  
Unique Shopping Days : 6  
Shopping Days As % Of Available Days [38] : 15.8%  
Average Spend Per Unique Shopping Day [6] : $10.38  
Date of First Purchase : 2020-12-01  
Date of Last Purchase : 2020-12-08  
Buying Window (days from first to last purchase) : 8  
Daily Average Spend During Buying Window [8 days] : $7.78  
Highest Spend On A Day : $19.01 on 2020-12-05  
Lowest Spend On A Day : $5.23 on 2020-12-01  
Spend Deviation (diff in high and low spend) : $13.78  
Spend Per Day  
$5.23 on 2020-12-01  
$12.98 on 2020-12-02  
$13.78 on 2020-12-03  
$6.03 on 2020-12-04  
$19.01 on 2020-12-05  
$5.23 on 2020-12-08  
- - + - -  
**CUSTOMER 7365**  
Total Spend : $25.70  
Total Items Purchased : 13  
Average Spend Per Item : $1.98  
Highest Value Item : 915PD at $3.25  
Unique Items (list with counts)  
893GDE [x2]  
384JHG [x2]  
548FH [x1]  
068HQJ [x1]  
475KDU [x1]  
023HRT [x1]  
501KH [x1]  
915PD [x1]  
626OH [x1]  
385HTU [x1]  
951LXU [x1]  
Unique Shopping Days : 6  
Shopping Days As % Of Available Days [38] : 15.8%  
Average Spend Per Unique Shopping Day [6] : $4.28  
Date of First Purchase : 2020-12-01  
Date of Last Purchase : 2020-12-05  
Buying Window (days from first to last purchase) : 5  
Daily Average Spend During Buying Window [5 days] : $5.14  
Highest Spend On A Day : $7.02 on 2020-12-05  
Lowest Spend On A Day : $1.96 on 2000-01-01  
Spend Deviation (diff in high and low spend) : $5.06  
Spend Per Day  
$1.96 on 2000-01-01  
$2.75 on 2020-12-01  
$4.89 on 2020-12-02  
$4.82 on 2020-12-03  
$6.22 on 2020-12-04  
$7.02 on 2020-12-05  
- - + - -    
**COMPLETE**  
- - + - -  
  
  
- - - -

### EXAMPLE 3 [TXT FILES]  

**EXAMPLE OF CUSTOMER TXT FILE SO FAR**  
*(as you can see there is much more data in terminal, but thats just because i'm still adding and creating that data)*  
  
**cust7365_allData.txt**  
  
Data From All Available Dates Included  
CUSTOMER 7365  
Total Spend : $25.70  
Total Items Purchased : 13  
Average Spend : $1.98  
Highest Value Item : 915PD at $3.25  
Unique Items With Amount Purchased  
2x 893GDE  
2x 384JHG  
1x 548FH  
1x 068HQJ  
1x 475KDU  
1x 023HRT  
1x 501KH  
1x 915PD  
1x 626OH  
1x 385HTU  
1x 951LXU  
  
- - - -

### EXAMPLE 4 [DB PEEK]
  
**EXAMPLE OF INSIGHTS DB TABLE**  
*(this has changed drastically already by Saturday 4th, below example (like the majority of the readme) is from Thursday 2nd)*   
  
| customer_id | total_items_purchased | total_spend | avg_spend | highest_indiv_item_spend | highest_indiv_item_id |
|-------------|-----------------------|-------------|-----------|--------------------------|-----------------------|
| 5632        | 10                    | 62.26       | 6.23      | 7.75                     | 853HGZ                |
| 2194        | 4                     | 50.00       | 12.50     | 12.50                    | 667XL                 |
| 7365        | 12                    | 25.40       | 2.12      | 3.25                     | 915PD                 |
| 3451        | 1                     | 9.15        | 9.15      | 9.15                     | 023HRT                |
| 996         | 1                     | 5.23        | 5.23      | 5.23                     | ABCDEF                |
  
- - - -
  
### EXAMPLE 5 [SQL COMMANDS] 
  
feel this gives a good idea of my level of interest in data engineering and showcases my high level of commitment to my learning  
through the timestamps (note I recently had surgery hence why I was up so early (because I tend to go to sleep quite early, between 6 and 9pm)  
  
**History**
Edit **19:02:56** SELECT purchase_date, SUM(purchase_amount) AS TotalCustomerSpend FROM CustomerSa  
Edit 17:56:46 UPDATE `CustomerSalesData` SET `customer_id` = '5632', `purchase_date` = '2020-1??? (0.014 s)  
Edit 17:28:06 SELECT purchase_date FROM CustomerSalesData WHERE customer_id = 7365 AND NOT pur???  
Edit 17:27:48 SELECT purchase_date FROM CustomerSalesData WHERE customer_id = 7365 AND NOT pur???  
Edit 17:27:37 SELECT purchase_date FROM CustomerSalesData WHERE customer_id = 7365 AND purchas???  
Edit 17:27:22 SELECT purchase_date FROM CustomerSalesData WHERE customer_id = 7365 AND purchas???  
Edit 17:27:12 SELECT purchase_date FROM CustomerSalesData WHERE customer_id = 7365 AND NOT pur???  
Edit 17:26:45 SELECT purchase_date FROM CustomerSalesData WHERE customer_id = 7365 GROUP BY pu???  
Edit 17:26:26 SELECT purchase_date FROM CustomerSalesData WHERE customer_id = 7365 GROUP BY pu???  
Edit 17:26:22 SELECT purchase_date AS purchDate FROM CustomerSalesData WHERE customer_id = 736???  
Edit 17:26:15 SELECT purchase_date AS purchDate FROM CustomerSalesData WHERE customer_id = 736???  
Edit 17:26:02 SELECT purchase_date FROM CustomerSalesData WHERE customer_id = 7365 AND  GROUP ???  
Edit 17:25:52 SELECT purchase_date AS TotalCustomerSpend FROM CustomerSalesData WHERE customer???  
Edit 17:25:33 SELECT purchase_date AS TotalCustomerSpend FROM CustomerSalesData WHERE customer???  
Edit 17:25:10 SELECT purchase_date AS TotalCustomerSpend FROM CustomerSalesData WHERE customer???  
Edit 15:28:16 SELECT purchase_date, SUM(purchase_amount) AS TotalCustomerSpend FROM CustomerSa???  
Edit 15:28:07 SELECT purchase_date, SUM(purchase_amount) AS TotalCustomerSpend FROM CustomerSa???  
Edit 15:27:56 SELECT purchase_date, SUM(purchase_amount) AS TotalCustomerSpend FROM CustomerSa???  
Edit 15:27:49 SELECT purchase_date, SUM(purchase_amount) AS TotalCustomerSpend FROM CustomerSa???  
Edit 15:26:14 SELECT purchase_date, SUM(purchase_amount) AS TotalCustomerSpend FROM CustomerSa???  
Edit 15:24:42 SELECT MAX(SUM(purchase_amount)), purchase_date AS TotalCustomerSpend FROM Custo???  
Edit 15:18:02 SELECT product_id, purchase_date AS TotalCustomerSpend FROM CustomerSalesData WH???  
Edit 15:17:39 SELECT SUM(purchase_amount), purchase_date AS TotalCustomerSpend FROM CustomerSa???  
Edit 15:17:22 SELECT SUM(purchase_amount), purchase_date, product_id AS TotalCustomerSpend FRO???  
Edit 15:08:22 SELECT SUM(purchase_amount), purchase_date AS TotalCustomerSpend FROM CustomerSa???  
Edit 15:08:12 SELECT SUM(purchase_amount) AS TotalCustomerSpend FROM CustomerSalesData WHERE c???  
Edit 15:08:02 SELECT SUM(purchase_amount) AS TotalCustomerSpend FROM CustomerSalesData_Staging???  
Edit 15:07:16 SELECT DISTINCT purchase_date, SUM(purchase_amount) AS TotalCustomerSpend FROM C???  
Edit 15:07:05 SELECT DISTINCT purchase_date SUM(purchase_amount) AS TotalCustomerSpend FROM Cu???  
Edit 11:05:40 SELECT DISTINCT customer_id, purchase_date AS unique_purchase_dates FROM Custome???  
Edit 11:05:29 SELECT COUNT (purchase_date) DISTINCT customer_id, purchase_date FROM CustomerSa???  
Edit 11:05:20 SELECT COUNT (purchase_date) DISTINCT customer_id, purchase_date AS unique_purch???  
Edit 11:04:15 SELECT DISTINCT customer_id, purchase_date AS unique_purchase_dates FROM Custome???  
Edit 11:04:07 SELECT (SELECT purchase_date FROM CustomerSalesData) AS unique_purchase_dates, (???  
Edit 11:04:01 SELECT (SELECT DISTINCT purchase_date FROM CustomerSalesData) AS unique_purchase???  
Edit 11:03:56 SELECT (SELECT DISTINCT purchase_date FROM CustomerSalesData) AS unique_purchase???  
Edit 11:03:30 SELECT (SELECT DISTINCT purchase_date FROM CustomerSalesData) AS unique_purchase???  
Edit 11:03:22 SELECT (SELECT DISTINCT customer_id, purchase_date FROM CustomerSalesData) AS un???  
Edit 11:02:07 SELECT DISTINCT customer_id, purchase_date AS unique_purchase_dates FROM Custome???  
Edit 11:01:27 SELECT DISTINCT customer_id, purchase_date SELECT purchase_amount AS unique_purc???  
Edit 11:01:05 SELECT DISTINCT customer_id, purchase_amount, purchase_date AS unique_purchase_d???  
Edit 11:00:44 SELECT DISTINCT customer_id, purchase_date AS unique_purchase_dates FROM Custome???  
Edit 11:00:36 SELECT DISTINCT purchase_date AS unique_purchase_dates FROM CustomerSalesData WH???  
Edit 11:00:30 SELECT purchase_date AS unique_purchase_dates FROM CustomerSalesData WHERE purch???  
Edit 11:00:15 SELECT purchase_date AS unique_purchase_dates FROM CustomerSalesData WHERE purch???  
Edit 11:00:01 SELECT COUNT(*), purchase_date AS unique_purchase_dates FROM CustomerSalesData W???  
Edit 10:59:13 SELECT COUNT(*), purchase_date AS unique_purchase_dates FROM CustomerSalesData W???  
Edit 10:58:52 SELECT COUNT(*), purchase_date AS unique_purchase_dates FROM CustomerSalesData W???  
Edit 10:55:16 SELECT DISTINCT customer_id, purchase_date AS unique_purchase_dates FROM Custome???  
Edit 10:54:40 SELECT DISTINCT customer_id, purchase_date FROM CustomerSalesData WHERE customer???  
Edit 10:54:31 SELECT DISTINCT customer_id, purchase_date, purchase_amount FROM CustomerSalesDa???  
Edit 10:54:06 SELECT DISTINCT purchase_date, purchase_amount FROM CustomerSalesData WHERE cust???  
Edit 10:53:52 SELECT DISTINCT purchase_date FROM CustomerSalesData WHERE customer_id = 5632  ;???  
Edit 10:53:17 SELECT DISTINCT purchase_date FROM CustomerSalesData WHERE customer_id = 5632 OR???  
Edit 10:40:35 SELECT * FROM `CustomerSalesData` LIMIT 50 ;  
Edit 10:32:54 CREATE TABLE CustomerSpendingInsights ( customer_id INT NOT NULL,  total_items_p???  
Edit 10:32:52 DROP TABLE CustomerSpendingInsights;  
Edit 10:12:44 SELECT DISTINCT product_id, purchase_amount FROM CustomerSalesData WHERE purchas???  
Edit 10:12:35 SELECT DISTINCT product_id, purchase_amount FROM CustomerSalesData WHERE purchas???  
Edit 10:12:24 SELECT DISTINCT product_id, purchase_amount FROM CustomerSalesData WHERE purchas???  
Edit 10:02:29 SELECT DISTINCT product_id, purchase_amount FROM CustomerSalesData WHERE purchas???  
Edit 10:02:19 SELECT product_id, purchase_amount FROM CustomerSalesData WHERE purchase_amount ???  
Edit 10:02:09 SELECT product_id, purchase_amount FROM CustomerSalesData WHERE purchase_amount ???  
Edit 10:01:47 SELECT product_id, purchase_amount FROM CustomerSalesData WHERE purchase_amount ???  
Edit 10:01:34 SELECT product_id, purchase_amount FROM CustomerSalesData WHERE purchase_amount ???  
Edit 10:01:13 SELECT product_id, purchase_amount FROM CustomerSalesData WHERE purchase_amount ???  
Edit 09:29:24 UPDATE `CustomerSalesData` SET `customer_id` = '7365', `purchase_date` = '2020-1??? (0.020 s)  
Edit 09:29:09 UPDATE CustomerSalesData SET purchase_amount = 0.02 WHERE purchase_amount = 0.01???  
Edit 09:20:13 SELECT c.product_id , p.product_price FROM CustomerSalesData AS c JOIN ProductPr???  
Edit 09:18:54 SELECT c.product_id , p.product_price FROM CustomerSalesData AS c JOIN ProductPr???  
Edit 09:18:39 SELECT c.product_id , p.product_price FROM CustomerSalesData AS c JOIN ProductPr???  
Edit 09:18:32 SELECT c.product_id , p.product_price FROM CustomerSalesData AS c JOIN ProductPr???  
Edit 09:18:16 SELECT c.product_id , p.product_price FROM CustomerSalesData AS c JOIN ProductPr???  
Edit 09:11:43 SELECT product_price FROM ProductPricing WHERE product_id = "893GDE"      ;  
Edit 09:10:36 SELECT product_id FROM CustomerSalesData  WHERE purchase_amount = 0.01     ;  
Edit 09:09:48 SELECT c.product_id, c.purchase_amount FROM ProductPricing p, CustomerSalesData ???  
Edit 09:09:30 SELECT p.product_id, c.purchase_amount FROM ProductPricing p, CustomerSalesData ???  
Edit 09:06:43 SELECT product_id FROM ProductPricing, CustomerSalesData WHERE purchase_amount =???  
Edit 09:04:53 SELECT p.product_id FROM ProductPricing p, CustomerSalesData c WHERE c.purchase_???  
Edit 09:04:02 SELECT p.product_price FROM ProductPricing p, CustomerSalesData c WHERE c.purcha???  
Edit 09:03:20 SELECT p.product_price FROM ProductPricing p, CustomerSalesData c WHERE c.purcha???  
Edit 09:01:02 SELECT product_price FROM ProductPricing WHERE purchase_amount = 0.01 FROM Custo???  
Edit 08:47:29 DELETE FROM `ProductPricing` WHERE `product_id` = '667XL' AND `product_id` = '66??? (0.230 s)  
Edit 08:47:05 INSERT INTO ProductPricing (product_id, product_price) SELECT DISTINCT product_i???  
Edit 08:47:02 ALTER TABLE `ProductPricing` CHANGE `product_id` `product_id` varchar(255) NOT N??? (0.278 s)  
Edit 08:46:10 INSERT INTO ProductPricing (product_id, product_price) SELECT DISTINCT product_i???  
Edit 08:44:35 SELECT DISTINCT product_id, purchase_amount FROM CustomerSalesData WHERE purchas???  
Edit 08:43:59 SELECT DISTINCT product_id, purchase_amount FROM CustomerSalesData WHERE purchas???  
Edit 08:43:48 SELECT DISTINCT product_id, purchase_amount FROM CustomerSalesData WHERE purchas???  
Edit 08:43:27 SELECT DISTINCT product_id, purchase_amount FROM CustomerSalesData WHERE purchas???  
Edit 08:37:15 CREATE TABLE ProductPricing( product_id INT NOT NULL,  product_price DECIMAL(8,2???  
Edit 08:27:37 SELECT * FROM CustomerSalesData WHERE purchase_amount = (SELECT MAX(purchase_amo???  
Edit 08:27:26 SELECT * FROM CustomerSalesData WHERE purchase_amount = (SELECT MAX(purchase_amo???  
Edit 08:27:16 SELECT * FROM CustomerSalesData WHERE purchase_amount = (SELECT MAX(purchase_amo???  
Edit 08:26:38 SELECT * FROM CustomerSalesData WHERE purchase_amount = (SELECT MAX(purchase_amo???  
Edit 07:20:30 SELECT * FROM CustomerSalesData WHERE purchase_amount = (SELECT MAX(purchase_amo???  
Edit 07:20:18 SELECT * FROM CustomerSalesData WHERE purchase_amount = (SELECT MAX(purchase_amo???  
Edit 07:20:02 SELECT * FROM CustomerSalesData_Staging WHERE purchase_amount = (SELECT MAX(purc???  
Edit 03:55:42 SELECT * FROM CustomerSalesData_Staging ORDER BY purchase_amount ;            
Edit 03:54:55 SELECT * FROM CustomerSalesData_Staging WHERE purchase_amount = (SELECT MAX(purc???  
Edit 03:54:31 SELECT * FROM CustomerSalesData_Staging WHERE purchase_amount = (SELECT MAX(purc???  
Edit 03:54:23 SELECT * FROM CustomerSalesData_Staging WHERE customer_id = 7365 AND purchase_am???  
Edit 03:54:03 SELECT * FROM CustomerSalesData_Staging WHERE purchase_amount = (SELECT MAX(purc???  
Edit 03:53:25 SELECT * FROM CustomerSalesData_Staging WHERE purchase_amount = (SELECT MAX(purc???  
Edit 03:52:42 SELECT * FROM CustomerSalesData_Staging WHERE customer_id = 7365 ;              ???  
Edit 03:52:08 SELECT MAX(purchase_amount) AS mostPurchased FROM CustomerSalesData_Staging WHER???  
Edit 03:51:02 SELECT MAX(purchase_amount) AS mostPurchased FROM CustomerSalesData_Staging WHER???  
Edit 03:50:56 SELECT MAX(purchase_amount) AS mostPurchased, FROM CustomerSalesData_Staging, WH???  
Edit 03:50:45 SELECT MAX(purchase_amount) AS mostPurchased, FROM CustomerSalesData_Staging, WH???  
Edit 03:49:48 SELECT purchase_amount GREATEST(purchase_amount) AS mostPurchased FROM CustomerS???  
Edit 03:49:31 SELECT purchase_amount, GREATEST(purchase_amount) AS mostPurchased, FROM Custome???  
Edit 03:49:01 SELECT * GREATEST(purchase_amount) AS mostPurchased FROM CustomerSalesData_Stagi???  
Edit 03:48:59 SELECT * GREATEST(purchase_amount) AS mostPurchased FROM CustomerSalesData_Stagi???  
Edit 03:48:57 SELECT * GREATEST(purchase_amount) AS mostPurchased FROM CustomerSalesData_Stagi???  
Edit 03:48:53 SELECT * GREATEST(purchase_amount) AS mostPurchased FROM CustomerSalesData_Stagi???  
Edit 03:48:51 SELECT * GREATEST(purchase_amount) AS mostPurchased FROM CustomerSalesData_Stagi???  
Edit 03:48:49 SELECT * GREATEST(purchase_amount) AS mostPurchased FROM CustomerSalesData_Stagi???  
Edit 03:48:47 SELECT * GREATEST(purchase_amount) AS mostPurchased, FROM CustomerSalesData_Stag???  
Edit 03:48:44 SELECT *, GREATEST(purchase_amount) AS mostPurchased, FROM CustomerSalesData_Sta???  
Edit 03:48:41 SELECT * GREATEST(purchase_amount) AS mostPurchased, FROM CustomerSalesData_Stag???  
Edit 03:48:38 SELECT * GREATEST(purchase_amount) AS mostPurchased, FROM CustomerSalesData_Stag???  
Edit 03:48:32 SELECT * GREATEST(purchase_amount) AS mostPurchased FROM CustomerSalesData_Stagi???  
Edit 03:47:33 SELECT * FROM CustomerSalesData_Staging WHERE customer_id = 7365 ;          
Edit 03:47:02 SELECT * FROM CustomerSalesData_Staging ORDER BY customer_id ;          
Edit 03:46:51 SELECT * FROM CustomerSalesData_Staging ORDER BY customer_id          ;  
Edit 03:46:20 SELECT * FROM CustomerSalesData_Staging, ORDER BY customer_id, ;          
Edit 03:45:41 SELECT * FROM CustomerSalesData_Staging, ORDER BY customer_id ;        
Edit 03:45:38 SELECT * FROM CustomerSalesData_Staging, ORDER BY customer_id       ;  
Edit 03:44:41 SELECT * FROM CustomerSalesData_Staging      ;  
Edit 03:44:21 SELECT * FROM 'CustomerSalesData_Staging';      
Edit 03:43:56 SELECT * FROM 'CustomerSalesData_Staging';      
Edit 03:43:52 SELECT *, FROM 'CustomerSalesData_Staging';    
Edit 03:43:26 SELECT * FROM 'CustomerSalesData_Staging';    
Edit **03:43:14** SELECT * FROM 'CustomerSalesData_Staging' ;  
Edit 16:16:28 CREATE TABLE CustomerSpendingInsights ( customer_id INT NOT NULL,  total_items_p???  
Edit 16:16:23 DROP TABLE CustomerSpendingInsights;  
Edit 15:18:13 CREATE TABLE CustomerSpendingInsights ( customer_id INT NOT NULL,  total_items_p???
Edit 15:18:06 CREATE TABLE CustomerSpendingInsights ( customer_id INT NOT NULL,  total_items_p???
Edit 15:17:51 DROP TABLE CustomerSpendingInsights;    
Edit 15:17:32 DELETE TABLE CustomerSpendingInsights;  
Edit 15:17:22 DELETE TABLE CustomerSpendingInsights  ;
Edit 14:07:23 CREATE TABLE CustomerSpendingInsights ( customer_id INT NOT NULL,  total_items_p???    
Edit 12:57:01 SELECT * FROM `CustomerSalesData_Staging` ORDER BY `customer_id` WHERE 'purchase???  
Edit 12:56:53 SELECT * FROM `CustomerSalesData_Staging` ORDER BY `customer_id` WHERE 'purchase???  
Edit 12:56:40 SELECT * FROM `CustomerSalesData_Staging` ORDER BY `customer_id` WHERE purchase_???  
Edit 12:56:28 SELECT * FROM `CustomerSalesData_Staging` ORDER BY `customer_id` WHERE purchase_???  
Edit 12:56:14 SELECT * FROM `CustomerSalesData_Staging` ORDER BY `customer_id` WHERE purchase_???  
Edit 12:55:52 SELECT * FROM `CustomerSalesData_Staging`, ORDER BY `customer_id`, WHERE purchas???  
Edit 12:55:34 SELECT * FROM `CustomerSalesData_Staging` ORDER BY `customer_id` WHERE purchase_???  
Edit 10:12:07 CREATE TABLE CustomerSalesData_Staging ( customer_id INT, purchase_date DATE, pu???  
Edit 10:11:59 CREATE TABLE CustomerSalesData.Stage ( customer_id INT, purchase_date DATE, purc???  
Edit 09:56:37 CREATE TABLE CustomerSalesData ( customer_id INT, purchase_date DATE, purchase_a???  
Edit 09:56:27 CREATE TABLE CustomerSalesData ( customer_id INT, purchase_date DATE, purchase_a???  
  
  
