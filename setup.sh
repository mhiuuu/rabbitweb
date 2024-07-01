#!/bin/bash

check_tools() {
    command -v curl >/dev/null 2>&1 || { echo "wget is required but not installed. Aborting."; exit 1; }
    command -v tar >/dev/null 2>&1 || { echo "tar is required but not installed. Aborting."; exit 1; }
    command -v make >/dev/null 2>&1 || { echo "make is required but not installed. Aborting."; exit 1; }
    command -v gcc >/dev/null 2>&1 || { echo "gcc is required but not installed. Aborting."; exit 1; }
}

download_tor() {
    URL="https://dist.torproject.org/"
    HTML_CONTENT=$(curl -s $URL)
    LATEST_VERSION=$(curl -s $URL | grep -oP 'href="\Ktor.*?\.tar\.gz(?=")' | sort -V | tail -n 1 | sed 's/\.tar\.gz$//')
    echo "Latest version $LATEST_VERSION"
    curl -o tor.tar.gz "$URL$LATEST_VERSION.tar.gz"
    tar -xzf tor.tar.gz 
    cd $LATEST_VERSION || { echo "Extraction failed. Aborting."; exit 1; }
}

install() {
    ./configure && make 
    sudo make install
}

cleanup() {
    echo "Cleaning up..."
    cd ..
    rm -rf tor.tar.gz $LATEST_VERSION
}

setupconfig() {
    sudo mv /usr/local/etc/tor/torrc.sample /usr/local/etc/tor/torrc
    sudo mkdir -p /etc/tor
    sudo touch /etc/tor/torrc
    sudo cp -vi /usr/local/etc/tor/torrc /etc/tor/torrc || { echo "Setup failed. Aborting"; exit 1; }
    sudo sh -c 'echo "%include /etc/tor/torrc" >> /usr/local/etc/tor/torrc'
}
main() {
    check_tools
    download_tor
    install
    cleanup
    setupconfig
    echo "Tor is installed. Original config file in '/usr/local/etc/tor/torrc', current config file in '/etc/tor/torrc"
}

main