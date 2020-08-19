# petegraham.co.uk

Code for petegraham.co.uk based on https://github.com/nickbalestra/kactus.

## Installation

You need Ruby 2.1.0 or higher installed for Jekyl with Github pages https://help.github.com/enterprise/2.11/user/articles/setting-up-your-github-pages-site-locally-with-jekyll/#step-1-create-a-local-repository-for-your-jekyll-site. OS X currently has Ruby 2.0 as it's built in version.

Install rvm https://rvm.io/rvm/install:
```
curl -sSL https://get.rvm.io | bash -s stable --ruby
```

Activate rvm:
```
source ~/.rvm/scripts/rvm
```

Install bundler:
```
gem install bundler
```

Install dependencies:
```
bundle install
```

## Running

```
rvm use 2.4.1
jekyll serve
```

## Deploying

Simply push to main:
```
git push
```
