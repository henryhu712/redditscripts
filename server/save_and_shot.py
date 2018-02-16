import pymysql.cursors
import praw
import subprocess

# Access to reddit api

freddit = open('./password/reddit', 'r')
reddit_client_id        = freddit.readline().rstrip('\n')
reddit_client_secret    = freddit.readline().rstrip("\n")
reddit_username         = freddit.readline().rstrip("\n")
reddit_password         = freddit.readline().rstrip("\n")

bot = praw.Reddit(
        user_agent    = 'dev2 v0.1',
        client_id     = reddit_client_id,
        client_secret = reddit_client_secret,
        username      = reddit_username,
        password      = reddit_password
    )

# Access to mysql

fmysql  = open('./password/mysql', 'r')
mysql_user      = fmysql.readline().rstrip("\n")
mysql_password  = fmysql.readline().rstrip("\n")
mysql_db        = fmysql.readline().rstrip("\n")

connection = pymysql.connect(
        host           = 'localhost',
        user           = mysql_user,
        password       = mysql_password,
        db             = mysql_db,
        charset        = 'utf8mb4',
        cursorclass    = pymysql.cursors.DictCursor
    )
cursor = connection.cursor()

languages = ['es', 'ja', 'hi', 'pt', 'bn', 'ru', 'de', 'vi', 'ko', 'fr']

file_obj = 'fine'
fobj = open(file_obj, "r");

lineCount = 1
reddit_id = ''
theTitle = ''
theLang = ''
trans_zh = ''
transTitle = {}
trans = []

for line in fobj:
    theLine = line.rstrip('\n')

    if lineCount == 1:
        print(theLine)
        lineCount = 2

    elif lineCount == 2:
        print(theLine)
        reddit_id = theLine
        lineCount = 3

    elif lineCount == 3:
        print(theLine)
        lineCount = 4

    elif lineCount == 4:
        print(theLine)
        trans_zh = theLine
        lineCount = 5

    elif lineCount == 5:
        print(theLine)
        #trans_es = theLine
        transTitle['es'] = theLine
        lineCount = 6

    elif lineCount == 6:
        transTitle['ja'] = theLine
        lineCount = 7

    elif lineCount == 7:
        transTitle['hi'] = theLine
        lineCount = 8

    elif lineCount == 8:
        transTitle['pt'] = theLine
        lineCount = 9

    elif lineCount == 9:
        transTitle['bn'] = theLine
        lineCount = 10

    elif lineCount == 10:
        transTitle['ru'] = theLine
        lineCount = 11

    elif lineCount == 11:
        transTitle['de'] = theLine
        lineCount = 12

    elif lineCount == 12:
        transTitle['vi'] = theLine
        lineCount = 13

    elif lineCount == 13:
        transTitle['ko'] = theLine
        lineCount = 14

    elif lineCount == 14:
        transTitle['fr'] = theLine
        lineCount = 1

        # English
        sql1 = "SELECT `reddit_id` FROM `newsitem` WHERE `reddit_id`=%s"
        cursor.execute(sql1, (reddit_id))
        result = cursor.fetchone()
        if (result is None):
            subm = bot.submission(id=reddit_id)
            sql11 = "INSERT INTO `newsitem` (`reddit_id`, `title`, `language`, `url_origin`, `status`, `created`, `published`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql11, (subm.id, subm.title, 'en', subm.url, 1, subm.created_utc, subm.created_utc))
            connection.commit()

        # Chinese
        sql2 = "SELECT `reddit_id` FROM `translated` WHERE `reddit_id`=%s AND `language`=%s"
        cursor.execute(sql2, (reddit_id, 'zh'))
        result = cursor.fetchone()
        if (result is None):
            trans.append((reddit_id, trans_zh, 'zh', 1))
        else:
            sql3 = "UPDATE translated SET `title`=%s WHERE `reddit_id`=%s AND `language`=%s"
            cursor.execute(sql3, (trans_zh, reddit_id, 'zh'))
            connection.commit()

        # Other languages
        for lang in languages:
            cursor.execute(sql2, (reddit_id, lang))
            result = cursor.fetchone()
            if (result is None):
                trans.append((reddit_id, transTitle[lang], lang, 1))

        # Take shot
        f_reddit = open('./en_version/' + reddit_id, "r")
        url_origin = f_reddit.readline().rstrip("\n")
        subprocess.call(['./shot/phantomjs', './shot/take_shot.js', reddit_id, url_origin])
        f_reddit.close()

print('')
if trans:
    print(trans)
    sql = "INSERT INTO `translated` (`reddit_id`, `title`, `language`, `status`) VALUES (%s,%s,%s,%s)"
    cursor.executemany(sql, trans)
    connection.commit()
else:
    print('empty')

connection.close()
fobj.close()
freddit.close()
fmysql.close()
