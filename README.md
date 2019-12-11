# SIRS 2019/2020 - Group 13

## Automatic Vulnerability Detector
"The leader of your group of hackers decided to create a scoring system that rewards the
members for any new vulnerabilities that they manage to find. With that goal in mind, he
implemented a system that allows members to submit their attacks and gain points.
As a member, you decided to create a program that automatically searches for
vulnerabilities in binaries in order to win this intra-group competition!
Your project should provide the following components:
* Compute fingerprinting of binaries through input/output interaction
* Automatically detect common vulnerabilities like calls to "gets" functions or to
printf-family functions with user controlled buffers.
* Submit fingerprinting and vulnerabilities to score points.
* Receive and store vulnerabilities from group members
* The leader of the group should be able to see the scoreboard and the exploits of
each member.
* Hackers should not be able to see other people’s attacks or submit bad attacks for
someone else. Basically, try to prevent any kind of cheating.
The primary focus of the system should be the scoring system integrity and information
confidentiality.
For the secondary functionality (vulnerability detector) you can choose an existing tool
such as the ones below, or implement a rudimentary solution yourself."
### References:
* AFL - American Fuzzy Lop has been the most widely used fuzzer for a while. It uses genetic fuzzing
to find inputs that crashes binaries, among other things.
> http://lcamtuf.coredump.cx/afl/
* Angr - A state-of-the-art binary analysis engine that allows to symbolically execute a binary and find
vulnerabilities and create exploits mostly automatically.
> https://angr.io/
* BAP - Binary Analysis Platform is a framework for binary analysis. It can be used to detect calls to
certain functions for instance.
> https://github.com/BinaryAnalysisPlatform/bap

## Execution
On the *Setup* folder run:
```bash
vagrant up --provision
```

After this, when the machines are up, it will open a virtual machine that is the client, and will ask for the credentials:
login: **vagrant** and password: **vagrant**.
When logged in just enter the command to initialize the interface:
```bash
./client/gui.sh
```

 Interface
After initializing the interface Xfce, open the Firefox app and open the web site https://192.168.50.10. This will open the scoreboard web interface.

After opening the website should be able to create new users, promote/demote users do leaders, if the user is already a leader. And other functionalities of the website.

If the client wants do submit a vulnerability, it need to install angr and cryptography which is used in our protocol. Run the following command:
```bash
mkvirtualenv --python=$(which python3) angr && python3 -m pip install angr cryptography
```
After the installation, to run a the vulnerability detector simply run:
```bash
python3 VulnDetector.py
```
Once the program starts input the angr launch file. An input program we provided is `angrVuln2`. Just input the name of the angr file you want. Note that the angr file must have a main function that returns the fingerprint. both the angr file and the binary that is to be analysed must be in the same folder as the `VulnDetector.py` and the `customClient.py`.
The just insert the explaination for the vulnerbility found and the username and password for the user.

After the submission of the vulnerability, you can check that the vulnerability was submitted on the website.

