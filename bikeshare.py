import time
import pandas as pd
import numpy as np
import datetime as de

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bike share data!')

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    msg = "Please enter city as Chicago, New York City or Washington: "
    city = input(msg).lower()
    correct_cities = ['chicago','new york city','washington']

    while city not in correct_cities:
        print("Incorrect value entered. Please enter a correct city:")
        city = input(msg).lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    msg = "Please enter month between January and June otherwise state 'all': "
    month = input(msg).title()
    correct_months = ['All','January','February','March','April','May','June']

    while month not in correct_months:
        print("Incorrect value entered. Please enter a correct month, otherwise state 'all':")
        month = input(msg).title()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    msg = "Please enter day of week between Monday and Sunday, otherwise enter 'all': "
    day = input(msg).title()
    correct_days = ['All','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

    while day not in correct_days:
        print("Incorrect value entered. Please enter a correct week day, otherwise enter 'all':")
        day = input(msg).title()

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df

def raw_data(df):
    """Prompts the user to see the contents of the dat files."""
    #Intialise parameter for records to show
    n = 0
    raw_display = input("\nWould you like to show the first five records of the file? Type 'yes' to do so.\n").lower()
    while raw_display == 'yes':
        #Increment record display by 5
        n += 5
        #Print specified itteration of x5 records
        print(df.head(n))
        #Prompt user for an additional 5 lines continuously until user opts out
        raw_display = input("\nWould you like to show the next five records of the file? Type 'yes' to do so.\n").lower()

    input("Displaying statistics on the dataset filtered, press Enter to continue...\n")

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    try:
        # TO DO: display the most common month
        common_month_int = df['month'].mode()[0]
        # Convert month integer to month name
        common_month = de.datetime.strptime(str(common_month_int), "%m")
        common_month_name = common_month.strftime("%B")
        print('Most Common Month:', common_month_name)

        # TO DO: display the most common day of week
        common_week_day = df['day_of_week'].mode()[0]
        print('Most Common Day of Week:', common_week_day)

        # TO DO: display the most common start hour
        # extract hour from the Start Time column to create an hour column
        df['Start hour'] = df['Start Time'].dt.hour
        # find the most popular hour
        common_start_hour = df['Start hour'].mode()[0]
        print('Most Common Start Hour:', common_start_hour)

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    except KeyError:
        print("Warning (Time Stats): Some columns for analysis do not exist in this dataset!\n")


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    try:
        # TO DO: display most commonly used start station
        common_start_station = df['Start Station'].value_counts().nlargest(1).index[0]
        print('Most Commonly Used Start Station:', common_start_station)

        # TO DO: display most commonly used end station
        common_end_station = df['End Station'].value_counts().nlargest(1).index[0]
        print('Most Commonly Used End Station:', common_end_station)

        # TO DO: display most frequent combination of start station and end station trip
        df['Start End Trip'] = df['Start Station'] + ' >> ' + df['End Station']
        common_station_trip = df['Start End Trip'].value_counts().nlargest(1).index[0]
        print('Most Commonly Used Start >> End Station Trip:', common_station_trip)

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    except KeyError:
        print("Warning (Station Stats): Some columns for analysis do not exist in this dataset!\n")


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    try:
        # TO DO: display total travel time
        # Sum time in seconds
        # Convert to days/hours/minutes/seconds
        print('Total Travel Time (days, hh:mi:ss):', str(de.timedelta(seconds=int(df['Trip Duration'].sum()))))

        # TO DO: display mean travel time
        # Average the time per trip, in seconds
        conversion = de.timedelta(seconds=int(df['Trip Duration'].mean()))
        print('Average Travel Time per Trip (hh:mi:ss):', str(conversion))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    except KeyError:
        print("Warning (Trip Duration Stats): Some columns for analysis do not exist in this dataset!\n")


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    try:
        # TO DO: Display counts of user types
        user_types = df['User Type'].value_counts()
        print(user_types)
        print('\n')

        # TO DO: Display counts of gender and count undisclosed
        gender_types = df['Gender'].value_counts(dropna=False).sort_index(ascending=False)
        print(gender_types)
        print('\n')

        # TO DO: Display earliest, most recent, and most common year of birth
        print ("Earliest Birth Year:",int(df['Birth Year'].min()))
        print ("Most Recent Birth Year:",int(df['Birth Year'].max()))
        print ("Most Common Birth Year:",int(df['Birth Year'].mode()[0]))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    except KeyError:
        print("Warning (User Stats): Some columns for analysis do not exist in this dataset!\n")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        #display raw data
        raw_data(df)

        #display statistics
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
