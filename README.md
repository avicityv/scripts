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
<h2> Just log in to your psql CLI and paste script. </h2>
<h3># git clone https://github.com/avicityv/db_college.git </h3>
<h3># cd db_college </h3>
<h3># cat script_db.txt </h3>  <h3> - COPY THIS CODE (Ctrl+Shift+C)</h3>
<h3># psql -U postgres 
<h3> paste code from clipboard (Ctrl+Shift+V)
<h3> Check db <b># \d</b></h3>

# script-gui-postgres
<br>Script for college classes.</br>


