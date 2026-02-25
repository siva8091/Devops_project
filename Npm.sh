curl -fsSL https://rpm.nodesource.com/setup_21.x | sudo bash -

sudo yum install -y nodejs

node -v
npm -v
sudo yum remove nodejs -y
