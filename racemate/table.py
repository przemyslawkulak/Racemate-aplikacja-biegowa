from racemate.models import MyUser

TABLES = [
    [30, 1076, 1840, 3826, 8464, 17357, 30, 720, 465, 423, 384, 355, 335],
    [31, 1047, 1791, 3723, 8241, 16917, 31, 720, 460, 412, 374, 348, 325],
    [32, 1019, 1745, 3626, 8029, 16498, 32, 720, 448, 400, 365, 335, 315],
    [33, 993, 1701, 3534, 7827, 16102, 33, 720, 438, 390, 356, 328, 305],
    [34, 969, 1659, 3446, 7636, 15723, 34, 720, 425, 380, 348, 320, 300],
    [35, 945, 1620, 3363, 7453, 15363, 35, 720, 415, 370, 340, 313, 290],
    [36, 923, 1582, 3284, 7279, 15019, 36, 720, 410, 361, 333, 305, 285],
    [37, 901, 1546, 3209, 7114, 14690, 37, 720, 400, 353, 326, 300, 275],
    [38, 881, 1512, 3137, 6955, 14375, 38, 720, 392, 345, 319, 294, 270],
    [39, 861, 1479, 3069, 6804, 14074, 39, 600, 386, 337, 312, 288, 265],
    [40, 843, 1448, 3003, 6659, 13785, 40, 600, 378, 329, 306, 282, 260],
    [41, 825, 1418, 2941, 6520, 13509, 41, 600, 371, 322, 300, 276, 255],
    [42, 808, 1389, 2881, 6387, 13243, 42, 600, 363, 316, 294, 271, 250],
    [43, 791, 1361, 2824, 6260, 12988, 43, 600, 356, 309, 289, 266, 245],
    [44, 775, 1335, 2769, 6137, 12743, 44, 600, 350, 303, 283, 261, 240],
    [45, 760, 1310, 2716, 6020, 12506, 45, 600, 343, 297, 278, 256, 235],
    [46, 746, 1285, 2665, 5907, 12279, 46, 600, 337, 291, 273, 252, 230],
    [47, 732, 1262, 2616, 5798, 12060, 47, 600, 331, 286, 269, 247, 225],
    [48, 718, 1239, 2570, 5693, 11849, 48, 600, 325, 281, 264, 243, 222],
    [49, 705, 1218, 2524, 5592, 11646, 49, 600, 320, 276, 260, 239, 220],
    [50, 693, 1197, 2481, 5495, 11449, 50, 600, 314, 271, 255, 235, 218],
    [51, 681, 1176, 2439, 5402, 11259, 51, 600, 309, 267, 251, 231, 215],
    [52, 669, 1157, 2399, 5311, 11076, 52, 600, 304, 262, 247, 228, 213],
    [53, 658, 1138, 2360, 5224, 10899, 53, 540, 299, 258, 244, 224, 210],
    [54, 647, 1120, 2322, 5140, 10727, 54, 540, 294, 254, 240, 221, 205],
    [55, 637, 1102, 2286, 5058, 10561, 55, 540, 290, 250, 236, 217, 202],
    [56, 637, 1085, 2251, 4980, 10400, 56, 540, 285, 246, 233, 214, 200],
    [57, 617, 1069, 2217, 4903, 10245, 57, 540, 281, 243, 230, 211, 197],
    [58, 608, 1053, 2184, 4830, 10094, 58, 540, 277, 239, 226, 208, 193],
    [59, 598, 1037, 2152, 4758, 9947, 59, 540, 273, 236, 223, 205, 190],
    [60, 590, 1023, 2122, 4689, 9805, 60, 540, 269, 232, 220, 203, 188]]


def checktable(time, check):  # sprawdzenie VDOT w tabeli
    for i in range(0, 30):
        if time > TABLES[0][check]:
            vdot = 30
            return vdot
        elif time <= TABLES[i][check] and time > TABLES[i + 1][check]:
            vdot = TABLES[i][0]
            return vdot
        elif time <= TABLES[30][check]:
            vdot = 60
            return vdot


def generateVDOT(tr):  # ustalenie który dystans sprawdzać
    if tr.distance_total < 3000:
        return f'VDOT is generated from distance 3 km'

    elif tr.distance_total >= 3000 and tr.distance_total < 5000:
        speed = round((float(tr.distance_total) / float(tr.time_total) * 3.6), 2)
        time = int(3000 / (speed / 3.6))

        return checktable(time, 1)

    elif tr.distance_total >= 5000 and tr.distance_total < 10000:
        speed = round((float(tr.distance_total) / float(tr.time_total) * 3.6), 2)
        time = int(5000 / (speed / 3.6))

        return checktable(time, 2)

    elif tr.distance_total >= 10000 and tr.distance_total < 20000:
        speed = round((float(tr.distance_total) / float(tr.time_total) * 3.6), 2)
        time = int(10000 / (speed / 3.6))

        return checktable(time, 3)

    elif tr.distance_total >= 20000 and tr.distance_total < 40000:
        speed = round((float(tr.distance_total) / float(tr.time_total) * 3.6), 2)
        time = int(21097 / (speed / 3.6))

        return checktable(time, 4)

    elif tr.distance_total >= 40000:
        speed = round((float(tr.distance_total) / float(tr.time_total) * 3.6), 2)
        time = int(42195 / (speed / 3.6))

        return checktable(time, 5)


def check_best_time(tr):
    if not tr.user.r3:
        tr.user.r3 = 0
    if not tr.user.r5:
        tr.user.r5 = 0
    if not tr.user.r10:
        tr.user.r10 = 0
    if not tr.user.r21:
        tr.user.r21 = 0
    if not tr.user.r42:
        tr.user.r42 = 0

    if tr.distance_total < 3000:
        return None, 'too short run'

    elif tr.distance_total == 3000:
        time = tr.time_total
        if tr.user.r3 > 0:
            if time < tr.user.r3:
                return time, 'r3'
            else:
                return None, 'r3'
        return time, 'r3'


    elif tr.distance_total > 3000 and tr.distance_total < 5000:
        speed = round((float(tr.distance_total) / float(tr.time_total) * 3.6), 2)
        time = int(3000 / (speed / 3.6))
        print(time)
        if tr.user.r3 > 0:
            if time < tr.user.r3:
                return time, 'r3'
            else:
                return None, 'r3'
        return time, 'r3'

    elif tr.distance_total == 5000:
        time = tr.time_total
        if tr.user.r5 > 0:
            if time < tr.user.r10:
                return time, 'r5'
            else:
                return None, 'r5'
        return time, 'r5'

    elif tr.distance_total > 5000 and tr.distance_total < 10000:
        speed = round((float(tr.distance_total) / float(tr.time_total) * 3.6), 2)
        time = int(5000 / (speed / 3.6))
        if tr.user.r5 > 0:
            if time < tr.user.r10:
                return time, 'r5'
            else:
                return None, 'r5'
        return time, 'r5'

    elif tr.distance_total == 10000:
        time = tr.time_total
        if tr.user.r10 > 0:
            if time < tr.user.r10:
                return time, 'r10'
            else:
                return None, 'r10'
        return time, 'r10'

    elif tr.distance_total > 10000 and tr.distance_total < 21097:
        speed = round((float(tr.distance_total) / float(tr.time_total) * 3.6), 2)
        time = int(10000 / (speed / 3.6))
        if tr.user.r10 > 0:
            if time < tr.user.r10:
                return time, 'r10'
            else:
                return None, 'r10'
        return time, 'r10'

    elif tr.distance_total == 21097:
        time = tr.time_total
        if tr.user.r21 > 0:
            if time < tr.user.r21:
                return time, 'r21'
            else:
                return None, 'r21'
        return time, 'r21'

    elif tr.distance_total > 21097 and tr.distance_total < 42195:
        speed = round((float(tr.distance_total) / float(tr.time_total) * 3.6), 2)
        time = int(21097 / (speed / 3.6))
        if tr.user.r21 > 0:
            if time < tr.user.r21:
                return time, 'r21'
            else:
                return None, 'r21'
        return time, 'r21'

    elif tr.distance_total == 42195:
        time = tr.time_total
        if tr.user.r42 > 0:
            if time < tr.user.r42:
                return time, 'r42'
            else:
                return None, 'r42'
        return time, 'r42'

    elif tr.distance_total > 42195:
        speed = round((float(tr.distance_total) / float(tr.time_total) * 3.6), 2)
        time = int(42195 / (speed / 3.6))
        print(time)
        if tr.user.r42 > 0:
            if time < tr.user.r3:
                return time, 'r42'
            else:
                return None, 'r42'
        return time, 'r42'


def generate_records(total_time):
    hours = total_time // 3600
    minutes = (total_time - hours * 3600) // 60
    seconds = total_time - hours * 3600 - minutes * 60
    if hours > 0:
        hours = str(hours) + "h "
    else:
        hours = ''
    if minutes > 0:
        minutes = str(minutes) + "min "
    else:
        minutes = ''
    if seconds > 0:
        seconds = str(seconds) + "sec "
    else:
        seconds = ''

    return hours + minutes + seconds


def adding_result(user):
    results = {}
    results['marathon'] = generate_records(user.r42)
    results['half'] = generate_records(user.r21)
    results['10k'] = generate_records(user.r10)
    results['5k'] = generate_records(user.r5)
    results['3k'] = generate_records(user.r3)
    return results
