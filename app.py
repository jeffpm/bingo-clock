from datetime import datetime

def break_down_minutes(max, minutes):
    answer = list()
    if minutes <= max:
        answer.append(minutes)
        return answer

    if minutes - max < max:
        answer.append(max)
        answer.append(minutes-max)
        return answer

    counter = 0
    for i in range(max, 0, -1):
        print(i)
        if i == max:
            answer.append(i)
            counter += i
            print(answer)
            continue
        elif i + counter <= minutes:
            answer.append(i)
            counter += i
            continue
        if counter == minutes:
            return answer

    return answer

def get_colors(hour, minutes):
    colors = dict()
    colors[hour] = "red"
    for min in minutes:
        if min in colors:
            colors[min] = "blue"
        else:
            colors[min] = "green"

    return colors

def main():
    # red = hour
    # green = minute
    # blue = both
    
    now = datetime.now()
    hour = int('{d.hour}'.format(d=now))

    if hour == 0:
        hour = 24

    minutes = int('{d.minute}'.format(d=now))
    print(f"Hour: {hour}")
    print(f"Minutes: {minutes}")
    minutes = break_down_minutes(25, minutes)  

    print(get_colors(hour, minutes))


if __name__ == "__main__":
    main()