#!/bin/bash

sig_trap () {

    echo -e "\n\n\n\nCleaning up & Terminating on user request .................\n\n"
    rm -f /usr/bin/cloudpoint

}

install_python () {
    os_release="$(awk -F= '/^NAME/{print $2}' /etc/os-release | tr -d '"')"
    if [ "$os_release" == 'Ubuntu' ]; then
        apt-get install -y python3 python3-pip
        pip3 install --upgrade pip
        ret_val=$?
        if (( "$ret_val" != "0" )); then
            echo -e "\nSomething went wrong. Please ensure Python3 is installed and run this script again.\n"
            exit
        fi
    elif [ "$os_release" == 'Red Hat Enterprise Linux Server' ]; then
        yum install -y python34 python34-pip
        pip3 install --upgrade pip
        ret_val=$?
        if (( "$ret_val" != "0" )); then
            echo -e "\nSomething went wrong. Please ensure Python3 is installed and run this script again.\n"
            exit
        fi
    else
        echo -e "\nCouldn't determine platform type.\nPlease install Python3 manually and run this script again.\n"
        exit
    fi
}
########################
#     Main Program     #
########################


trap 'rc=$?; trap "" EXIT; sig_trap $rc; exit $rc' INT TERM QUIT HUP

if [ "$#" != "0" ];
then
    echo "Usage: $0"
else
    if (( "$(id -u)" != "0" ));
    then
        echo -e "\nThis script should be run as root\n"
        exit
    fi

    if ! [[ -x "$(command -v python3)"  &&
            -x "$(command -v pip3 )" ]] ; then
        echo -e "\nPython3/pip3 is not installed on this host (cannot find it in \$PATH)\n"
        while true;
        do
            read -p "Install python3 (y)es, (n)o?" install_py
            if [ "$install_py" = "y" ];
            then
                install_python
                break
            elif [ "$install_py" = "n" ];
            then
                echo -e "Please install Python3 and run this script again\n"
                exit
            else
                echo -e "\nPlease answer 'y' or 'n'\n"
            fi
        done
    fi

    pip3 install -r ./requirements.txt
    ln -s "$(pwd)"/src/cloudpoint.py /usr/bin/cloudpoint
    ln -s "$(pwd)"/cloudpoint_cli.config /root/.cloudpoint_cli.config
    activate-global-python-argcomplete
    source /etc/profile
    echo -e "Setup is complete...\n" 
    echo -e "Please open up a new session for command completion to work\n"
    echo -e "Run 'cloudpoint -h' to get CloudPoint CLI help\n\n"
fi
