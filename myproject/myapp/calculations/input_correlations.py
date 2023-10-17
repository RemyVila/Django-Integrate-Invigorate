sample_data = [
        {
            "id": 1,
            "date": "2023-09-01",
            "user_id": 1,
            "wellbeing": 5,
            "vigor": 4,
            "foods": {
                "foods": [
                    "chicken",
                    "rice",
                    "black beans",
                    "monster"
                ]
            },
            "hours_slept": 7,
            "wakeup_time": "08:00:00"
        },
        {
            "id": 2,
            "date": "2023-09-02",
            "user_id": 1,
            "wellbeing": 4,
            "vigor": 3,
            "foods": {
                "foods": [
                    "eggs",
                    "toast",
                    "coffee"
                ]
            },
            "hours_slept": 6,
            "wakeup_time": "07:30:00"
        },
        {
            "id": 3,
            "date": "2023-09-03",
            "user_id": 1,
            "wellbeing": 3,
            "vigor": 2,
            "foods": {
                "foods": [
                    "cereal",
                    "milk"
                ]
            },
            "hours_slept": 5,
            "wakeup_time": "07:00:00"
        },
        {
            "id": 4,
            "date": "2023-09-04",
            "user_id": 1,
            "wellbeing": 4,
            "vigor": 4,
            "foods": {
                "foods": [
                    "salad",
                    "water",
                    "nuts"
                ]
            },
            "hours_slept": 6,
            "wakeup_time": "08:30:00"
        },
        {
            "id": 5,
            "date": "2023-09-05",
            "user_id": 1,
            "wellbeing": 5,
            "vigor": 5,
            "foods": {
                "foods": [
                    "oatmeal",
                    "yogurt",
                    "berries"
                ]
            },
            "hours_slept": 7,
            "wakeup_time": "08:00:00"
        },
        {
            "id": 6,
            "date": "2023-09-06",
            "user_id": 1,
            "wellbeing": 4,
            "vigor": 3,
            "foods": {
                "foods": [
                    "turkey sandwich",
                    "chips",
                    "soda"
                ]
            },
            "hours_slept": 6,
            "wakeup_time": "07:30:00"
        },
        {
            "id": 7,
            "date": "2023-09-07",
            "user_id": 1,
            "wellbeing": 3,
            "vigor": 2,
            "foods": {
                "foods": [
                    "pizza",
                    "cola"
                ]
            },
            "hours_slept": 5,
            "wakeup_time": "07:00:00"
        },
        {
            "id": 8,
            "date": "2023-09-08",
            "user_id": 1,
            "wellbeing": 5,
            "vigor": 4,
            "foods": {
                "foods": [
                    "pancakes",
                    "syrup",
                    "orange juice"
                ]
            },
            "hours_slept": 7,
            "wakeup_time": "08:00:00"
        },
        {
            "id": 9,
            "date": "2023-09-09",
            "user_id": 1,
            "wellbeing": 4,
            "vigor": 3,
            "foods": {
                "foods": [
                    "scrambled eggs",
                    "toast",
                    "tea"
                ]
            },
            "hours_slept": 6,
            "wakeup_time": "07:30:00"
        },
        {
            "id": 10,
            "date": "2023-09-10",
            "user_id": 1,
            "wellbeing": 3,
            "vigor": 2,
            "foods": {
                "foods": [
                    "granola",
                    "milk"
                ]
            },
            "hours_slept": 5,
            "wakeup_time": "07:00:00"
        },
        {
            "id": 11,
            "date": "2023-09-11",
            "user_id": 1,
            "wellbeing": 4,
            "vigor": 4,
            "foods": {
                "foods": [
                    "chicken salad",
                    "water",
                    "almonds"
                ]
            },
            "hours_slept": 6,
            "wakeup_time": "08:30:00"
        },
        {
            "id": 12,
            "date": "2023-09-12",
            "user_id": 1,
            "wellbeing": 5,
            "vigor": 5,
            "foods": {
                "foods": [
                    "yogurt parfait",
                    "berries",
                    "honey"
                ]
            },
            "hours_slept": 7,
            "wakeup_time": "08:00:00"
        },
        {
            "id": 13,
            "date": "2023-09-13",
            "user_id": 1,
            "wellbeing": 4,
            "vigor": 3,
            "foods": {
                "foods": [
                    "club sandwich",
                    "fries",
                    "soda"
                ]
            },
            "hours_slept": 6,
            "wakeup_time": "07:30:00"
        },
        {
            "id": 14,
            "date": "2023-09-14",
            "user_id": 1,
            "wellbeing": 3,
            "vigor": 2,
            "foods": {
                "foods": [
                    "pasta",
                    "sauce",
                    "garlic bread"
                ]
            },
            "hours_slept": 5,
            "wakeup_time": "07:00:00"
        },
        {
            "id": 15,
            "date": "2023-09-15",
            "user_id": 1,
            "wellbeing": 4,
            "vigor": 4,
            "foods": {
                "foods": [
                    "steak",
                    "baked potato",
                    "green beans"
                ]
            },
            "hours_slept": 6,
            "wakeup_time": "08:30:00"
        }
]


def average_wellbeing_and_vigor_by_hours_slept(data):
    # Create a dictionary to store the total wellbeing, vigor, and count for each unique hours_slept
    hourly_stats = {}

    for entry in data:
        hours_slept = entry['hours_slept']
        wellbeing = entry['wellbeing']
        vigor = entry['vigor']

        if hours_slept not in hourly_stats:
            hourly_stats[hours_slept] = {'total_wellbeing': 0, 'total_vigor': 0, 'count': 0}

        hourly_stats[hours_slept]['total_wellbeing'] += wellbeing
        hourly_stats[hours_slept]['total_vigor'] += vigor
        hourly_stats[hours_slept]['count'] += 1

    # Calculate the average wellbeing and average vigor for each unique hours_slept
    average_stats = {}
    for hours_slept, stats in hourly_stats.items():
        average_wellbeing = round(stats['total_wellbeing'] / stats['count'], 1)
        average_vigor = round(stats['total_vigor'] / stats['count'], 1)
        average_stats[hours_slept] = {'average_wellbeing': average_wellbeing, 'average_vigor': average_vigor}

    return average_stats

def average_wellbeing_and_vigor_by_unique_foods(data):
    # Create a dictionary to store the total wellbeing, vigor, and count for each unique food
    food_stats = {}

    for entry in data:
        foods = entry['foods']['foods']
        wellbeing = entry['wellbeing']
        vigor = entry['vigor']

        for food in foods:
            if food not in food_stats:
                food_stats[food] = {'total_wellbeing': 0, 'total_vigor': 0, 'count': 0}

            food_stats[food]['total_wellbeing'] += wellbeing
            food_stats[food]['total_vigor'] += vigor
            food_stats[food]['count'] += 1

    # Calculate the average wellbeing and average vigor for each unique food
    average_stats = {}
    for food, stats in food_stats.items():
        average_wellbeing = round(stats['total_wellbeing'] / stats['count'], 1)
        average_vigor = round(stats['total_vigor'] / stats['count'], 1)
        average_stats[food] = {'wellbeing': average_wellbeing, 'vigor': average_vigor}

    return average_stats
