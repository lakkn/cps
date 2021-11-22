from flask import Blueprint, render_template, request, g, flash
import sqlite3 as sql
from .scraper import scrape

DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sql.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/scraper/', methods=['GET','POST'])
def scraper():
    data = request.form.get("search")
    dlen = len(str(data))
    if (len(str(data)) == 7 and str(data)[0:3] == "14-" and str(data)[3:7].isdigit()) or (len(str(data)) == 4 and str(data).isdigit()):
        teamnum = ""
        if len(str(data)) == 4:
            teamnum = "14-"
        teamnum += str(data)
        query = 'select * from info;'
        all = query_db(query)
        isThere = False
        for a_team in all:
            if a_team[1] == teamnum:
                isThere = True
        if isThere:
            scrape()
            query = 'select * from info where TeamNumber = "'+teamnum+'";'
            team = query_db(query)
            inlength = len(team[0])
            query = 'select count(*) from info;'
            numt = query_db(query)
            numte = numt[0][0]
            for i in range(1,100):
                print(i)
                query = 'select * from info where rowid ='+str(i)+';'
                top_team = query_db(query)
                if top_team[0][8] == None:
                    continue
                else:
                    break
            query = 'select * from info where rowid ='+str(team[0][0]-1)+';'
            team_above = query_db(query)[0]
            query = 'select * from info where rowid ='+str(team[0][0]+1)+';'
            team_below = query_db(query)[0]
            query = 'select * from info where "Location/Category" ="'+team[0][2]+'";'
            stinfo = query_db(query)
            st_info = []
            count = 1
            for a_team in stinfo:
                if str(a_team[1]) == teamnum:
                    st_info.append(count)
                    break
                count += 1
            st_info.append(len(stinfo))
            query = 'select * from info where "Tier" ="'+team[0][4]+'";'
            tiinfo = query_db(query)
            ti_info = []
            count = 1
            for a_team in tiinfo:
                if str(a_team[1]) == teamnum:
                    ti_info.append(count)
                    break
                count += 1
            ti_info.append(len(tiinfo))
            query = 'select * from info where "Division" ="'+team[0][3]+'";'
            diinfo = query_db(query)
            di_info = []
            count = 1
            for a_team in diinfo:
                if str(a_team[1]) == teamnum:
                    di_info.append(count)
                    break
                count += 1
            di_info.append(len(diinfo))
        else:
            flash('Team does not exist', category='error')
            team = [()]
            numte = 0
            inlength = 0
            top_team = [()]
            team_above = [()]
            team_below = [()]
            st_info = []
            ti_info = []
            di_info = []

    elif data == None:
        team = [()]
        numte = 0
        inlength = 0
        top_team = [()]
        team_above = [()]
        team_below = [()]
        st_info = []
        ti_info = []
        di_info = []
    elif dlen > 0:
        flash('Invalid team number', category='error')
        team = [()]
        numte = 0
        inlength = 0
        top_team = [()]
        team_above = [()]
        team_below = [()]
        st_info = []
        ti_info = []
        di_info = []
    return render_template("scraper.html", info=team[0], inlen = inlength, numt = numte, topt = top_team[0], teama = team_above, teamb = team_below, stinfo = st_info, tiinfo = ti_info, diinfo = di_info)
