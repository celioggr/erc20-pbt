
<h3 align="center">ERC-20 pbt</h3>

<p align="center">
  A testing framework based in Property-based testing for assessing the correctness
and compliance of ERC-20 contracts.<br />
  <a href="https://github.com/celioggr/erc20-pbt/blob/master/Property-based%20testing%20of%20ERC-20%20smart%20contracts.pdf"><strong>Thesis document »</strong></a>
  <br/>
  <br/>
</p>

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the project](#about-the-project)
* [Getting started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)

<!-- ABOUT THE PROJECT -->
## About the project


This project was developed by Célio Rodrigues in the context of a Master's thesis in Information security at [FCUP](https://sigarra.up.pt/fcup/en/WEB_PAGE.INICIAL), named *Property-based testing of ERC-20 smart contracts* and advised by Professor [Eduardo Marques](https://github.com/edrdo). 

This ERC-20 testing framework is based upon the creation of a rule-based state machine model
deployed on top of Brownie. Brownie is a Python-based development and testing framework for
Ethereum smart contracts that extends the Hypothesis engine for property-based testing. The
rule-based model is a general one, meaning that any ERC-20 contract can be tested at will. Moreover, it is extensible to other extra functionalities commonly found in contracts such as token
minting, burning and sale. This project provides 8 real-world contracts and 2 reference implementations of ERC-20 to serve as testing examples.


<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

This testing framework has the following dependencies:
* python3 version 3.6 or greater, python3-dev
* ganache-cli version 6.8.2
* Brownie v1.10.4 or greater

### Installation

1. Install pipx
```
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```
2. Install Brownie using pipx
```
pipx install eth-brownie
```
3. Clone the repo
```sh
git clone https://github.com/celioggr/erc20-pbt.git
```


<!-- USAGE EXAMPLES -->
## Usage
To facilitate the invocation of a property-based test with several configurable options, a
simple shell script called `pbt` is used as a wrapper for the invocation of `pytest`. 
The invocation options relate to basic property-based testing parameters. 

* stateful step count
* number of examples
* test seed
* optional shrinking of falsifying examples

Additionally, two operation modes can be enabled:

* coverage monitoring 
* and debug output 

Optional verification features can also be used to check for:
* events 
* return values


Following is the usage message for the `pbt` script.
```
Usage :
pbt [ options ] test1...testn
Options :
−c <arg> : set stateful step count
−n <arg> : set maximum examples
−s <arg> : set seed for tests
−C : measure coverage
−D : enable debug output
−E : enable verification of events
−R : enable verification of return values
−S : enable shrinking
```

<!-- CONTRIBUTING -->
## Contributing

Any contributions are welcome.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/Feature`)
3. Commit your Changes (`git commit -m 'Add some Feature'`)
4. Push to the Branch (`git push origin feature/Feature`)
5. Open a Pull Request

<!-- LICENSE -->
## License

Distributed under the Apache2.0 License. See `LICENSE` for more information.


<!-- CONTACT -->
## Contact

* [Célio Rodrigues](https://github.com/celioggr)

* [Eduardo Marques](https://github.com/edrdo)
