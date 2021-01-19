from flask import Flask, render_template, request, redirect, send_file
from so_scrapper import get_jobs as so_get_jobs
from ind_scrapper import get_jobs as ind_get_jobs
from exporter import save_to_file

app = Flask("SuperScrapper")


db = {}

@app.route("/") # 누군가가 "/"에 접속하면, home이라는 함수를 만들거야
def home():
  return render_template('potato.html')
  # return "<h1>Job Search</h1><form><input placeholder='What job do you want?' requred /><button>Search</button>"


@app.route("/report")
def report ():
  word = request.args.get('word')
  if word:
    word = word.lower()
    existingJobs = db.get(word)
    if existingJobs:
      jobs = existingJobs
    else:
      jobs = ind_get_jobs(word) + so_get_jobs(word) 

      db[word] = jobs
  else:
    return redirect("/")
  return render_template("report.html", searchingBy=word, resultsNumber = len(jobs), jobs=jobs)

@app.route("/export")
def export():
      try:
        word = request.args.get('word')
        if not word:
          raise Exception()
        word = word.lower()
        jobs = db.get(word)
        if not jobs:
          raise Exception()

        save_to_file(jobs)

        return send_file("jobs.csv")

      except:
        return redirect("/")

app.run(host="0.0.0.0")