import emoji
from datetime import datetime, timedelta


def which_emoji(a):

    if a[3] == 'True':
        a[3] = emoji.emojize("✅")
    elif a[3] == 'False':
        a[3] = emoji.emojize("❌")
    return a


def sort_by_date(a):
    
    a = list(map(list,a))
    a.sort(key=lambda date: date[2])

    return a


def time_to_deadline(task):
    dl = datetime.strptime(task[2], '%Y-%m-%d %H:%M')
    now = datetime.now()
    rz = int((dl-now).total_seconds())
    if rz <= 0:
        res = ''
    else:
        if rz//3600 == 1:
            res = f'{rz//3600} час {(rz-3600*(rz//3600))//60} минут'
        elif rz//3600 == 0:
            res = f'{rz//3600} часов {(rz-3600*(rz//3600))//60} минут'
        else:
            res = f'{rz//3600} часа {(rz-3600*(rz//3600))//60} минут'
    return res


def chek_deadline(task):

    return datetime.now() <= datetime.strptime(task[2], '%Y-%m-%d %H:%M')




def time_to_complete(days, task):
    res = []
    tod = datetime.now().date()
    for ind, item in enumerate(task):
        if days == 0:
            dt = item[2].split()[0]
            if (tod == datetime.strptime(dt, '%Y-%m-%d').date()):
                res.append(item)
        elif days == 7:
            dt = datetime.strptime(item[2], '%Y-%m-%d %H:%M').date()
            dl = datetime.strptime((tod + timedelta(days=7)).strftime('%Y-%m-%d'), '%Y-%m-%d').date()
            rz = ((dl - dt).days)

            if 0 <= rz <= 7:
                res.append(item)
        elif days == 30:
            dt = datetime.strptime(item[2], '%Y-%m-%d %H:%M').date()
            dl = datetime.strptime((tod + timedelta(days=30)).strftime('%Y-%m-%d'), '%Y-%m-%d').date()
            rz = ((dl - dt).days)

            if 0 <= rz <= 30:
                res.append(item)
        elif days == 365:
            dt = datetime.strptime(item[2], '%Y-%m-%d %H:%M').date()
            dl = datetime.strptime((tod + timedelta(days=365)).strftime('%Y-%m-%d'), '%Y-%m-%d').date()
            rz = ((dl - dt).days)

            if 0 <= rz <= 365:
                res.append(item)
    return res




