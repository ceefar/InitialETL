# ---- imports ----
# for db
import pymysql
import os
from dotenv import load_dotenv
# for csv
import csv
# for number of days between dates
import doing_dates as dt


# ---- db ----
# load environment variables from .env file
load_dotenv()
host = os.environ.get("mysql_host")
user = os.environ.get("mysql_user")
password = os.environ.get("mysql_pass")
database = os.environ.get("mysql_db")


# establish a database connection
connection = pymysql.connect(
    host = host,
    user = user,
    password = password,
    database = database
)


def add_to_db(command):
    cursor = connection.cursor()
    cursor.execute(f"{command}") 
    connection.commit()
    #cursor.close()
    #connection.close()


def get_from_db(command):
    cursor = connection.cursor()
    cursor.execute(f"{command}") 
    myresult = cursor.fetchall()
    connection.commit()
    #cursor.close()
    #connection.close()
    return(myresult)


# not used but obvs would have initially (just did in adminer using SQL command)
init_table_query = f"CREATE TABLE CustomerSalesData (customer_id INT, purchase_date DATE, purchase_amount DECIMAL(7,2), product_id VARCHAR(255) NOT NULL)"


def load_data_from_csv():
    """ 
    load the data locally from the csv before moving it to staging 
    """
    data = []
    try:
        with open('sales_data.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)
        return(data)
    except FileNotFoundError:
        print("No File Found - Halting Program To Prevent Critical Error")
        print("\n- - - -\nPlease Check The File System")


def print_csv_data():
    """ 
    used to check that the data has loaded locally as expected 
    """
    local_copy = load_data_from_csv()
    print("Data Loaded [but i'm not printing it]")
    #[print(item) for item in local_copy]
    #print("\n- - - -\nLocal Data Loaded Successfully\n- - - -\n")
    return(True)


# ---- v1 clean, just drop data ----
def write_local_to_db():
    """ 
    wipe current daily table then upload data to staging table from local copy 
    """
    # initialise var for dropped (partial) items  
    dropped_lines = []
    # load the local data
    local_copy = load_data_from_csv()
    # wipe the current table
    trunc_query = "TRUNCATE TABLE CustomerSalesData_Staging"
    add_to_db(trunc_query)
    for i, item in enumerate(local_copy):
        # skip the header
        if i == 0:
            pass
        else:
            # if any rows are missing, drop the data and add it to a variable to print on completion
            if len(item[0]) < 1 or len(item[1]) < 1 or len(item[2]) < 1 or len(item[3]) < 1:
                dropped_lines.append(i)
                pass
            else:
                # load only complete data to staging, giga basic clean, print confirmation
                upload_query = f"INSERT INTO CustomerSalesData_Staging VALUES ({item[0]}, '{item[1]}', {item[2]}, '{item[3]}')"
                add_to_db(upload_query)
                print(f"Item {i} Added")
                # should have counted total lines in local data (minus 1 for header) and then done count total data to print back (29 of 31 added to db) <<<<<<
    # print confirmation
    print("\n- - - -\nLocal Data Successfully Moved To Staging Table\n- - - -")
    # if any items were dropped, print them
    if dropped_lines:
        print("\n- - - -\nSome Items From Local Data Were Dropped")
        print(f"Lines -> {dropped_lines}")
        print("- - - -\n")


# ---- v2 clean, replace empty fields with nullified dummy data ----
def write_local_to_db():
    """ 
    wipe current daily table then upload data to staging table from local copy,
    adding dummy data for any empty fields
    -> str = ABCDEF, date = 2000-01-01, int = 0000, flt = 0.01 
    """
    # initialise var for dropped (partial) items  
    dummified_lines = []
    # load the local data
    local_copy = load_data_from_csv()
    # wipe the current table
    trunc_query = "TRUNCATE TABLE CustomerSalesData_Staging"
    add_to_db(trunc_query)
    for i, item in enumerate(local_copy):
        # skip the header
        if i == 0:
            pass
        else:
            # if any rows are empty, dummify the data and add it to a variable to print on completion
            # 0 = _cust_id[int], 1 = purch_date[date], 2 = purch_amnt[float/decimal], 3 = prod_id[str]
            if len(item[0]) < 1 or len(item[1]) < 1 or len(item[2]) < 1 or len(item[3]) < 1:
                # if len of item is less than 1 (is empty) then dummify it (see doc string for dummy data format)
                # should make them tuples with the row too tbf <<<<<<
                item[0] = 0000 if len(item[0]) < 1 else item[0]
                item[1] = "2000-01-01" if len(item[1]) < 1 else item[1]
                item[2] = 0.01 if len(item[2]) < 1 else item[2]
                item[3] = "ABCDEF" if len(item[3]) < 1 else item[3]
                # if data was dummified add it's column to var to print for confirmation       
                dummified_lines.append(i)
            # END IF
            # load complete & dummified data to staging, will be entire dataset, print confirmation
            upload_query = f"INSERT INTO CustomerSalesData_Staging VALUES ({item[0]}, '{item[1]}', {item[2]}, '{item[3]}')"
            add_to_db(upload_query)
            # print(f"Item {i} Added")
        # END IF ELSE
    # END FOR
    # print confirmation
    print("\n- - - -\nLocal Data Successfully Moved To Staging Table\n- - - -")
    # if any items were dropped, print them
    if dummified_lines:
        print("\n- - - -\nSome Items From Local Data Were Dummified Due To Incomplete Data")
        print(f"Lines -> {dummified_lines}")
        print("- - - -\n")


def transform_db_data():
    """ pls add doc string """
    # input date option here boom!
    #    - maybe even a want year end option (pyinq?) so you can just enter one date instead of 2?
    transform_each_customers_data()
    #transform_each_customers_data(["2020-12-01", "2020-12-05"])


def get_customer_total_spend(customerID, between_dates=None) -> float: 
    """ QUERY ONE - get customer total spend for period (all) and print to terminal """
    # using none default argument as default mutable arguments are defined when function is defined, not when its run
    # meaning empty lists would contain previous values on subsequent calls, not what we would want
    if between_dates:
        customer_spend_query = f"SELECT SUM(purchase_amount) AS TotalCustomerSpend FROM CustomerSalesData_Staging WHERE customer_id = {customerID[0]} AND purchase_amount > 0.01 AND purchase_date BETWEEN '{between_dates[0]}' AND '{between_dates[1]}'"
    else:
        customer_spend_query = f"SELECT SUM(purchase_amount) AS TotalCustomerSpend FROM CustomerSalesData_Staging WHERE customer_id = {customerID[0]} AND purchase_amount > 0.01 AND purchase_date > '2000-01-01'"
    customer_spend = get_from_db(customer_spend_query)
    # format and print to terminal - customer total spend, with customer number heading
    customer_spend = float(customer_spend[0][0])
    print(f"- - - - - - - - - - - - - - -\nCUSTOMER {customerID[0]}\nTotal Spend : ${customer_spend:.2f}")
    # return spend so the same info can be written to the customers txt file
    return(customer_spend)


def get_customer_total_items_purchased(customerID, between_dates=None) -> int:
    """ QUERY TWO - get customer total amount of items purchased for period (all) """
    # using none param as default mutable arguments are defined when function is defined, not when its run, meaning empty lists would contain prev values on future calls
    if between_dates:
        customer_count_query = f"SELECT COUNT(purchase_amount) AS TotalCustomerSpendCount FROM CustomerSalesData_Staging WHERE customer_id = {customerID[0]} AND purchase_amount > 0.01 AND purchase_date BETWEEN '{between_dates[0]}' AND '{between_dates[1]}'"
    else:
        customer_count_query = f"SELECT COUNT(purchase_amount) AS TotalCustomerItemCount FROM CustomerSalesData_Staging WHERE customer_id = {customerID[0]} AND purchase_amount > 0.01 AND purchase_date > '2000-01-01'"
    customer_item_count = get_from_db(customer_count_query)
    # format and print to terminal - total items purchased 
    customer_item_count = customer_item_count[0][0]
    print(f"Total Items Purchased : {customer_item_count}")
    # return the same info to be written to the customers txt file 
    return(customer_item_count)


def get_customer_avg_spend(customerID, between_dates=None) -> float:
    """ QUERY THREE - get customer average spend (per item) for period (all) - spendAmount / amountOfItems, but uses built in AVG mysql query (same result) """
    # using none param as default mutable arguments are defined when function is defined, not when its run, meaning empty lists would contain prev values on future calls
    if between_dates:
        customer_avg_query = f"SELECT AVG(purchase_amount) AS AvgCustomerSpend FROM CustomerSalesData_Staging WHERE customer_id = {customerID[0]} AND purchase_amount > 0.01 AND purchase_date BETWEEN '{between_dates[0]}' AND '{between_dates[1]}'"
    else:
        customer_avg_query = f"SELECT AVG(purchase_amount) AS AvgCustomerSpend FROM CustomerSalesData_Staging WHERE customer_id = {customerID[0]} AND purchase_amount > 0.01 AND purchase_date > '2000-01-01'"
    customer_avg_spend = get_from_db(customer_avg_query)
    # format and print to terminal - customer average spend 
    customer_avg_spend = customer_avg_spend[0][0]
    print(f"Average Spend Per Item : ${customer_avg_spend:.2f}")
    # return the same info for writing to the customers txt file (not formatted to 2dp)
    return(customer_avg_spend)


def get_customer_unique_items_with_item_counts(customerID, between_dates=None) -> list:
    """ QUERY FOUR - get customer unique items purchased with amount purchased (count) for each item for period (all) """
    # using none param as default mutable arguments are defined when function is defined, not when its run, meaning empty lists would contain prev values on future calls
    if between_dates:
        get_customers_unique_items_list_query = f"SELECT COUNT(*), product_id AS CustomerUniqueItemPurchaseCountList FROM CustomerSalesData_Staging WHERE purchase_amount > 0.01 AND customer_id = {customerID[0]} AND purchase_date BETWEEN '{between_dates[0]}' AND '{between_dates[1]}' GROUP BY product_id"
    else:
        get_customers_unique_items_list_query = f"SELECT COUNT(*), product_id AS CustomerUniqueItemPurchaseCountList FROM CustomerSalesData_Staging WHERE purchase_amount > 0.01 AND customer_id = {customerID[0]} AND purchase_date > '2000-01-01' GROUP BY product_id"
    customer_unique_items_tuptups = get_from_db(get_customers_unique_items_list_query)
    # list comprehension for formatting of unique items with count (different formatting for terminal print)
    itemlist_with_counts_formatted = [f"- {item[1]} [x{item[0]}]" for item in customer_unique_items_tuptups]
    print("Unique Items (list with counts)")
    print(*(itemlist_with_counts_formatted), sep="\n")
    # different formatting for txt file (2x itemID, 4x itemID, etc)
    itemlist_with_counts_for_txt = [f"{item[0]}x {item[1]}" for item in customer_unique_items_tuptups]
    return(itemlist_with_counts_for_txt)


def get_highest_value_item(customerID, between_dates=None) -> tuple:
    """ QUERY FIVE - get customers highest value item (the most expensive item they have purcahsed) for each item for period (all) """
    # using none param as default mutable arguments are defined when function is defined, not when its run, meaning empty lists would contain prev values on future calls
    # must use distinct in query otherwise get repeats for multiple purchases
    if between_dates:
        highest_value_item_query = f"SELECT DISTINCT product_id, purchase_amount FROM CustomerSalesData WHERE purchase_amount = (SELECT MAX(purchase_amount) FROM CustomerSalesData WHERE customer_id = {customerID[0]}) AND customer_id = {customerID[0]} AND purchase_date BETWEEN '{between_dates[0]}' AND '{between_dates[1]}'"
    else:
        highest_value_item_query = f"SELECT DISTINCT product_id, purchase_amount FROM CustomerSalesData WHERE purchase_amount = (SELECT MAX(purchase_amount) FROM CustomerSalesData WHERE customer_id = {customerID[0]}) AND customer_id = {customerID[0]}"
    highest_value_item = get_from_db(highest_value_item_query)
    print(f"Highest Value Item : {highest_value_item[0][0]} at ${float(highest_value_item[0][1]):.2f}")
    return(highest_value_item[0])


def transform_each_customers_data(in_these_dates:list = None):
    """
    calculate total spend for each customer, swerving any column with dummied spend data
    multiple queries, prints to terminal and saves individual customer data files as txt
    """
    # pull each unique customer id to local list for confirmation, not counting rows with dummified spending data 
    # doesn't drop dummified data for purchase date, product id, or customer id
    # does drop dummified data for order amount (if we don't know how much they spent why do we care about the id or date)
    #   - actually this logic is incorrect, if we have the id we can figure out the amount, write a function for this shortly
    #      - also vice versa, if amount can find id, but wouldn't be valid in 99% of cases as many products would have the same price so not implementing this way
    # note, haven't actually considered the dummified customer id case yet properly as we don't have one

    # two separate queries for creating our unique customer list (which we loop for pulling insight data), also prints headers in terminal for clarity
    # validated by boolean because didn't want an empty list as a default parameter
    if in_these_dates:
        get_unique_customers_query = f"SELECT DISTINCT customer_id FROM CustomerSalesData_Staging WHERE purchase_amount > 0.01 AND purchase_date BETWEEN '{in_these_dates[0]}' AND '{in_these_dates[1]}' ORDER BY customer_id ASC" # e.g. in_these_dates = ["2020-12-01", "2020-12-05"]
        print(f"\nDATE RANGE : {in_these_dates[0]} AND {in_these_dates[0]}\n")
    else:
        get_unique_customers_query = "SELECT DISTINCT customer_id FROM CustomerSalesData_Staging WHERE purchase_amount > 0.01 ORDER BY customer_id ASC"
        print("\nDATE RANGE : ALL\n")
    
    # for looping the valid customers for insights
    try:
        valid_customers_list = get_from_db(get_unique_customers_query)
    except pymysql.Error as e:
        print(f"Critical Error : {e}")

    # print out our list of unique customers (there are many lines of info for each customer so we don't need duplicates)
    print("- - - -\nUnique Customers (by ID) Used In This Data Set\n- - - -")
    [print(customer[0]) for customer in valid_customers_list]
    
    # truncate insights before insert
    trunc_query = "TRUNCATE TABLE CustomerSpendingInsights"
    add_to_db(trunc_query)

    # START FOR LOOP
    # loop the unique customers list, query db for sum of purchase amounts for each unique customer, swerving dummified spending data
    for _, customer in enumerate(valid_customers_list): # enumerate is better than range(len(list)), just drop the index
        
        # create unique names for each text file
        if in_these_dates:
            customer_text_file_name = f"cust{customer[0]}_{in_these_dates[0]}_to_{in_these_dates[1]}.txt"
        else:
            customer_text_file_name = f"cust{customer[0]}_allData.txt"
        # open the txt file in write (creates new file if not found)
        text_file = open(customer_text_file_name, "w")
        
        # write txt file headers clarifying date ranges if they were used
        if in_these_dates:
            text_file.write(f"Data Produced From Dates - {in_these_dates[0]} to {in_these_dates[0]}\n")
        else:
            text_file.write(f"Data From All Available Dates Included\n")

        # for dates if given, else all date ranges - get customer data, print it to terminal, then return it to be written to customers txt file 
        if in_these_dates:
            # total spend
            customer_spend = get_customer_total_spend(customerID=customer, between_dates=in_these_dates)
            # total amount of all items purchased
            customer_item_count = get_customer_total_items_purchased(customerID=customer, between_dates=in_these_dates)
            # average spend
            customer_avg_spend = get_customer_avg_spend(customerID=customer, between_dates=in_these_dates)
            # highest value item with its price (tuple)
            highest_value_tuple = get_highest_value_item(customerID=customer, between_dates=in_these_dates)
            # unqiue items with counts list
            itemlist_with_counts_formatted = get_customer_unique_items_with_item_counts(customerID=customer, between_dates=in_these_dates)
        else:
            # total spend
            customer_spend = get_customer_total_spend(customerID=customer)
            # total amount of all items purchased
            customer_item_count = get_customer_total_items_purchased(customerID=customer)
            # average spend
            customer_avg_spend = get_customer_avg_spend(customerID=customer)
            # highest value item with its price (tuple)
            highest_value_tuple = get_highest_value_item(customerID=customer)
            # unqiue items with counts list
            itemlist_with_counts_formatted = get_customer_unique_items_with_item_counts(customerID=customer)
        # write data to txt file in same order as above (total spend, total items count, average spend, highest value item, unique items with counts listed)
        text_file.write(f"CUSTOMER {customer[0]}\nTotal Spend : ${customer_spend:.2f}\n")
        text_file.write(f"Total Items Purchased : {customer_item_count}\n")
        text_file.write(f"Average Spend : ${customer_avg_spend:.2f}\n")
        text_file.write(f"Highest Value Item : {highest_value_tuple[0]} at ${highest_value_tuple[1]:.2f}\n")
        # write to txt is slightly different for the final unqiue items + counts list
        # by using join (and not list comprehension) there is no trailing \n (shout out mozway on stackoverflow for help on this one https://stackoverflow.com/questions/72472001/why-is-map-function-not-computing-my-lambda)
        text_file.write(f"Unique Items With Amount Purchased\n")
        text_file.write('\n'.join(itemlist_with_counts_formatted))

        print("")

        unique_shopping_days_query = f"SELECT DISTINCT customer_id, purchase_date AS unique_purchase_dates FROM CustomerSalesData WHERE customer_id = {customer[0]}"
        unique_shopping_days_info_tuple = get_from_db(unique_shopping_days_query)
        unique_shopping_days = len(unique_shopping_days_info_tuple)
        print(f"Unique Shopping Days : {unique_shopping_days}")
        print(f"Shopping Days As % Of Available Days [38] : {(unique_shopping_days/38) * 100:.1f}%") # counts only start day, not end
        print(f"Average Spend Per Unique Shopping Day [{unique_shopping_days}] : ${customer_spend/unique_shopping_days:.2f}")
        # daily spend between first and last day

        print("")

        first_purchase_date_query = f"SELECT purchase_date FROM CustomerSalesData WHERE customer_id = {customer[0]} AND NOT purchase_date = '2000-01-01' GROUP BY purchase_date ORDER BY purchase_date LIMIT 1"
        first_purchase_date = get_from_db(first_purchase_date_query)
        first_purchase_date = str(first_purchase_date[0][0])
        print(f"Date of First Purchase : {first_purchase_date}")
        last_purchase_date_query = f"SELECT purchase_date FROM CustomerSalesData WHERE customer_id = {customer[0]} AND NOT purchase_date = '2000-01-01' GROUP BY purchase_date ORDER BY purchase_date DESC LIMIT 1"
        last_purchase_date = get_from_db(last_purchase_date_query)
        last_purchase_date = str(last_purchase_date[0][0])
        print(f"Date of Last Purchase : {last_purchase_date}")
        buying_window = dt.calc_date_between_dates(first_purchase_date, last_purchase_date)
        buying_window += 1 # for including both start and end dates
        print(f"Buying Window (days from first to last purchase) : {buying_window}")
        average_spend_during_buying_window = customer_spend/buying_window
        print(f"Daily Average Spend During Buying Window [{buying_window} days] : ${average_spend_during_buying_window:.2f}")
        current_date = ""
        days_since_last_purchase = dt.calc_date_between_dates(first_purchase_date, last_purchase_date)
        
        # C:\Users\robfa\Downloads\initialetl
        # then
        # days since last purchase
        # average daily spend from first to now
   

        highest_spend_on_day_query = f"SELECT purchase_date, SUM(purchase_amount) AS TotalCustomerSpend FROM CustomerSalesData WHERE customer_id = {customer[0]} GROUP BY purchase_date ORDER BY TotalCustomerSpend DESC LIMIT 1" 
        highest_spend_on_day = get_from_db(highest_spend_on_day_query)
        print(f"Highest Spend On A Day : ${float(highest_spend_on_day[0][1])} on {str(highest_spend_on_day[0][0])}")
        lowest_spend_on_day_query = f"SELECT purchase_date, SUM(purchase_amount) AS TotalCustomerSpend FROM CustomerSalesData WHERE customer_id = {customer[0]} GROUP BY purchase_date ORDER BY TotalCustomerSpend LIMIT 1" 
        lowest_spend_on_day = get_from_db(lowest_spend_on_day_query)
        print(f"Lowest Spend On A Day : ${float(lowest_spend_on_day[0][1])} on {str(lowest_spend_on_day[0][0])}")
        spend_deviation = highest_spend_on_day[0][1] - lowest_spend_on_day[0][1]
        print(f"Spend Deviation (diff in high and low spend) : ${spend_deviation}") # lower is better, specifically lower deviation with higher average spend

        print("")

        print("Spend Per Day")
        purchase_total_for_each_shopping_day_query = f"SELECT purchase_date, SUM(purchase_amount) AS TotalCustomerSpend FROM CustomerSalesData WHERE customer_id = {customer[0]} GROUP BY purchase_date"
        purchase_total_for_each_shopping_day = get_from_db(purchase_total_for_each_shopping_day_query)
        [print(f"${float(day_info[1])} on {str(day_info[0])}") for day_info in purchase_total_for_each_shopping_day]

        # SHOULD DO A SECOND AVERAGE FOR DATES WHICH ISN'T THE AVG SPEND DURING ALL DATES, BUT THE AVG STARTING FROM THEIR FIRST PURCHASE TO THE END DATE (not last purchase date tho)
        
        # use days between dates to get some extra info here like percent or ratio 
        # note its 38 days but should use this grepper info https://www.google.com/search?q=days+between+dates&rlz=1C1CHBF_en-GBGB914GB914&oq=days+between+dates&aqs=chrome..69i57j0i512l2j0i20i263i512j0i512l6.1647j0j7&sourceid=chrome&ie=UTF-8
      

        # close the txt file
        print("- - - - - - - - - - - - - - -\n")
        text_file.close()

        # before finishing loop for this customer add the data (total_spend, avg_spend, total_items_purchased) to the new insights table (v1)
        insert_query = f"INSERT INTO CustomerSpendingInsights (customer_id, total_items_purchased, total_spend, avg_spend, highest_indiv_item_spend, highest_indiv_item_id) VALUES ({customer[0]}, {customer_item_count}, {customer_spend}, {customer_avg_spend:.2f}, {highest_value_tuple[1]:.2f}, '{highest_value_tuple[0]}')"
        add_to_db(insert_query)   

    # END FOR LOOP    
    print("- - - -\nCOMPLETE\n- - - -\n")


def finalise_staging_data():
    trunc_query = f"TRUNCATE TABLE CustomerSalesData"
    add_to_db(trunc_query)
    from_stage_to_final_query = f"INSERT INTO CustomerSalesData SELECT * FROM CustomerSalesData_Staging"
    add_to_db(from_stage_to_final_query)
    trunc_query = f"TRUNCATE TABLE CustomerSalesData_Staging"
    add_to_db(trunc_query)
    

def update_product_with_missing_price():
    """  
    get id and price of all items with 0.01 (dummy) purchase amount from main dataset using join
    so fucking dope as this actually dragged back the customer 1054 into relevance, and now his data is not only in txt
    but also in the insights table, completing the entire dataset even though there was missing datal and making him usable for insights
    """
    # note1 if at end use salesData, if during run use staging (where its best anyway duh)
    # note2 tho im unsure what would happen if it was a lone id with no existing data to check against tho assumption is it just wouldnt fill it in as before 
    # join id and price from SalesData_Staging x new productPricing where we have had to use dummy (0.01) purchase data with the id and price it was for others
    # unsure what would happen in duplicate id cases, would probably want it to drop the data but assuming it will just use one of the ones it finds
    # (or return them all and the first one in the list will just be selected below)
    get_id_price_query = "SELECT c.product_id, p.product_price FROM CustomerSalesData_Staging AS c JOIN ProductPricing AS p ON p.product_id = c.product_id WHERE c.purchase_amount = 0.01"
    id_price_list = get_from_db(get_id_price_query)
    try:
        # if the query returned data (unsure how well this will work tho tbf)
        if id_price_list[0]:
            # for each item in the loaded dataset with 0.01 purchase_amount (id_price_list contains the *actual* price and the matching id)
            for _, item in enumerate(id_price_list):       
                # find data in the staging table with the matching id and purchase amount of 0.01, and update it with the data we've pulled from the new ProductPricing table
                update_missing_data_query = f"UPDATE CustomerSalesData_Staging SET purchase_amount = {float(item[1])} WHERE purchase_amount = 0.01 AND product_id = '{item[0]}'"
                add_to_db(update_missing_data_query)
    except IndexError:
        (print("There Was A Problem Updating Missing Price Data - Skipping This Step"))
        fake_input = input("Press Enter To Continue")


def update_product_price_table():
    """ 
    new table ProductPricing matches instances of unique product_id with their own unique price,
    meaning yes there is one instance of an id with the same price but it adds both to our table (which we want),
    this will be used to filling in missing fields as well as other possible future requirements
    """
    # truncate product pricing before updating
    trunc_query = "TRUNCATE TABLE ProductPricing"
    add_to_db(trunc_query)
    product_price_table_query = "INSERT INTO ProductPricing (product_id, product_price) SELECT DISTINCT product_id, purchase_amount FROM CustomerSalesData WHERE purchase_amount > 0.01 AND NOT product_id = 'ABCDEF' ORDER BY purchase_amount DESC"
    add_to_db(product_price_table_query)


def driver():
    """
    main program, reads csv, stages to db, cleans data by dummifying it,
    then transforms the data, prints into to terminal, writes that same info to individual txt files for each customer
    both for all their data, and for a specified date range, then adds some of the relevant data to customer new customer spending insights db table 
    """
    print("Program Start")
    # have some basic validation checks in here on the csv file, so if it passes that then we run the db functions
    if print_csv_data():
        # stages the date and cleans the data with simple dummification it
        write_local_to_db()
        # updates dummy prices with existing data if it can find it, do this before running our transformation insights
        update_product_with_missing_price()
        # transforms and writes the data to txt files and new customer spending insights table
        transform_db_data()
        # move original csv data from staging table to final table, and wipe staging table
        finalise_staging_data()
    # update the new product pricing table, do this at end as though we can use it to fill in missing data it should be using existing/historical data to do that (?)
    update_product_price_table()
    
    
# driver... duh
driver()


# ---- important notes ----
# most importantly have updated the only date from 2021 as the 1 month gap made no logical sense and made the data averages unrealistic
#     - afforementioned date is now 2020-12-08
#     - when calculating to current date not actually using our date in 2022, using 2020-12-10, 2 days after the last purchase date (which is the one mentioned above) 
#
# also have made some changes to the original dataset
#     - removed a few data points from everything except customer id for dummifying, cleaning, updating, and generally testing


# ---- ideas ----
#
# COULD/SHOULD
# could/should drastically expand the data set with new information just so i can work with more data since is hardly enough currently
#     - could expand with a product table that would show wholesale cost and markup so could calculate profit margins but thats more in future tbf loads more to do for now
# could/should expand the data set based on what we will get for project
# new most purchased item and most spending on item fields for db
# new insights by year db tables
# new table for product insights (item popularity, item popularity for period, etc)
# and try to do web app dashboard, charts and data visualisation, & ml model 
#
# FOR INSIGHTS
# most valuable customer ranking
#     - if customer is above the average value rating then they would get access to a store card or rewards card or something
#     - then tiered rewards based on some other insight idk
# first purchase date, last purchase date
# spending period (how many days between first and last purchase)
# total/average spend for each year
# some of the above stuff in could/should too
# and probs many others but too tired to think rn


# MADE REDUNDANT
def get_customer_unique_items_only(customerID) -> list:
    # redundant since query 5 does the same thing just better, only keeping as want to remember the generator
    # QUERY FOUR - get customer unique items purchased for period (all) - the item numbers that the customer purchased in the timeframe with no duplicates
    get_customers_unique_items_query = f"SELECT DISTINCT product_id AS CustomerUniqueItemPurchaseCount FROM CustomerSalesData_Staging WHERE purchase_amount > 0.01 AND customer_id = {customerID[0]} AND purchase_date > '2000-01-01'"
    customer_unique_items_list = get_from_db(get_customers_unique_items_query)
    # creates a generator expression then prints from that generator with new line separator 
    items_formatted_generator = (f"{i+1}. {item[0]}" for i, item in enumerate(customer_unique_items_list))
    # format and print to terminal - customer unique items, prints a header first since generator print has no ability to prepend 
    print(f"Just Unique Items Purchased")
    print(*(items_formatted_generator), sep="\n")
    # use a new, separate list comprehension for writing to the txt file since don't want loads of excess lines for no reason
    items_formatted = [f"{i+1}. {item[0]}" for i, item in enumerate(customer_unique_items_list)]
    return(items_formatted)