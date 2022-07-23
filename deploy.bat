git add .
git commit -m "update code"
git push origin master
heroku ps:stop run -a iseek
git push heroku master