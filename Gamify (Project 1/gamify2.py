def initialize():
    global health, hedons
    global running, resting, textbooks   #docstrings are not needed
    global star_run, star_text
    global time_since
    global time_during
    global tired
    global bored
    global running_time_in_a_row, textbooks_time_in_a_row
    global now, prev_offer1, prev_offer2, last_star
    health = 0
    hedons = 0
    time_since = 100000
    running_time_in_a_row = 0
    textbooks_time_in_a_row = 0
    running = False
    resting = True
    now = 0
    prev_offer1 = -1
    prev_offer2 = -1
    last_star = 100000
    textbooks = False
    star_run = False
    star_text = False
    tired = False
    bored = False


def get_cur_hedons():
    '''Return the total number of hedons accumulated so far in integers.'''
    return hedons


def get_cur_health():
    '''Return the total number of health points accumulated so far in integers.'''
    return health


def offer_star(activity):
    '''Offer a star for string parameter activity
    parameters : {"running", "resting", "textbooks"}
    what the function does:
    -records offer time to detect boredom
    -gives star to activity in parameter
    -resets last star to 0    '''

    global star_run, star_text , now, prev_offer1, prev_offer2, last_star, bored


    if prev_offer2 != -1:
        if (now - prev_offer2) < 120:
            bored = True

    prev_offer2 = prev_offer1
    prev_offer1 = now

    if activity == "running":
        star_run = True
        star_text = False
    elif activity == "textbooks":
        star_text = True
        star_run = False
    else:
        star_run = False
        star_text = False


    last_star = 0


def perform_activity(activity, duration):
    '''Simulate performing activity for duration minutes.

    parameters:
    activity -> string that is one of {"running", "resting", "textbooks"}. If not, the function will do nothing
    duration -> positive integer representing how many minutes the user spends doing an activity

    what the function does:
    -Updates hedons and health points according to the rules
    -Applies star bonuses that are relevant
    -Updates the tired variable
    -Updates the clock and time since last star offer '''

    global time_during, star_text, star_run, running, textbooks, resting
    global tired, time_since, last_star, running_time_in_a_row, textbooks_time_in_a_row, now

    if activity != "running" and activity != "textbooks" and activity != "resting":
        return

    time_during = duration


    running_before = running
    textbooks_before = textbooks
    resting_before = resting

    if activity == "running" or activity == "textbooks":
            if time_since < 120:
                tired = True
            else:
                tired = False
            time_since = 0

    if activity == "running":
        resting = False
        textbooks = False
        running = True

        running_time_in_a_row += time_during
        textbooks_time_in_a_row = 0

        if star_text == True:
            star_text = False

    elif activity == "textbooks":
        resting = False
        running = False
        textbooks = True

        textbooks_time_in_a_row += time_during
        running_time_in_a_row = 0

        if star_run == True:
            star_run = False

    else:
        running = False
        textbooks = False
        resting = True

        time_since += time_during
        running_time_in_a_row = 0
        textbooks_time_in_a_row = 0

        if star_run == True or star_text == True:
            star_run = False
            star_text = False

    calc_health()
    calc_hedons()

    now += duration
    last_star += duration



def calc_health():
    '''Calculate health based on the current activity and duration '''

    global health, time_during, textbooks, running_time_in_a_row
    if running == True:
        if running_time_in_a_row <= 180:
            health += 3 * time_during
        elif running_time_in_a_row - time_during >= 180:
            health += time_during
        else:
            extra = running_time_in_a_row - 180
            health += 3 * (time_during - extra) + extra
    elif textbooks == True:
        health += 2 * time_during


def calc_hedons():
    '''Calculate hedons based on the current activity and duration (and other factors)
    -split the calculation into two cases: when user is bored , and when the user is not bored'''

    global hedons, time_during, star_run, star_text, tired
    global running, textbooks, running_time_in_a_row, textbooks_time_in_a_row

    if running == True:
        prev_run = running_time_in_a_row - time_during  # streak at the start of this chunk
        not_tired = 0
        if prev_run < 10:
            if prev_run + time_during <= 10:
                not_tired = time_during
            else:
                not_tired = 10 - prev_run
        tired_num = time_during - not_tired

        if tired == True:
            base = -2 * time_during
        else:
            base = 2 * not_tired + (-2) * tired_num

        bonus = 0
        if not bored and star_can_be_taken("running"):
            if time_during <= 10:
                bonus = 3 * time_during
            else:
                bonus = 3 * 10
            star_run = False

        hedons += base + bonus

    elif textbooks == True:
        prev_text = textbooks_time_in_a_row - time_during
        not_tired_t = 0
        if prev_text < 20:
            if prev_text + time_during <= 20:
                not_tired_t = time_during
            else:
                not_tired_t = 20 - prev_text
        tired_num_t = time_during - not_tired_t

        if tired == True:
            base_t = -2 * time_during
        else:
            base_t = 1 * not_tired_t + (-1) * tired_num_t

        bonus_t = 0
        if not bored and star_can_be_taken("textbooks"):
            if time_during <= 10:
                bonus_t = 3 * time_during
            else:
                bonus_t = 3 * 10
            star_text = False

        hedons += base_t + bonus_t
    else:
        pass  #pass is to just do nothing!



def star_can_be_taken(activity):
    '''Return True iff a star can be used for `activity` right now.
    Conditions to check:
    -user is not bored
    -no time has passed since the star offer
    -star was offered for the activitty in the parameter '''

    global last_star, star_run, star_text
    if bored or last_star != 0:
        return False
    elif activity == "running" and star_run == True:
        return True
    elif activity == "textbooks" and star_text == True:
        return True
    else:
        return False


def most_fun_activity_minute():
    '''return the activity that would give the most hedons if ran for one minute'''

    best_activity = "resting"
    best_value = 0

    if time_since < 120:
        is_tired = True
    else:
        is_tired = False


    if running == True:
        if is_tired:
            r_base = -2
        else:
            prev_run = running_time_in_a_row
            if prev_run < 10:
                r_base = 2
            else:
                r_base = -2
    else:
        if is_tired:
            r_base = -2
        else:
            r_base = 2

    r_bonus = 0

    if star_can_be_taken("running"):
        r_bonus = 3
    r_total = r_base + r_bonus
    if r_total > best_value:
        best_value = r_total
        best_activity = "running"

    if textbooks == True:
        if is_tired:
            t_base = -2
        else:
            prev_text = textbooks_time_in_a_row
            if prev_text < 20:
                t_base = 1
            else:
                t_base = -1
    else:
        if is_tired == True:
            t_base = -2
        else:
            t_base = 1
    t_bonus = 0
    if star_can_be_taken("textbooks"):
        t_bonus = 3
    t_total = t_base + t_bonus
    if t_total > best_value:
        best_value = t_total
        best_activity = "textbooks"

    return best_activity


if __name__ == "__main__":
    initialize()
    perform_activity("running", 30)
    print(get_cur_hedons()) # -20 = 10 * 2 + 20 * (-2)
    print(get_cur_health()) # 90 = 30 * 3
    print(most_fun_activity_minute()) #resting
    perform_activity("resting", 30)
    offer_star("running")
    print(most_fun_activity_minute()) # running
    perform_activity("textbooks", 30)
    print(get_cur_health()) # 150 = 90 + 30*2
    print(get_cur_hedons()) # -80 = -20 + 30 * (-2)
    offer_star("running")
    perform_activity("running", 20)
    print(get_cur_health()) # 210 = 150 + 20 * 3
    print(get_cur_hedons()) # -90 = -80 + 10 * (3-2) + 10 * (-2)
    perform_activity("running", 170)
    print(get_cur_health()) # 700 = 210 + 160 * 3 + 10 * 1
    print(get_cur_hedons()) # -430 = -90 + 170 * (-2)


