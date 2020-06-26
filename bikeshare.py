import time
import pandas as pd
import numpy as np

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
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Enter a city (chicago, new york city, washington): ")
    city = city.lower()
    while city != 'chicago' and city != 'new york city' and city != 'washington':
        city = input("Enter a valid city (chicago, new york city, washington): ")
        city = city.lower()
    # TO DO: get user input for month (all, january, february, ... , june)
    month = input("Enter a month (all, january, february, ... , june): ")
    month = month.lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Enter a day name (all, mon, tue, wed, thu, fri, sat , sun): ")
    day = day.lower()

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
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june','july','august','september','october','november','december']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Popular month:',  popular_month)
    
    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Popular day:',  popular_day)

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)
    
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]    
    print('most commonly used start station: ' + popular_start_station )
    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('most commonly used end station: ' + popular_end_station)
    # TO DO: display most frequent combination of start station and end station trip
    popular_startandend_station = (df['Start Station']+df['End Station']).mode()[0]
    print('most frequent combination of start station and end station trip: ' + popular_startandend_station )
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration:\n')
    start_time = time.time()

    # TO DO: display total travel time
    
    df['delta time']= (df['End Time']-df['Start Time'])
    df['delta time sec']=df['delta time'].dt.seconds
    
    total_travel_time= np.sum(df['delta time sec'])

    print('total travel time: ' , total_travel_time)
    # TO DO: display mean travel time
    mean_travel_time= np.mean(df['delta time sec'])
    print('mean travel time' , mean_travel_time)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    count_user_type=df['User Type'].value_counts()
    print ('Counts of user type: ',count_user_type)
    

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        counts_gender= df['Gender'].value_counts()
        print ('Counts of gender: ',counts_gender)
    else:
        print ("The city doesn't have Gender information")

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year_of_birth = np.min(df['Birth Year'])
        print ('Earliest year of birth: ' , earliest_year_of_birth)
        most_recent_year_of_birth= df['Birth Year'].values[0]
        print ('Most recent year of birth: ' , most_recent_year_of_birth)
        most_common_year_of_birth = df['Birth Year'].mode()[0]  
        print ('Most common year of birth: ' , most_common_year_of_birth)
    else:
        print ("The city doesn't have Birth Year information")
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters() 
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        review = input('\nWould you like to view individual trip data? Enter yes or no.\n')
        review=review.lower()
        a = int(0)
        while review=='yes':            
            print (df[a:a+5])
            review = input('\nWould you like to view individual trip data? Enter yes or no.\n')
            review=review.lower()
            a = a + 5
            
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

  
