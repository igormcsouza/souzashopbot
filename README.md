# Souza's Shop Bot

Create a shop list telegram bot!

## Troubleshoot

_First Heroku Push ask for procfile instead of heroku.yml_: Heroku set the
default stack to use procfile. Just need to change on command line as shown
bellow. See
[this](https://devcenter.heroku.com/articles/build-docker-images-heroku-yml)
for more details.

    heroku stack:set container

_Heroku is trying to bind to port_: Well, this app is not a web app, so, the
dyno must be set to be a worker. More about it
[here](https://devcenter.heroku.com/articles/build-docker-images-heroku-yml#build-defining-your-build).
Remember to set worker in the `heroku.yml`. If the dyno isn't starting up
correctly, go and manually start it up!
