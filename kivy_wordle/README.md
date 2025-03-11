# Wordle app

## Tips for build
You can follow the [official guide](https://kivy.org/doc/stable/guide/packaging-android.html). I will share how I did the build.

I did this on Ubuntu 22.04.5, python 3.12.7.

Install buildozer from GitHub, because they fixed some issues from last release. I did it with activated venv.
```bash
pip3 install git+https://github.com/kivy/buildozer
```

Done commands from [buildozer docs](https://buildozer.readthedocs.io/en/latest/installation.html)
```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
pip3 install --upgrade Cython==0.29.33 virtualenv
```

In _kivy_wordle_ directory ran this, which created file _buildozer.spec_.
```bash
buildozer init
```

Then I plugged in phone, turned on developer mode and ran this, but did not work.  
It was stuck on `Waiting for application to start`. I guess the phone was somehow not connected.
```bash
buildozer android debug deploy run
```

So I did this, which created an _.apk_ file. I moved the _.apk_ file to phone and installed it.
```bash
buildozer android debug
```
