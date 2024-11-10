# script-set-env
<br>Setting environment on ubuntu ( vim, python, docker, k3s, ansible )
<br><h2>After installing, script will reboot your system, dont forget about that.</h1>
<br><b>Handwork:</b>
<br>
<ul>
  <li> ssh-keygen -t ed25519</li>
  <li>sudo usermod -aG sudo $USER</li>
  <li>git clone https://github.com/avicityv/script-set-env</li>
  <li>sudo chmod -R 777 ./script-set-env</li>
</ul>
<br>
<h3># Check installation
  <ul>
    <li>python3.9 --version</li>
    <li>ansible --version</li>
    <li>docker run hello-world</li>
    <li>sudo k3s kubectl get nodes</li>
  </ul>
</h2>
<h2>CAN CAUSE ERRORS WITH WEB-SERVERS. BE CAREFUL!</h2>

# script create-db-psql
Edit user, PGPASSWORD and dbname if need.

# script-gui-postgres
<br>App for college classes. View db content, watch DB tables and values</br>
Todo: fix deleting values by key 

# web_gui
Repo for web application that listening local psql db. 
<h3>python -m venv venv</h3>
<h3>source /venv/bin/activate</h3>
<h3>pip install requirements.txt</h3>


