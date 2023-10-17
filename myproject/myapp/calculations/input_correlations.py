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
