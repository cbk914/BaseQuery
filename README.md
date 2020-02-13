<h1 align="center">
  BaseQuery V2.0
</h1>

<p align="center">
  <a href="https://twitter.com/G666g1e">
      <img src="https://img.shields.io/twitter/url?url=https%3A%2F%2Fgithub.com%2Fg666gle%2FBaseQuery">
  </a>
  <a href="https://github.com/g666gle/BaseQuery/blob/master/LICENSE.md">
    <img src="https://img.shields.io/github/license/g666gle/BaseQuery">
  </a>
  <a href="https://github.com/g666gle/BaseQuery/graphs/contributors">
      <img src="https://img.shields.io/github/contributors/g666gle/BaseQuery.svg">
  </a>
  <a href="https://github.com/g666gle/BaseQuery/issues">
    <img src="https://img.shields.io/github/issues-raw/g666gle/BaseQuery.svg">
  </a>
  <a href="https://github.com/g666gle/BaseQuery/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aclosed+">
      <img src="https://img.shields.io/github/issues-closed-raw/g666gle/BaseQuery.svg">
  </a>
</p>

Your private data is constantly being traded and sold all over the internet. 
Leaks and breaches propagate on a weekly or even daily basis making it difficult to gauge your level of exposure. 
The majority of user-passwords and other sensitive information have been posted 
somewhere on the internet/darknet for anyone to see. 
To take more control of what personal info is out there you can use 
[Haveibeenpwned](https://haveibeenpwned.com/) to narrow down which breaches your 
information has been exposed in. This is a great start but won't tell you which passwords were exposed.
What if you want to know exactly what information of yours other people have access to? 
BaseQuery makes it easy to organize and search through hundreds or even thousands of breaches extremely fast.


![basequery_banner](https://user-images.githubusercontent.com/47184892/70909711-f2e15380-2005-11ea-9f77-d2d78e6d6d41.png)
### Features Included:
 * A 4x nested storage structure
 * Average import speeds of 10,000+ entries per second (Intel Core i7-7700HQ CPU @ 2.8GHz)
 * Instantaneous querying system
 * Facebook's zstd loss-less compression algorithm to reduce the size of the data (On average reduces the data to less than 10% of the original size)
 * Calculate the time all your files will take to import based on your specific hardware
 * Duplicate data protection
 * Output all of your findings in a standard format
 * Email harvesting tool built-in

## Installing

### Git Clone

To Install BaseQuery from GitHub type the following commands

```
git clone https://github.com/g666gle/BaseQuery.git
cd BaseQuery
sudo ./install.sh
./run.sh
```

### Docker

To Install BaseQuery into a docker container type the following commands

_This requires docker and docker-compose to be previously installed_
```
git clone https://github.com/g666gle/BaseQuery.git
```
** Copy any databreaches into the ./PutYourdataBasesHere folder at this point **
```
sudo docker-compose run --name BaseQuery --workdir="/root/BaseQuery/" basequery /bin/bash run.sh
```


## Getting Started Guide
1. Place any databases that you have into the "PutYourDataBasesHere" folder
    - As of right now, BaseQuery can only accept files in the format where each line is colon seperated "test@example.com:password" or "password:test@example.com"
    - It doesn't matter if the line formats are mixed up within the same file. Ex) The first line may be "email:password" and the second line can be "password:email"
    - One entry per line!! 
    - If you need a better visual there is an example.txt file in the folder "PutYourDataBasesHere"
    - You should delete the example file before running the program since it has fake data.
1. Now that you have all of your files in the correct folder
    - Open up a terminal in the BaseQuery directory.
    - Type ./install.sh to install all of the resources needed ( You only need to do this once )
    - Type ./run.sh to start the program 
    - **Note that if you are using a laptop make sure it is plugged in. Importing databases uses A LOT of processing power and will make the import 4 times faster on average!**
1. Follow the instructions on the screen
    - That's it, enjoy!
    - Contact me with any issues.

### Import Times Based on Hardware Specifics

<a href="url"><img src="https://user-images.githubusercontent.com/47184892/53662625-5fcf5c80-3c31-11e9-8be3-a43b01106a7c.PNG" height="183" width="535" ></a>


### Query Options

![basequery_query](https://user-images.githubusercontent.com/47184892/53662460-f0596d00-3c30-11e9-8ac6-f0b154ad22b7.PNG)

***



## Built With

* Ubuntu 18.04 bionic

* Bash Version:
GNU bash, version 4.4.19

* Python Version:
3.7.1

## Authors

* **G666gle** -  [Github](https://github.com/G666gle), [Twitter](https://twitter.com/g666g1e)


## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/g666gle/BaseQuery/blob/master/LICENCE.md) file for details

## Disclaimer

**READ UP ON YOUR LOCAL LAWS FIRST BEFORE USING THIS PROGRAM. I TAKE NO RESPONSIBILITY FOR ANYTHING YOU DO WITH BASEQUERY. UNDER NO CIRCUMSTANCE SHOULD BASEQUERY BE USED FOR ILLEGAL PURPOSES.**




