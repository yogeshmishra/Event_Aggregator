sudo apt-get install libffi-dev
sudo apt-get install libssl-dev
sudo apt-get install libxml2-dev libxslt1-dev python-dev

pip install scrapy
pip install pyelasticsearch

pip install scrapyjs

sudo apt-get update
sudo apt-get install apt-transport-https ca-certificates
sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
sudo echo "deb https://apt.dockerproject.org/repo ubuntu-trusty main" >> /etc/apt/sources.list.d/docker.list
sudo apt-get update
sudo apt-get purge lxc-docker
sudo apt-cache policy docker-engine
sudo apt-get update
sudo apt-get install linux-image-extra-$(uname -r)
sudo apt-get update
sudo apt-get install docker-engine
sudo service docker start
sudo docker run hello-world

docker run -p 8050:8050 scrapinghub/splash

