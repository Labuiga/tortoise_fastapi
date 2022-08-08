# If you have UNIX environment:

execute install.sh with privileges

    sudo su
    . install.sh

launch the app:

    . launch.sh


# If you have Windows environment:

install python virtualenv on windows

install python3 on project/p3
    
    virtualenv -p python3 p3

install pip requirements

    pip install -r requirements.txt

create sqlite schemas 

    python schemas.py

launch app

    . p3/bin/activate && python -m app.main



    