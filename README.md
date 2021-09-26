# Souza's Shop Bot

Create a shop list telegram bot!

## Troubleshoot

_First Heroku Push ask for procfile instead of heroku.yml_: Heroku set the
default stack to use procfile. Just need to change on command line as shown
bellow. See
[this](https://devcenter.heroku.com/articles/build-docker-images-heroku-yml)
for more details.

    heroku stack:set container
