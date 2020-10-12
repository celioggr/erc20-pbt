pragma solidity ^0.5.0;

import "./ERC20.sol";
import "./ERC20Detailed.sol";
import "./Ownable.sol";
import "./ERC20Mintable.sol";


contract OpenZeppelin is ERC20, ERC20Detailed, Ownable, ERC20Mintable{

  constructor(uint256 initialSupply, string memory _name, string memory _symbol, uint8 _decimals)
  ERC20Detailed(_name,_symbol,_decimals) public  {
    _mint(msg.sender, initialSupply);
  }

}
