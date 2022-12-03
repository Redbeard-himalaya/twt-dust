# Getting Start

This project is just a demo python code to show how to create tweets, retweet, reply tweets, get twitter user timeline, and search popular tweets.

The demo code is based on Pypi twitter project which wraps twitter API v1.1. Users have to create Twitter account app before using it.


## Twitter Account APP SignUp
Follow [Twitter developer API instructions](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api) to sign up your Twitter account.

After sign up, follow below instructions to create a APP in your [twitter developer portal](https://developer.twitter.com/en/portal/)

 1. Click "Projects & Apps" on left navigation frame;
 2. Click "Overview";
 3. Click "Create App" in "Standalone Apps" section;
 4. Enter your app name and click next;
 5. Save your **Access Token**, **Access Token Secret**, **Api Key**, **Api Key Secret** into **.env** file of this project (follow the demo);

## Runtime Environment Setup
Download this project first:
git clone https://github.com/Redbeard-himalaya/twt-dust.git

Then, install Docker engine depended by the runtime environment of this project. Follow [docker engine installation instructions](https://docs.docker.com/engine/install/) to install docker on your machine.

## Run Project
Now, you can run this project. Follow below instructions to run:

 - Get top tweets of a specific twitter user
	 - docker-compose run --rm tw timeline -u ${user_name} -c {count}
 - Search popular tweets of a topic in Chinese
	 - docker-compose run --rm tw search -p ${topic} -l cs
 - Retweet a tweet
	 - docker-compose run --rm tw retweet -i ${id}
 - Create your new tweet
	 - docker-compose run --rm tw tweet -t 'Hello, the world!'
 - Reply a tweet
	 - docker-compose run --rm tw reply -u ${user_name} -i ${id} -t 'Hello, this is my reply'
 - Get help
	 - docker-compose run --rm tw help
	 - docker-compose run --rm tw -h

## Examples

 - To retweet latest (20 by default) tweets of user Mina88117194
	 - do docker-compose run --rm tw retweet -u Mina88117194
 - To reply latest 5 tweets of user Mina88117194
	 - docker-compose run --rm tw reply -u Mina88117194 -c 5 -t 'Thank you very much. NFSC fellow'
 - To search popular tweet relevant to 'ccp'
	 - docker-compose run --rm tw search -p 'ccp'
 - To search popular tweet relevant to 'ccp' and tweet geocode is within NewYork 100km range
	 - docker-compose run --rm tw search -p 'ccp' -g '40.73103330314383,-74.00377049618126,100km'
